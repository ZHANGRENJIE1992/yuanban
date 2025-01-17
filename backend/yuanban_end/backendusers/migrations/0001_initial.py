# Generated by Django 2.2.7 on 2020-02-11 10:26

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('openid', models.CharField(default='', max_length=200, verbose_name='用户微信唯一ID')),
                ('avatarUrl', models.URLField(default='', max_length=500, verbose_name='用户微信头像')),
                ('country', models.CharField(default='', max_length=100, verbose_name='用户微信国家')),
                ('user_bh', models.CharField(default='fd0d3b0df7d240d1b6156f91defb346e', max_length=50, unique=True, verbose_name='用户唯一ID')),
                ('province', models.CharField(default='', max_length=100, verbose_name='用户微信城市')),
                ('city', models.CharField(default='', max_length=100, verbose_name='用户微信区域')),
                ('language', models.CharField(default='', max_length=100, verbose_name='用户微信语言')),
                ('background', models.ImageField(blank=True, default='/default/default.jpg', null=True, upload_to='UserProFilebg/%Y/%m/7fe4f72590014ea087ebb56a650ebe88', verbose_name='背景图')),
                ('nickName', models.CharField(max_length=20, verbose_name='微信用户名')),
                ('name', models.CharField(max_length=20, verbose_name='用户名')),
                ('birthay', models.DateField(default=datetime.datetime.now, verbose_name='出生日期')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='UserProFilebg/avatar/%y/%d/7fe4f72590014ea087ebb56a650ebe88')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, verbose_name='手机号')),
                ('gender', models.CharField(choices=[('1', '男'), ('2', '女')], default='1', max_length=10, verbose_name='性别')),
                ('thesignature', models.TextField(default='世界为你转身，因为你肯冒险！', max_length=200, verbose_name='用户签名')),
                ('agreement', models.BooleanField(default=False, verbose_name='是否阅读协议')),
                ('email', models.EmailField(blank=True, max_length=100, null=True, verbose_name='邮箱')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='注册时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户管理',
                'verbose_name_plural': '用户管理',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
