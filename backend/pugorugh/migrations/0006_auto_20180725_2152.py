# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-25 21:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0005_auto_20180725_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdog',
            name='dog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relation', to='pugorugh.Dog'),
        ),
        migrations.AlterField(
            model_name='userdog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='age',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='gender',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='size',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
