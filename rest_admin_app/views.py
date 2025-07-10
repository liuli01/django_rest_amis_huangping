from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_admin_app.models import RestAdminAppDevice, RestAdminAppRawdata, RestAdminAppCleaneddata, RestAdminAppCleanmethod
from django.utils.dateparse import parse_datetime

class CleanedDataCompareView(APIView):
    def get(self, request):
        device_id = request.GET.get("device_id")
        e_key = request.GET.get("e_key")
        method_keys = request.GET.getlist("methods[]")
        start = parse_datetime(request.GET.get("start"))
        end = parse_datetime(request.GET.get("end"))

        if not all([device_id, e_key, start, end]):
            return Response({"status": 1, "msg": "参数不完整"}, status=status.HTTP_400_BAD_REQUEST)

        device = RestAdminAppDevice.objects.filter(device_id=device_id).first()
        if not device:
            return Response({"status": 1, "msg": "设备不存在"}, status=status.HTTP_404_NOT_FOUND)

        # 原始数据
        raw_qs = RestAdminAppRawdata.objects.filter(
            device=device, e_key=e_key, datetime__range=(start, end)
        ).order_by("datetime")

        xAxis = [r.datetime.strftime("%Y-%m-%d %H:%M") for r in raw_qs]
        raw_series = [round(r.e_value, 4) for r in raw_qs]
        table_rows = [{"datetime": r.datetime.strftime("%Y-%m-%d %H:%M"), "raw": round(r.e_value, 4)} for r in raw_qs]

        # 清洗数据
        series = [{"name": "原始数据", "type": "line", "data": raw_series}]
        legend = ["原始数据"]

        for method_key in method_keys:
            method = RestAdminAppCleanmethod.objects.filter(method_key=method_key).first()
            if not method:
                continue

            cleaned = RestAdminAppCleaneddata.objects.filter(
                device=device,
                e_key=e_key,
                clean_method=method,
                datetime__range=(start, end)
            ).order_by("datetime")

            clean_series = {c.datetime.strftime("%Y-%m-%d %H:%M"): round(c.e_value, 4) for c in cleaned}
            y_data = [clean_series.get(dt, None) for dt in xAxis]

            series.append({
                "name": method.method_name,
                "type": "line",
                "data": y_data
            })
            legend.append(method.method_name)

            # 添加到表格中
            for row in table_rows:
                row[method_key] = clean_series.get(row["datetime"], None)

        return Response({
            "status": 0,
            "msg": "ok",
            "data": {
                "chart": {
                    "legend": legend,
                    "xAxis": xAxis,
                    "series": series
                },
                "table": table_rows
            }
        })
    



import io
import pandas as pd
from datetime import datetime
from django.http import FileResponse

class CleanedDataExportView(APIView):
    def get(self, request):
        device_id = request.GET.get("device_id")
        e_key = request.GET.get("e_key")
        method_keys = request.GET.getlist("methods[]")
        start = parse_datetime(request.GET.get("start"))
        end = parse_datetime(request.GET.get("end"))

        if not all([device_id, e_key, start, end]):
            return Response({"status": 1, "msg": "参数不完整"}, status=status.HTTP_400_BAD_REQUEST)

        device = RestAdminAppDevice.objects.filter(device_id=device_id).first()
        if not device:
            return Response({"status": 1, "msg": "设备不存在"}, status=status.HTTP_404_NOT_FOUND)

        # 原始数据 DataFrame
        raw_qs = RestAdminAppRawdata.objects.filter(
            device=device, e_key=e_key, datetime__range=(start, end)
        ).order_by("datetime")

        df = pd.DataFrame([{
            "时间": r.datetime.strftime("%Y-%m-%d %H:%M"),
            "原始值": round(r.e_value, 4)
        } for r in raw_qs])

        # 清洗数据列合并
        for method_key in method_keys:
            method = RestAdminAppCleanmethod.objects.filter(method_key=method_key).first()
            if not method:
                continue

            clean_qs = RestAdminAppCleaneddata.objects.filter(
                device=device, e_key=e_key, clean_method=method,
                datetime__range=(start, end)
            )

            clean_map = {
                c.datetime.strftime("%Y-%m-%d %H:%M"): round(c.e_value, 4)
                for c in clean_qs
            }

            df[method.method_name] = df["时间"].map(clean_map)

        # 保存为 Excel
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="清洗数据对比")

        buffer.seek(0)
        filename = f"{device.name}_{e_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        return FileResponse(buffer, as_attachment=True, filename=filename, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")




