# Generated by Django 3.0.4 on 2020-05-15 14:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_auto_20200314_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gmatmodel',
            name='signdate',
            field=models.DateField(default=datetime.date(2020, 5, 15), verbose_name='打卡时间'),
        ),
        migrations.AlterField(
            model_name='gremodel',
            name='signdate',
            field=models.DateField(default=datetime.date(2020, 5, 15), verbose_name='打卡时间'),
        ),
        migrations.AlterField(
            model_name='ieltsmodel',
            name='signdate',
            field=models.DateField(default=datetime.date(2020, 5, 15), verbose_name='打卡时间'),
        ),
        migrations.AlterField(
            model_name='toeflmodel',
            name='signdate',
            field=models.DateField(default=datetime.date(2020, 5, 15), verbose_name='打卡时间'),
        ),
    ]
