from uuid import uuid4
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser  # 继承Django_AbstractUser用来扩展models
import shortuuid
# from .common import Common
# from dateutil.relativedelta import relativedelta
from django.utils.timezone import now, timedelta

image_file = uuid4().hex


# Create your models here.

class UserProFile(AbstractUser):
    '''
    用户表
    '''
    GENDER = {
        ("1", "男"),
        ("2", "女")
    }
    openid = models.CharField(max_length=200, default='', verbose_name='用户微信唯一ID')
    avatarUrl = models.URLField(max_length=500, default='', verbose_name='用户微信头像')
    country = models.CharField(max_length=100, default='', verbose_name='用户微信国家')
    province = models.CharField(max_length=100, default='', verbose_name='用户微信城市')
    city = models.CharField(max_length=100, default='', verbose_name='用户微信区域')
    language = models.CharField(max_length=100, default='', verbose_name='用户微信语言')
    background = models.ImageField(upload_to='media/UserProFilebg/%Y/%m/{imagess}'.format(imagess=image_file), null=True,
                                   blank=True,
                                   default='/default/default.jpg',
                                   verbose_name='背景图')
    nickName = models.CharField(max_length=20, verbose_name="微信用户名")
    name = models.CharField(max_length=20, verbose_name="用户名")
    birthay = models.DateField(default=datetime.now, verbose_name="出生日期")
    avatar = models.ImageField(upload_to='media/UserProFilebg/avatar/%y/%d/{image_file}'.format(image_file=image_file), null=True,
                               blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号")
    gender = models.CharField(max_length=10, choices=GENDER, default="1",
                              verbose_name="性别")
    thesignature = models.TextField(max_length=200, default='世界为你转身，因为你肯冒险！', verbose_name='用户签名')
    agreement = models.BooleanField(default=False, verbose_name='是否阅读协议')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="注册时间")

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


def createuuid():
    return shortuuid.uuid()


class Base(models.Model):
    del_state_type = ((0, '已删除'), (1, '默认'))
    uuid = models.CharField('ID', max_length=22, primary_key=True, default=createuuid, editable=False)
    add_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    del_state = models.IntegerField('删除状态', choices=del_state_type, default=1, db_index=True)

    class Meta:
        abstract = True


class User(Base):
    """用户表"""
    location_types = ((0, 'Suzhou'), (1, 'Shanghai'),)
    system_role_type = ((0, '普通用户'), (1, '管理员'),)
    name = models.CharField('姓名', max_length=50)
    password = models.CharField('密码', max_length=200)
    cellphone = models.CharField('手机号', max_length=15, blank=True, null=True)
    email = models.CharField('邮箱', max_length=50, blank=True, null=True)
    wechat_name = models.CharField('微信名', max_length=50)
    system_role = models.IntegerField('系统角色', choices=system_role_type, default=0)
    school = models.CharField('学校', max_length=200, blank=True, null=True)
    grade = models.CharField('多少届', max_length=30, blank=True, null=True)
    wechat_user = models.OneToOneField(UserProFile, verbose_name='微信用户', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

