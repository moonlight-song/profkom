# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-20 10:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20180920_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='name',
            field=models.CharField(default='FileName', max_length=128),
            preserve_default=False,
        ),
    ]
