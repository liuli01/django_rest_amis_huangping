# Generated by Django 5.2 on 2025-04-14 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_admin_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fisrtmodel',
            name='created',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='fisrtmodel',
            name='linenos',
            field=models.BooleanField(),
        ),
    ]
