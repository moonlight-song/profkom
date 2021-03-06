# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-19 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_service', '0007_auto_20180911_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='affected_by_chernobyl',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='claim',
            name='is_orphan',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='claim',
            name='lives_in_dormitory',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='claim',
            name='sms_notification',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='period',
            name='application_type',
            field=models.CharField(choices=[('apos_regular', 'Ежемесячный АПОС'), ('meals', 'Бесплатное питание'), ('profilaktory', 'Профилакторий'), ('apos_single', 'Единоразовый АПОС')], max_length=30),
        ),
    ]
