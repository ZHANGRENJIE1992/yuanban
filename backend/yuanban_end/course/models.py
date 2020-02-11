from uuid import uuid4
from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model  # 继承Django_AbstractUser用来扩展models
from backendusers.models import UserProFile
USER = get_user_model()
image_file = uuid4().hex


# Create your models here.

class ieltsModel(models.Model):
    '''
    雅思
    '''
    user = models.ForeignKey(UserProFile, verbose_name='用户', on_delete=models.CASCADE)
    signdate = models.DateTimeField(default=datetime.now, verbose_name='打卡时间')
    buqianstatus = models.BooleanField(default=False, verbose_name='是否补签')
    wordnumber = models.IntegerField(default=0, verbose_name='单词背诵数量')
    readpercent = models.IntegerField(default=0, verbose_name='阅读正确率')
    listenpercent = models.IntegerField(default=0, verbose_name='听力正确率')
    wordimageset = models.ImageField(upload_to='ielts/%y/%m/%d/{{imagewordset}}',null=True,
                                    blank=True, verbose_name='单词图片')
    readimageset = models.ImageField(upload_to='ielts/%y/%m/%d/{{imagereadset}}',null=True,
                                    blank=True, verbose_name='阅读图片')
    writeimageset = models.ImageField(upload_to='ielts/%y/%m/%d/{{imagewriteset}}',null=True,
                                    blank=True, verbose_name='写作图片')
    listenimageset = models.ImageField(upload_to='ielts/%y/%m/%d/{{imagelistenset}}',null=True,
                                    blank=True, verbose_name='听力图片')
    speakimageset = models.ImageField(upload_to='ielts/%y/%m/%d/{{imagespeakset}}',null=True,
                                    blank=True, verbose_name='口语图片')



    '''GENDER = {
        ("1", "男"),
        ("2", "女")
    }
    openid = models.CharField(max_length=200, default='', verbose_name='用户微信唯一ID')
    avatarUrl = models.URLField(max_length=500, default='', verbose_name='用户微信头像')
    country = models.CharField(max_length=100, default='', verbose_name='用户微信国家')
    user_bh = models.CharField(max_length=50, default=uuid4().hex, unique=True, verbose_name='用户唯一ID')
    province = models.CharField(max_length=100, default='', verbose_name='用户微信城市')
    city = models.CharField(max_length=100, default='', verbose_name='用户微信区域')
    language = models.CharField(max_length=100, default='', verbose_name='用户微信语言')
    background = models.ImageField(upload_to='UserProFilebg/%Y/%m/{imagess}'.format(imagess=image_file), null=True,
                                   blank=True,
                                   default='/default/default.jpg',
                                   verbose_name='背景图')
    nickName = models.CharField(max_length=20, verbose_name="微信用户名")
    name = models.CharField(max_length=20, verbose_name="用户名")
    birthay = models.DateField(default=datetime.now, verbose_name="出生日期")
    avatar = models.ImageField(upload_to='UserProFilebg/avatar/%y/%d/{image_file}'.format(image_file=image_file), null=True,
                               blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号")
    gender = models.CharField(max_length=10, choices=GENDER, default="1",
                              verbose_name="性别")
    thesignature = models.TextField(max_length=200, default='世界为你转身，因为你肯冒险！', verbose_name='用户签名')
    agreement = models.BooleanField(default=False, verbose_name='是否阅读协议')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="注册时间")
'''
    class Meta:
        verbose_name = '雅思打卡'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.name

