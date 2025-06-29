# Generated by Django 5.2.3 on 2025-06-30 10:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_admin_app', '0006_alter_fisrtmodel_created_alter_fisrtmodel_linenos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rawdata',
            name='device',
        ),
        migrations.AlterModelOptions(
            name='restadminappcleanmethod',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='restadminappdevice',
            options={'managed': True},
        ),
        migrations.AlterModelTable(
            name='restadminappcleanmethod',
            table='rest_admin_app_cleanmethod',
        ),
        migrations.AlterModelTable(
            name='restadminappdevice',
            table='rest_admin_app_device',
        ),
        migrations.RenameModel(
            old_name='CleanMethod',
            new_name='RestAdminAppCleanmethod',
        ),
        migrations.CreateModel(
            name='RestAdminAppCleaneddata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('e_key', models.CharField(max_length=10)),
                ('e_value', models.FloatField()),
                ('datetime', models.DateTimeField()),
                ('clean_method', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='RestAdminAppCleaneddata_clean_method', to='rest_admin_app.restadminappcleanmethod')),
                ('device', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='RestAdminAppCleaneddata_device', to='rest_admin_app.restadminappdevice')),
            ],
            options={
                'db_table': 'rest_admin_app_cleaneddata',
                'managed': True,
            },
        ),
        migrations.RenameModel(
            old_name='Device',
            new_name='RestAdminAppDevice',
        ),
        migrations.CreateModel(
            name='RestAdminAppRawdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('e_key', models.CharField(max_length=10)),
                ('e_name', models.CharField(max_length=50)),
                ('e_num', models.CharField(max_length=20)),
                ('e_value', models.FloatField()),
                ('e_unit', models.CharField(max_length=20)),
                ('datetime', models.DateTimeField()),
                ('device', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='RestAdminAppRawdata_device', to='rest_admin_app.restadminappdevice')),
            ],
            options={
                'db_table': 'rest_admin_app_rawdata',
                'managed': True,
            },
        ),
        migrations.DeleteModel(
            name='CleanedData',
        ),
        migrations.DeleteModel(
            name='RawData',
        ),
    ]
