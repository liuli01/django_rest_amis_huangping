# ...
from django_echarts.starter.sites import DJESite
from django_echarts.entities import Copyright
from pyecharts import options as opts
from pyecharts.charts import Bar
from rest_admin_app.models import RestAdminAppDevice, RestAdminAppRawdata, RestAdminAppCleaneddata, RestAdminAppCleanmethod
from pyecharts.charts import Line


site_obj = DJESite(site_title="设备数据平台")

@site_obj.register_chart(title='设备原始数据 vs 清洗数据对比', catalog='清洗分析')
def device_raw_vs_cleaned():
    # 示例参数：你也可以在这里换成实际筛选值
    device_name = '管网监测点1'
    e_name = 'COD'
    method_name = 'Z-Score滤波'

    # 过滤对应对象
    device = RestAdminAppDevice.objects.filter(name=device_name).first()
    method = RestAdminAppCleanmethod.objects.filter(method_name=method_name).first()
    e_key = RestAdminAppRawdata.objects.filter(device=device, e_name=e_name).first().e_key
    print(f"设备: {device}, 清洗方法: {method}, 指标 : {e_key}")

    # 原始数据
    raw_qs = RestAdminAppRawdata.objects.filter(device=device, e_name=e_name).order_by("datetime")[:100]
    raw_times = [r.datetime.strftime("%Y-%m-%d %H:%M") for r in raw_qs]
    raw_values = [r.e_value for r in raw_qs]

    # 清洗数据
    clean_qs = RestAdminAppCleaneddata.objects.filter(device=device, clean_method=method, e_key=e_key ).order_by("datetime")[:100]
    print(f"清洗数据数量: {clean_qs.count()}")
    clean_times = [c.datetime.strftime("%Y-%m-%d %H:%M") for c in clean_qs]
    clean_values = [c.e_value for c in clean_qs]

    # 构建折线图
    line = (
        Line()
        .add_xaxis(raw_times)
        .add_yaxis("原始数据", raw_values, is_smooth=True, linestyle_opts=opts.LineStyleOpts(type_="solid"),label_opts=opts.LabelOpts(is_show=False, position="top"))
        .add_yaxis("清洗数据", clean_values, is_smooth=True, linestyle_opts=opts.LineStyleOpts(type_="dashed"),label_opts=opts.LabelOpts(is_show=False, position="top"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"{device_name} - {e_name} 数据对比", subtitle=f"清洗方法：{method_name}"),
            xaxis_opts=opts.AxisOpts(name="时间", type_="category", boundary_gap=False),
            yaxis_opts=opts.AxisOpts(name="数值"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            datazoom_opts=[opts.DataZoomOpts()],
        )
    )
    return line