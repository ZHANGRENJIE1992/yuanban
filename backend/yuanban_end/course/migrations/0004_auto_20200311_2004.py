# Generated by Django 3.0.4 on 2020-03-11 12:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20200219_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gmatmodel',
            name='signdate',
            field=models.DateField(default=datetime.date(2020, 3, 11), verbose_name='打卡时间'),
        ),
        migrations.AlterField(
            model_name='gremodel',
            name='signdate',
            field=models.DateField(default=datetime.date(2020, 3, 11), verbose_name='打卡时间'),
        ),
        migrations.AlterField(
            model_name='ieltsmodel',
            name='signdate',
            field=models.DateField(default=datetime.date(2020, 3, 11), verbose_name='打卡时间'),
        ),
        migrations.AlterField(
            model_name='toeflmodel',
            name='signdate',
            field=models.DateField(default=datetime.date(2020, 3, 11), verbose_name='打卡时间'),
        ),
    ]
