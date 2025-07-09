import logging
import requests
from datetime import datetime, timedelta
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.util import close_old_connections
from rest_admin_app.cleaning import CLEAN_METHODS
from collections import defaultdict

from rest_admin_app.models import RestAdminAppDevice, RestAdminAppRawdata, RestAdminAppCleaneddata, RestAdminAppCleanmethod
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


def my_job():
    print("定时任务执行中...")


@close_old_connections
def fetch_device_data():
    """
    拉取所有设备数据并写入 RawData
    """
    devices = RestAdminAppDevice.objects.all()
    for device in devices:
        url = f"http://47.105.215.208:8005/intfa/queryData/{device.device_id}"
        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            data = resp.json()

            for item in data.get("entity", []):
                dt = datetime.strptime(item["datetime"], "%Y-%m-%d %H:%M:%S")
                RestAdminAppRawdata.objects.update_or_create(
                    device=device,
                    e_key=item["eKey"],
                    datetime=dt,
                    defaults={
                        "e_name": item["eName"],
                        "e_value": float(item["eValue"]),
                        "e_unit": item["eUnit"],
                        "e_num": item["eNum"]
                    }
                )
        except Exception as e:
            logger.error(f"设备 {device.device_id} 获取失败: {e}")





@close_old_connections
def clean_device_data():
    """
    清洗最近2小时的原始数据写入 CleanedData 表
    """
    logger.info("[任务] 开始执行数据清洗任务...")
    try:
        time_threshold = datetime.now() - timedelta(hours=2)
        method_map = {m.method_key: m for m in RestAdminAppCleanmethod.objects.all()}
        devices = RestAdminAppDevice.objects.all()

        for device in devices:
            try:
                raw_qs = RestAdminAppRawdata.objects.filter(device=device, datetime__gte=time_threshold)
                data_grouped = defaultdict(list)
                for data in raw_qs:
                    data_grouped[data.e_key].append(data)

                for e_key, data_list in data_grouped.items():
                    datetimes = [d.datetime for d in data_list]
                    values = [d.e_value for d in data_list]

                    for method_key, method_def in CLEAN_METHODS.items():
                        clean_func = method_def["func"]
                        method_obj = method_map.get(method_key)
                        if not method_obj:
                            logger.warning(f"[警告] 清洗方法 {method_key} 未注册到数据库，跳过")
                            continue

                        try:
                            cleaned_values = clean_func(values)
                        except Exception as e:
                            logger.error(f"[错误] 方法 {method_key} 清洗失败 (设备: {device.device_id}, 参数: {e_key}): {e}")
                            continue

                        for dt, val in zip(datetimes, cleaned_values):
                            if val is None:
                                continue
                            RestAdminAppCleaneddata.objects.update_or_create(
                                device=device,
                                e_key=e_key,
                                clean_method=method_obj,
                                datetime=dt,
                                defaults={"e_value": round(val, 4)}
                            )
            except Exception as e:
                logger.error(f"[错误] 清洗设备 {device.device_id} 失败: {e}")

    except Exception as e:
        logger.error(f"[致命错误] 数据清洗任务执行失败: {e}")
    else:
        logger.info("[任务] 数据清洗完成。")





@close_old_connections
def history_trend_clean_all(method_keys=CLEAN_METHODS.keys()):
    """
    清空 CleanedData 表后，对所有设备、参数执行历史趋势拟合清洗
    对所有设备、所有参数的历史数据执行 trend_fit、savgol 等趋势拟合清洗，并批量写入 CleanedData 表
    """
    logger.info("[任务] 开始执行历史趋势拟合清洗任务...")
    try:
        # 全表删除
        RestAdminAppCleaneddata.objects.all().delete()
        logger.info("[清理] 已清空 CleanedData 表全部历史数据")
        # 拉取数据库中已注册的方法对象
        method_map = {
            m.method_key: m
            for m in RestAdminAppCleanmethod.objects.filter(method_key__in=method_keys)
        }

        # 检查未注册的方法
        for key in method_keys:
            if key not in CLEAN_METHODS:
                logger.warning(f"[跳过] 清洗方法 {key} 未在 CLEAN_METHODS 中注册")
            elif key not in method_map:
                logger.warning(f"[跳过] 清洗方法 {key} 未在数据库中注册")

        devices = RestAdminAppDevice.objects.all()

        for device in devices:
            try:
                raw_qs = RestAdminAppRawdata.objects.filter(device=device).order_by("datetime")
                if not raw_qs.exists():
                    continue

                # 按 e_key 分组
                data_grouped = defaultdict(list)
                for data in raw_qs:
                    data_grouped[data.e_key].append(data)

                for e_key, data_list in data_grouped.items():
                    datetimes = [d.datetime for d in data_list]
                    values = [d.e_value for d in data_list]

                    for method_key in method_keys:
                        method_def = CLEAN_METHODS.get(method_key)
                        method_obj = method_map.get(method_key)

                        if not method_def or not method_obj:
                            continue

                        clean_func = method_def["func"]

                        try:
                            cleaned_values = clean_func(values)
                        except Exception as e:
                            logger.error(f"[错误] 方法 {method_key} 拟合失败 (设备: {device.device_id}, 参数: {e_key}): {e}")
                            continue

                        # 已有记录的时间点集合（用于去重）
                        existing_times = set(
                            RestAdminAppCleaneddata.objects.filter(
                                device=device,
                                e_key=e_key,
                                clean_method=method_obj,
                                datetime__in=datetimes
                            ).values_list("datetime", flat=True)
                        )

                        # 构建待插入对象列表
                        objs_to_create = [
                            RestAdminAppCleaneddata(
                                device=device,
                                e_key=e_key,
                                clean_method=method_obj,
                                datetime=dt,
                                e_value=round(val, 4)
                            )
                            for dt, val in zip(datetimes, cleaned_values)
                            if val is not None and dt not in existing_times
                        ]

                        if objs_to_create:
                            RestAdminAppCleaneddata.objects.bulk_create(objs_to_create, batch_size=1000)

                        logger.info(f"[完成] 设备 {device.device_id} - 参数 {e_key} - 方法 {method_key} 清洗完成，新增 {len(objs_to_create)} 条")
            except Exception as e:
                logger.error(f"[错误] 设备 {device.device_id} 清洗失败: {e}")

    except Exception as e:
        logger.error(f"[致命错误] 历史趋势清洗任务失败: {e}")
    else:
        logger.info("[任务] 历史趋势拟合清洗全部完成。")

