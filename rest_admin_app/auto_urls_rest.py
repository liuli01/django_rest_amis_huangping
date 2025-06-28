from django_rest_admin.my_rest_api import my_rest_viewsetB
from .models import *
from .urls import router
####################################
#for route/FisrtModel
routeName="/FisrtModel"

if routeName[0] == '/':
    routeName = routeName[1:]
tableBName = routeName
foreign_key_ro = {}
foreign_key_id = {}
model_obj_list = ["linenos", "id", "created", "title", "code"]
filter_fields = None
no_need_login = 1
search_fieldsA = ["linenos", "id", "created", "title", "code"]
ordering = ["linenos", "id", "created", "title", "code"]
ordering_fields = ["linenos", "id", "created", "title", "code"]
filter_keys = [{"filter_name": "id", "field_name": "id", "filter_type": "number", "lookup_expr": "exact"}]
foreign_slug_kf = None
if model_obj_list is None:
    model_obj_list="__all__"
if foreign_key_id is not None:
    for i in foreign_key_id:
        foreign_key_id[i]= globals()[foreign_key_id[i][0]]
choice_problems = my_rest_viewsetB(FisrtModel, tableBName + 'V',
               model_obj_list=model_obj_list, no_need_login=no_need_login,
               foreign_key_ro=foreign_key_ro, foreign_key_id=foreign_key_id,
               filter_fieldsA=filter_fields,
               search_fieldsA=search_fieldsA, orderingA=ordering,
               ordering_fieldsA=ordering_fields, filter_keys=filter_keys,
               foreign_slug_kf=foreign_slug_kf)
               

router.register(routeName, choice_problems) 
####################################
####################################
#for route/RestAdminAppCleanmethod
routeName="/RestAdminAppCleanmethod"

if routeName[0] == '/':
    routeName = routeName[1:]
tableBName = routeName
foreign_key_ro = {}
foreign_key_id = {}
model_obj_list = ["id", "method_key", "method_name", "description"]
filter_fields = None
no_need_login = 1
search_fieldsA = ["id", "method_key", "method_name", "description"]
ordering = ["id", "method_key", "method_name", "description"]
ordering_fields = ["id", "method_key", "method_name", "description"]
filter_keys = [{"filter_name": "id", "field_name": "id", "filter_type": "number", "lookup_expr": "exact"}]
foreign_slug_kf = None
if model_obj_list is None:
    model_obj_list="__all__"
if foreign_key_id is not None:
    for i in foreign_key_id:
        foreign_key_id[i]= globals()[foreign_key_id[i][0]]
choice_problems = my_rest_viewsetB(RestAdminAppCleanmethod, tableBName + 'V',
               model_obj_list=model_obj_list, no_need_login=no_need_login,
               foreign_key_ro=foreign_key_ro, foreign_key_id=foreign_key_id,
               filter_fieldsA=filter_fields,
               search_fieldsA=search_fieldsA, orderingA=ordering,
               ordering_fieldsA=ordering_fields, filter_keys=filter_keys,
               foreign_slug_kf=foreign_slug_kf)
               

router.register(routeName, choice_problems) 
####################################
####################################
#for route/RestAdminAppDevice
routeName="/RestAdminAppDevice"

if routeName[0] == '/':
    routeName = routeName[1:]
tableBName = routeName
foreign_key_ro = {}
foreign_key_id = {}
model_obj_list = ["id", "device_id", "name", "remark"]
filter_fields = None
no_need_login = 1
search_fieldsA = ["id", "device_id", "name", "remark"]
ordering = ["id", "device_id", "name", "remark"]
ordering_fields = ["id", "device_id", "name", "remark"]
filter_keys = [{"filter_name": "id", "field_name": "id", "filter_type": "number", "lookup_expr": "exact"}]
foreign_slug_kf = None
if model_obj_list is None:
    model_obj_list="__all__"
if foreign_key_id is not None:
    for i in foreign_key_id:
        foreign_key_id[i]= globals()[foreign_key_id[i][0]]
