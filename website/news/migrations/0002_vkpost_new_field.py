# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-13 10:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vkpost',
            name='new_field',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
