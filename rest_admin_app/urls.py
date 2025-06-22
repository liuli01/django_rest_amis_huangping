
from django.contrib import admin
from django.urls import path, re_path
from django.urls import path, include
from django.views.generic.base import RedirectView

from django.urls import re_path, path, include
from rest_framework import routers
import traceback
router = routers.DefaultRouter()

try:
    from .auto_urls_rest import *
except Exception as e:
    traceback.print_exc()
    print('ERROR: django_rest_admin error. rest may not not work as expected.')
    print(e)


def default_list(request):
    """
    this is used for api url location reverse.
    """
    return ''

urlpatterns = [
    path('', include(router.urls)),
    path('default_list/', default_list, name='django_rest_admin_default_list'),
]

