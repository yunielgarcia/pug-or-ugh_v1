# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-30 14:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0007_auto_20180730_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpref',
            name='age',
            field=models.CharField(default='b', max_length=255),
        ),
    ]
