from django.contrib.auth.models import User
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class FisrtModel(models.Model):
    linenos = models.BooleanField()
    #    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField()
    title = models.CharField(max_length=100, blank=True, null=True)
    code = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'fisrt_model'
        
class RestAdminAppDevice(models.Model):
    #    id = models.BigAutoField(primary_key=True)
    device_id = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=100)
    remark = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'rest_admin_app_device'

class RestAdminAppRawdata(models.Model):
    #    id = models.BigAutoField(primary_key=True)
    e_key = models.CharField(max_length=10)
    e_name = models.CharField(max_length=50)
    e_num = models.CharField(max_length=20)
    e_value = models.FloatField()
    e_unit = models.CharField(max_length=20)
    datetime = models.DateTimeField()
    device = models.ForeignKey(to=RestAdminAppDevice, db_constraint=False, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='RestAdminAppRawdata_device')

    class Meta:
        managed = True
        db_table = 'rest_admin_app_rawdata'


class RestAdminAppCleanmethod(models.Model):
    #    id = models.BigAutoField(primary_key=True)
    method_key = models.CharField(unique=True, max_length=50)
    method_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'rest_admin_app_cleanmethod'


class RestAdminAppCleaneddata(models.Model):
    #    id = models.BigAutoField(primary_key=True)
    e_key = models.CharField(max_length=10)
    e_value = models.FloatField()
    datetime = models.DateTimeField()
    clean_method = models.ForeignKey(to=RestAdminAppCleanmethod, db_constraint=False, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='RestAdminAppCleaneddata_clean_method')
    device = models.ForeignKey(to=RestAdminAppDevice, db_constraint=False, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='RestAdminAppCleaneddata_device')

    class Meta:
        managed = True
        db_table = 'rest_admin_app_cleaneddata'




