import os
import sys
import requests
import datetime
from PIL import Image
from io import BytesIO
from rest_framework import status
from rest_framework import mixins
from django.shortcuts import render
from rest_framework import authentication
from rest_framework import views, viewsets
from rest_framework.response import Response

from utils.weixin_util.weixin import WXAPPAPI
from utils.permissions import IsOwnerOrReadOnly  # 登陆验证
from rest_framework.mixins import CreateModelMixin
from django.contrib.auth.backends import ModelBackend
from rest_framework.permissions import IsAuthenticated  # 登陆验证
from rest_framework_jwt.views import JSONWebTokenAPIView  # 重写jwt的认证
from utils.weixin_util.weixin.lib.wxcrypt import WXBizDataCrypt
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer
)
from rest_framework_jwt.settings import api_settings
from yuanban_end.sys_info import MINI_APP_ID, MINI_APP_SECRET
from ielts.models import ieltsModel
from yuanban_end.settings import BASE_DIR
from yuanban_end.settings import IMAGES_URL
from users.models import UserProFile
#from users.Serializers import UserRegSerializer

now = datetime.datetime.now()

class createieltsdetailinfo(views.APIView):
    '''
    雅思信息
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    def post(self,request):
        try:
            datechoice = request.data('riqi_index')
            if(datachoice == 0):
                date = datetime.datetime.now().strftime("%Y-%m-%d") 
                delaystatus = False
            elif(datachoice == 1):
                date = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
                delaystatus = True
            elif(datachoice == 2):
                date = (datetime.datetime.now()+datetime.timedelta(days=-2)).strftime("%Y-%m-%d")
                delaystatus = True
            userid = request.data('username')
            wordnumber =  request.data('wordnumber')
            readpercent = request.data('readpercent')
            listenpercent = request.data('listenpercent')
            #雅思单词图片组
            ieltswordPicset = request.data('upImgArr')
            ieltswordPath = os.path.join(BASE_DIR, 'upload/ielts/word/')
            #雅思阅读图片组
            ieltsreadPicset = request.data('upImgArr_read')
            ieltsreadPath = os.path.join(BASE_DIR, 'upload/ielts/read/')
            #雅思写作图片组
            ieltswritePicset = request.data('upImg_write')
            ieltswritePath = os.path.join(BASE_DIR, 'upload/ielts/write/')
            #雅思听力图片组
            ieltslistenPicset = request.data('upImgArr_listen')
            ieltslistenPath = os.path.join(BASE_DIR, 'upload/ielts/listen/')
            #雅思口语图片组
            ieltsspeakPicset = request.data('upImgArr_speak')
            ieltsspeakPath = os.path.join(BASE_DIR, 'upload/ielts/speak/')
            
            ieltsdetail = ieltsModel()
            user = User.objects.get(username=userid)
            
            ieltsdetail.user = user
            ieltsdetail.signdate = date
            ieltsdetail.buqianstatus = delaystatus
            ieltsdetail.wordnumber = wordnumber
            ieltsdetail.readpercent = readpercent
            ieltsdetail.listenpercent = listenpercent
            index_word = 0
            for item in ieltswordPicset:
                index_word += 1
                ieltswordname = ieltswordPath + date + index + userid + ".png"
                image = Image.open(BytesIO(item.content))
                image.save(ieltswordname)
                ieltsdetail.wordimageset = item

            index_read = 0
            for item in ieltsreadPicset:
                index_read += 1
                ieltsreadname = ieltsreadPath + date + index + userid + ".png"
                image = Image.open(BytesIO(item.content))
                image.save(ieltsreadname) 
                ieltsdetail.readimageset = item

            index_write = 0
            for item in ieltswritePicset:
                index_write += 1
                ieltswritename = ieltswritePath + date + index + userid + ".png"
                image = Image.open(BytesIO(item.content))
                image.save(ieltswritename) 
                ieltsdetail.writeimageset = item

            index_listen = 0
            for item in ieltslistenPicset:
                index_listen += 1
                ieltslistenname = ieltslistenPath + date + index + userid + ".png"
                image = Image.open(BytesIO(item.content))
                image.save(ieltslistenname) 
                ieltsdetail.listenimageset = item

            index_speak = 0
            for item in ieltsspeakPicset:
                index_speak += 1
                ieltsspeakname = ieltsspeakPath + date + index + userid + ".png"
                image = Image.open(BytesIO(item.content))
                image.save(ieltsspeakname) 
                ieltsdetail.speakimageset = item

            ieltsdetail.save()

            



        except:
            return JsonResponse(self.msg(20000))
        else:
            return JsonResponse(self.msg(10000, info))


            


