"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_admin_app.views_echarts import site_obj
from rest_admin_app.views import (
    CleanedDataCompareView,
    CleanedDataExportView,
    FilterOptionsView,
    water_quality_view,
    export_cleaned_data

)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('front/', include('django_amis_render.urls')),
    path('render/', include('myRenderApp.urls')),
    path('api/', include('rest_admin_app.urls')),
    path('amis-api/', include('amisproxy.urls')),

    path('echarts/', include(site_obj.urls)), 
    path("api/cleaned-data/compare/", CleanedDataCompareView.as_view(), name="cleaned_data_compare"),
    path("api/cleaned-data/export/", CleanedDataExportView.as_view(), name="cleaned_data_export"),
    path("api/filter-options/", FilterOptionsView.as_view(), name="filter_options"),
    path('api/cleaned-data-compare/', CleanedDataCompareView.as_view(), name='cleaned_data_compare'),
    path('water-quality/', water_quality_view, name='water-quality'),
    path('echarts/export_data/', export_cleaned_data, name='export_data'),

]


