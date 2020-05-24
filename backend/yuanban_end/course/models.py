from uuid import uuid4
from django.db import models
import datetime
from django.contrib.auth import get_user_model  # 继承Django_AbstractUser用来扩展models
from backendusers.models import UserProFile
USER = get_user_model()
image_file = uuid4().hex


# Create your models here.
from django.apps import apps


def getmodelfield(appname,modelname,exclude):
    """
    获取model的verbose_name和name的字段
    """
    modelobj = apps.get_model(appname, modelname)
    filed = modelobj._meta.fields
    print(filed)
    fielddic = {}

    params = [f for f in filed if f.name not in exclude]

    for i in params:
        fielddic[i.name] = i.verbose_name
    return fielddic


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

    @staticmethod
    def ver_name():
        exclude = []
        name_dict = getmodelfield('course', 'ieltsModel', exclude)
        return name_dict


class toeflModel(models.Model):
    '''
    托福
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
        verbose_name = '托福打卡'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.name + self.signdate

    @staticmethod
    def ver_name():
        exclude = []
        name_dict = getmodelfield('course', 'toeflModel', exclude)
        return name_dict


class greModel(models.Model):
    '''
    gre
    '''
    user = models.ForeignKey(UserProFile, verbose_name='用户', on_delete=models.CASCADE)
    signdate = models.DateField(default=datetime.date.today(), verbose_name='打卡时间')
    buqianstatus = models.BooleanField(default=False, verbose_name='是否补签')
    wordnumber = models.IntegerField(default=0, verbose_name='单词背诵数量')
    fill_blank_number = models.IntegerField(default=0, verbose_name='填空题正确率')
    readpercent = models.IntegerField(default=0, verbose_name='阅读正确率')
    mathpercent = models.IntegerField(default=0, verbose_name='数学正确率')
    wordimageset = models.TextField(null=True, blank=True, verbose_name='单词图片')
    readimageset = models.TextField(null=True, blank=True, verbose_name='阅读图片')
    writeimageset = models.TextField(null=True, blank=True, verbose_name='写作图片')
    mathimageset = models.TextField(null=True, blank=True, verbose_name='数学图片')
    fill_blank_imageset = models.TextField(null=True, blank=True, verbose_name='填空图片')

    class Meta:
        verbose_name = 'gre打卡'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.name + self.signdate

    @staticmethod
    def ver_name():
        exclude = []
        name_dict = getmodelfield('course', 'greModel', exclude)
        return name_dict


class gmatModel(models.Model):
    '''
    gmat
    '''
    user = models.ForeignKey(UserProFile, verbose_name='用户', on_delete=models.CASCADE)
    signdate = models.DateField(default=datetime.date.today(), verbose_name='打卡时间')
    buqianstatus = models.BooleanField(default=False, verbose_name='是否补签')
    wordnumber = models.IntegerField(default=0, verbose_name='单词背诵数量')
    grammarnumber = models.IntegerField(default=0, verbose_name='语法正确率')
    readpercent = models.IntegerField(default=0, verbose_name='阅读正确率')
    mathpercent = models.IntegerField(default=0, verbose_name='数学正确率')
    logicpercent = models.IntegerField(default=0, verbose_name='逻辑正确率')
    wordimageset = models.TextField(null=True, blank=True, verbose_name='单词图片')
    readimageset = models.TextField(null=True, blank=True, verbose_name='阅读图片')
    grammarimageset = models.TextField(null=True, blank=True, verbose_name='语法图片')
    writeimageset = models.TextField(null=True, blank=True, verbose_name='写作图片')
    mathimageset = models.TextField(null=True, blank=True, verbose_name='数学图片')
    logicimageset = models.TextField(null=True, blank=True, verbose_name='逻辑图片')

    class Meta:
        verbose_name = 'gmat打卡'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.name + self.signdate

    @staticmethod
    def ver_name():
        exclude = []
        name_dict = getmodelfield('course', 'gmatModel', exclude)
        return name_dict
