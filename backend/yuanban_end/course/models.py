from uuid import uuid4
from django.db import models
import datetime
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
    signdate = models.DateField(default=datetime.date.today(), verbose_name='打卡时间')
    buqianstatus = models.BooleanField(default=False, verbose_name='是否补签')
    wordnumber = models.IntegerField(default=0, verbose_name='单词背诵数量')
    readpercent = models.IntegerField(default=0, verbose_name='阅读正确率')
    listenpercent = models.IntegerField(default=0, verbose_name='听力正确率')
    wordimageset = models.TextField(null=True, blank=True, verbose_name='单词图片')
    readimageset = models.TextField(null=True, blank=True, verbose_name='阅读图片')
    writeimageset = models.TextField(null=True, blank=True, verbose_name='写作图片')
    listenimageset = models.TextField(null=True, blank=True, verbose_name='听力图片')
    speakimageset = models.TextField(null=True, blank=True, verbose_name='口语图片')

    class Meta:
        verbose_name = '雅思打卡'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.name + self.signdate