class FilterOptionsView(APIView):
    def get(self, request):
        device_id = request.GET.get("device_id")
        response_data = {}

        # 设备列表
        devices = RestAdminAppDevice.objects.all()
        response_data["devices"] = [
    {
        "label": d.name,
        "value": d.device_id,
        "selected": idx == 0  # ✅ 选中第一个
    }
    for idx, d in enumerate(devices)
]

        # e_key 参数列表（基于当前 device_id）
        if device_id:
            device = RestAdminAppDevice.objects.filter(device_id=device_id).first()
            if device:
                e_keys = (
                    RestAdminAppRawdata.objects.filter(device=device)
                    .values("e_key", "e_name")
                    .distinct()
                )
                response_data["e_keys"] = [
                    {
                        "label": item["e_name"],
                        "value": item["e_key"],
                        "selected": idx == 0  # 默认第一个选中
                    }
                    for idx, item in enumerate(e_keys)
                ]
            else:
                response_data["e_keys"] = []
        else:
            response_data["e_keys"] = []

        # 清洗方法列表
        methods = RestAdminAppCleanmethod.objects.all()
        response_data["methods"] = [
                {
                    "label": m.method_name,
                    "value": m.method_key,
                    "selected": idx == 0  # 第一个方法选中
                }
                for idx, m in enumerate(methods)]

        return Response({"status": 0, "msg": "ok", "data": response_data})


from django.http import HttpResponse
from rest_admin_app.models import RestAdminAppCleaneddata
import csv
from datetime import timedelta
from django.db.models import Avg
# def export_cleaned_data(request):
#     device_name = request.GET.get("device")
#     e_name = request.GET.get("indicator")  # 中文名
#     method_name = request.GET.get("method")
#     start = request.GET.get("start")
#     end = request.GET.get("end")

#     if not all([device_name, e_name, method_name, start, end]):
#         return HttpResponse("缺少必要参数", status=400)

#     try:
#         device = RestAdminAppDevice.objects.get(name=device_name)
#         method = RestAdminAppCleanmethod.objects.get(method_name=method_name)
#     except RestAdminAppDevice.DoesNotExist:
#         return HttpResponse("设备不存在", status=404)
#     except RestAdminAppCleanmethod.DoesNotExist:
#         return HttpResponse("清洗方法不存在", status=404)

#     start_dt = parse_datetime(start)
#     end_dt = parse_datetime(end)
#     if not start_dt or not end_dt:
#         return HttpResponse("时间格式错误，应为 ISO 格式", status=400)

#     # 查询 e_key
#     raw_qs = RestAdminAppRawdata.objects.filter(e_name=e_name)
#     e_keys = list(raw_qs.values_list("e_key", flat=True).distinct())
#     e_key_to_name = {obj.e_key: obj.e_name for obj in raw_qs.only("e_key", "e_name")}

#     if not e_keys:
#         return HttpResponse(f"未找到指标 {e_name} 对应的 e_key", status=404)

#     # 查询清洗数据
#     cleaned_qs = RestAdminAppCleaneddata.objects.filter(
#         device=device,
#         clean_method=method,
#         e_key__in=e_keys,
#         datetime__range=(start_dt, end_dt)
#     ).order_by("datetime")

#     if not cleaned_qs.exists():
#         return HttpResponse("没有匹配的清洗数据", status=404)

#     # 建立 { (e_key, datetime): 原始值 } 映射
#     rawdata_map = {
#         (r.e_key, r.datetime): r.e_value
#         for r in RestAdminAppRawdata.objects.filter(
#             device=device,
#             e_key__in=e_keys,
#             datetime__range=(start_dt, end_dt)
#         )
#     }

#     # 构建 CSV 响应
#     response = HttpResponse(content_type='text/csv')
#     filename = f"{device_name}_{e_name}_{method_name}_with_raw.csv".replace(" ", "_")
#     response['Content-Disposition'] = f'attachment; filename="{filename}"'

