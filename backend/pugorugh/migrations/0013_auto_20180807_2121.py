# Generated by Django 2.0.6 on 2018-08-07 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0012_auto_20180807_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdog',
            name='status',
            field=models.CharField(default='u', max_length=1),
        ),
    ]