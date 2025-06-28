
from django.core.management.base import BaseCommand
from rest_admin_app.models import RestAdminAppCleanmethod,RestAdminAppDevice

CLEAN_METHODS = {
    "moving_avg": ("滑动平均", "按固定窗口取平均"),
    "median": ("中值滤波", "按窗口取中位数，平滑异常值"),
    "zscore": ("Z-Score滤波", "统计偏差异常值剔除"),
}

DEVICES = [
    {"device_id": "11130301", "name": "管网监测点1"},
    {"device_id": "11130302", "name": "管网监测点2"},
    {"device_id": "11130303", "name": "管网监测点3"},
    {"device_id": "11130304", "name": "管网监测点4"},
    {"device_id": "11130305", "name": "管网监测点5"},
]

class Command(BaseCommand):
    help = "初始化设备和清洗方法数据"

    def handle(self, *args, **kwargs):
        for key, (name, desc) in CLEAN_METHODS.items():
            obj, created = RestAdminAppCleanmethod.objects.get_or_create(
                method_key=key,
                defaults={"method_name": name, "description": desc}
            )
            self.stdout.write(self.style.SUCCESS(
                f"{'新增' if created else '存在'}清洗方法: {key} - {name}"
            ))

        for item in DEVICES:
            obj, created = RestAdminAppDevice.objects.get_or_create(
                device_id=item["device_id"],
                defaults={"name": item["name"]}
            )
            self.stdout.write(self.style.SUCCESS(
                f"{'新增' if created else '存在'}设备: {item['device_id']} - {item['name']}"
            ))
