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
