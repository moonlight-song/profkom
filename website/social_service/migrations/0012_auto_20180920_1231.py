# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-20 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_service', '0011_auto_20180920_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='period',
            name='application_type',
            field=models.CharField(choices=[('profilaktory', 'Профилакторий'), ('meals', 'Бесплатное питание'), ('apos_single', 'Единоразовый АПОС'), ('apos_regular', 'Ежемесячный АПОС')], max_length=30),
        ),
    ]
