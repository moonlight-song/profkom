# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-13 10:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_vkpost_new_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vkpost',
            name='new_field',
        ),
    ]