#     writer = csv.writer(response)
#     writer.writerow(['时间', '设备', '指标', '清洗方法', '原始值', '清洗值'])

#     for row in cleaned_qs:
#         raw_value = rawdata_map.get((row.e_key, row.datetime), "")
#         writer.writerow([
#             row.datetime.strftime('%Y-%m-%d %H:%M:%S'),
#             device.name,
#             e_key_to_name.get(row.e_key, row.e_key),
#             method.method_name,
#             raw_value,
#             row.e_value
#         ])
#     return response

def export_cleaned_data(request):
    device_name = request.GET.get("device")
    e_name = request.GET.get("indicator")  # 中文名
    method_name = request.GET.get("method")
    start = request.GET.get("start")
    end = request.GET.get("end")

    if not all([device_name, e_name, method_name, start, end]):
        return HttpResponse("缺少必要参数", status=400)

    try:
        device = RestAdminAppDevice.objects.get(name=device_name)
        method = RestAdminAppCleanmethod.objects.get(method_name=method_name)
    except RestAdminAppDevice.DoesNotExist:
        return HttpResponse("设备不存在", status=404)
    except RestAdminAppCleanmethod.DoesNotExist:
        return HttpResponse("清洗方法不存在", status=404)

    start_dt = parse_datetime(start)
    end_dt = parse_datetime(end)
    if not start_dt or not end_dt:
        return HttpResponse("时间格式错误，应为 ISO 格式", status=400)

    # 获取 e_keys
    raw_qs = RestAdminAppRawdata.objects.filter(e_name=e_name)
    e_keys = list(raw_qs.values_list("e_key", flat=True).distinct())
    e_key_to_name = {obj.e_key: obj.e_name for obj in raw_qs.only("e_key", "e_name")}

    if not e_keys:
        return HttpResponse(f"未找到指标 {e_name} 对应的 e_key", status=404)

    cleaned_qs = RestAdminAppCleaneddata.objects.filter(
        device=device,
        clean_method=method,
        e_key__in=e_keys,
        datetime__range=(start_dt, end_dt)
    ).order_by("datetime")

    if not cleaned_qs.exists():
        return HttpResponse("没有匹配的清洗数据", status=404)

    # 响应
    response = HttpResponse(content_type='text/csv')
    filename = f"{device_name}_{e_name}_{method_name}_export.csv".replace(" ", "_")
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)

    is_hourly_avg = method_name == "小时平均"

    if is_hourly_avg:
        writer.writerow(['时间', '设备', '指标', '清洗方法', '清洗值'])

        seen_timestamps = set()
        for row in cleaned_qs:
            # 只保留每小时一条
            dt_str = row.datetime.strftime("%Y/%m/%d %H:00:00")  # 注意统一格式
            if dt_str in seen_timestamps:
                continue
            seen_timestamps.add(dt_str)

            writer.writerow([
                dt_str,
                device.name,
                e_key_to_name.get(row.e_key, row.e_key),
                method.method_name,
                round(row.e_value, 4)
            ])  
    else:
        writer.writerow(['时间', '设备', '指标', '清洗方法', '原始值', '清洗值'])

        # 获取原始数据映射
        raw_map = {
            (r.e_key, r.datetime): r.e_value
            for r in RestAdminAppRawdata.objects.filter(
                device=device,
                e_key__in=e_keys,
                datetime__range=(start_dt, end_dt)
            )
        }

        seen = set()
        for row in cleaned_qs:
            dt_str = row.datetime.strftime("%Y-%m-%d %H:%M:%S")
            key = (dt_str, round(row.e_value, 4))
            if key in seen:
                continue
            seen.add(key)
            raw_val = raw_map.get((row.e_key, row.datetime), "")
            writer.writerow([
                dt_str,
                device.name,
                e_key_to_name.get(row.e_key, row.e_key),
                method.method_name,
                raw_val,
                row.e_value
            ])

    return response

# water_monitor/views.py
from django.shortcuts import render

def water_quality_view(request):
    return render(request, 'water_quality_monitoring.html')