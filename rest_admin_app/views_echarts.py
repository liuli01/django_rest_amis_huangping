# ...
from django_echarts.starter.sites import DJESite
from django_echarts.entities import Copyright
from pyecharts import options as opts
from pyecharts.charts import Bar
from rest_admin_app.models import RestAdminAppDevice, RestAdminAppRawdata, RestAdminAppCleaneddata, RestAdminAppCleanmethod
from pyecharts.charts import Line
from django_echarts.entities.uri import ParamsConfig




# @site_obj.register_chart(title='{year}年福建省家庭户类型组成', 
#                         params_config=ParamsConfig({'year': [1982, 1990, 2000, 2010, 2020]}))
# def yearly_family_types(year: int):
#     family_types = [
#         '一人户', '二人户', '三人户', '四人户', '五人户', '六人户', '七人户', '八人户', '九人户', '十人及其以上'
#     ]
#     data = [
#         [1982, 7.7, 8.2, 12.2, 17.1, 18.4, 14.7, 10.1, 11.6, 0, 0],
#         [1990, 5.8, 8.6, 16.8, 23.6, 21.4, 11.8, 5.9, 2.9, 1.4, 1.8],
#         [2000, 9.1, 15.5, 25.4, 24.7, 15.8, 5.9, 2.2, 0.8, 0.3, 0.3],
#         [2010, 12.1, 17.2, 24.3, 21.7, 13.7, 6.4, 2.6, 1.1, 0.5, 0.4],
#         [2020, 27.3, 26.3, 19.4, 14.2, 6.9, 4, 1.1, 0.4, 0.2, 0.2]
#     ]
#     yearly_data = {item[0]: item[1:] for item in data}

#     year_data = yearly_data[year]
#     bar = (
#         Bar()
#             .add_xaxis(family_types).add_yaxis('百分比(%)', year_data)
#             .set_global_opts(title_opts=opts.TitleOpts("福建省家庭户类型构成-{}年".format(year)))
#     )
#     return bar




device_name_list= RestAdminAppDevice.objects.values_list('name', flat=True).distinct()
device_name_list = list(device_name_list) 
e_name_list = RestAdminAppRawdata.objects.filter(device__name=device_name_list[0]).values_list('e_name', flat=True).distinct()
e_name_list = list(e_name_list)
method_name_list = RestAdminAppCleanmethod.objects.values_list('method_name', flat=True).distinct()
method_name_list = list(method_name_list)
# print(f"设备列表: {device_name_list}")
# print(f"指标列表: {e_name_list}")
# print(f"清洗方法列表: {method_name_list}")

site_obj = DJESite(site_title="设备数据平台",ignore_register_nav=True)
@site_obj.register_chart(title='{device_name}-{e_name}指标-{method_name}数据清洗', params_config=ParamsConfig({
    'device_name': device_name_list,
    'e_name': e_name_list,
    'method_name': method_name_list})
)
def device_raw_vs_cleaned(device_name: str, e_name: str, method_name: str):
    # 示例参数：你也可以在这里换成实际筛选值
    # device_name = '管网监测点2'
    # e_name = 'COD'
    # method_name = '滑动平均'
    # method_name = '中值滤波'
    # method_name = 'Z-Score滤波'

    # 过滤对应对象
    device = RestAdminAppDevice.objects.filter(name=device_name).first()
    method = RestAdminAppCleanmethod.objects.filter(method_name=method_name).first()
    e_key = RestAdminAppRawdata.objects.filter(device=device, e_name=e_name).first().e_key
    print(f"设备: {device}, 清洗方法: {method}, 指标 : {e_key}")

    # 原始数据
    raw_qs = RestAdminAppRawdata.objects.filter(device=device, e_name=e_name).order_by("datetime")
    raw_dict = {r.datetime.strftime("%Y-%m-%d %H:%M"): r.e_value for r in raw_qs}

    # 清洗数据
    clean_qs = RestAdminAppCleaneddata.objects.filter(device=device, clean_method=method, e_key=e_key ).order_by("datetime")
    clean_dict = {c.datetime.strftime("%Y-%m-%d %H:%M"): c.e_value for c in clean_qs}

    # 取时间点交集，保证一一对应
    common_times = sorted(set(raw_dict.keys()) & set(clean_dict.keys()))
    raw_values = [raw_dict[t] for t in common_times]
    clean_values = [clean_dict[t] for t in common_times]

    # 构建折线图
    line = (
        Line()
        .add_xaxis(common_times)
        .add_yaxis("原始数据", raw_values, is_smooth=True, linestyle_opts=opts.LineStyleOpts(type_="solid"),label_opts=opts.LabelOpts(is_show=False, position="top"))
        .add_yaxis("清洗数据", clean_values, is_smooth=True, linestyle_opts=opts.LineStyleOpts(type_="dashed"),label_opts=opts.LabelOpts(is_show=False, position="top"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"{device_name} - {e_name} 数据对比", subtitle=f"清洗方法：{method_name}"),
            xaxis_opts=opts.AxisOpts(name="时间", type_="category", boundary_gap=False),
            yaxis_opts=opts.AxisOpts(name="数值"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            datazoom_opts=[opts.DataZoomOpts()],
            toolbox_opts=opts.ToolboxOpts(is_show=False)
            
        )
    )


    return line

