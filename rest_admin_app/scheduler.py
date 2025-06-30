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
    清洗最近2小时的原始数据,写入 CleanedData 表
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