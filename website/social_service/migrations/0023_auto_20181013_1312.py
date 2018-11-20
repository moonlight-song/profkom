# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-13 10:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_service', '0022_auto_20181013_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='period',
            name='application_type',
            field=models.CharField(choices=[('meals', 'Бесплатное питание'), ('profilaktory', 'Профилакторий'), ('apos_regular', 'Ежемесячный АПОС'), ('apos_single', 'Единоразовый АПОС')], max_length=30),
        ),
    ]