choice_problems = my_rest_viewsetB(RestAdminAppDevice, tableBName + 'V',
               model_obj_list=model_obj_list, no_need_login=no_need_login,
               foreign_key_ro=foreign_key_ro, foreign_key_id=foreign_key_id,
               filter_fieldsA=filter_fields,
               search_fieldsA=search_fieldsA, orderingA=ordering,
               ordering_fieldsA=ordering_fields, filter_keys=filter_keys,
               foreign_slug_kf=foreign_slug_kf)
               

router.register(routeName, choice_problems) 
####################################
####################################
#for route/RestAdminAppCleaneddata
routeName="/RestAdminAppCleaneddata"

if routeName[0] == '/':
    routeName = routeName[1:]
tableBName = routeName
foreign_key_ro = {"clean_method_id": "clean_method.id", "clean_method_method_key": "clean_method.method_key", "clean_method_method_name": "clean_method.method_name", "clean_method_description": "clean_method.description", "device_id": "device.id", "device_device_id": "device.device_id", "device_name": "device.name", "device_remark": "device.remark"}
foreign_key_id = {'clean_method': ['RestAdminAppCleanmethod', 'DO_NOTHING'], 'device': ['RestAdminAppDevice', 'DO_NOTHING']}
model_obj_list = ["id", "e_key", "e_value", "datetime", "clean_method_id", "device_id"]
filter_fields = None
no_need_login = 1
search_fieldsA = ["id", "e_key", "e_value", "datetime", "clean_method_id", "device_id"]
ordering = ["id", "e_key", "e_value", "datetime", "clean_method_id", "device_id"]
ordering_fields = ["id", "e_key", "e_value", "datetime", "clean_method_id", "device_id"]
filter_keys = [{"filter_name": "id", "field_name": "id", "filter_type": "number", "lookup_expr": "exact"}]
foreign_slug_kf = None
if model_obj_list is None:
    model_obj_list="__all__"
if foreign_key_id is not None:
    for i in foreign_key_id:
        foreign_key_id[i]= globals()[foreign_key_id[i][0]]
choice_problems = my_rest_viewsetB(RestAdminAppCleaneddata, tableBName + 'V',
               model_obj_list=model_obj_list, no_need_login=no_need_login,
               foreign_key_ro=foreign_key_ro, foreign_key_id=foreign_key_id,
               filter_fieldsA=filter_fields,
               search_fieldsA=search_fieldsA, orderingA=ordering,
               ordering_fieldsA=ordering_fields, filter_keys=filter_keys,
               foreign_slug_kf=foreign_slug_kf)
               

router.register(routeName, choice_problems) 
####################################
####################################
#for route/RestAdminAppRawdata
routeName="/RestAdminAppRawdata"

if routeName[0] == '/':
    routeName = routeName[1:]
tableBName = routeName
foreign_key_ro = {"device_id": "device.id", "device_device_id": "device.device_id", "device_name": "device.name", "device_remark": "device.remark"}
foreign_key_id = {'device': ['RestAdminAppDevice', 'DO_NOTHING']}
model_obj_list = ["id", "e_key", "e_name", "e_num", "e_value", "e_unit", "datetime", "device_id"]
filter_fields = None
no_need_login = 1
search_fieldsA = ["id", "e_key", "e_name", "e_num", "e_value", "e_unit", "datetime", "device_id"]
ordering = ["id", "e_key", "e_name", "e_num", "e_value", "e_unit", "datetime", "device_id"]
ordering_fields = ["id", "e_key", "e_name", "e_num", "e_value", "e_unit", "datetime", "device_id"]
filter_keys = [{"filter_name": "id", "field_name": "id", "filter_type": "number", "lookup_expr": "exact"}]
foreign_slug_kf = None
if model_obj_list is None:
    model_obj_list="__all__"
if foreign_key_id is not None:
    for i in foreign_key_id:
        foreign_key_id[i]= globals()[foreign_key_id[i][0]]
choice_problems = my_rest_viewsetB(RestAdminAppRawdata, tableBName + 'V',
               model_obj_list=model_obj_list, no_need_login=no_need_login,
               foreign_key_ro=foreign_key_ro, foreign_key_id=foreign_key_id,
               filter_fieldsA=filter_fields,
               search_fieldsA=search_fieldsA, orderingA=ordering,
               ordering_fieldsA=ordering_fields, filter_keys=filter_keys,
               foreign_slug_kf=foreign_slug_kf)
               

router.register(routeName, choice_problems) 
####################################
