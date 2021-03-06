# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-20 09:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_document'),
        ('social_service', '0010_auto_20180920_1018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='claim',
            name='documents',
        ),
        migrations.AddField(
            model_name='claim',
            name='documents',
            field=models.ManyToManyField(blank=True, to='accounts.Document'),
        ),
        migrations.AlterField(
            model_name='period',
            name='application_type',
            field=models.CharField(choices=[('apos_regular', 'Ежемесячный АПОС'), ('apos_single', 'Единоразовый АПОС'), ('profilaktory', 'Профилакторий'), ('meals', 'Бесплатное питание')], max_length=30),
        ),
    ]
