# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-25 14:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0004_auto_20180724_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='users',
            field=models.ManyToManyField(null=True, through='pugorugh.UserDog', to=settings.AUTH_USER_MODEL),
        ),
    ]
