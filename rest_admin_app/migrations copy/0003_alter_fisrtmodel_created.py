# Generated by Django 5.2 on 2025-04-14 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_admin_app', '0002_alter_fisrtmodel_created_alter_fisrtmodel_linenos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fisrtmodel',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
