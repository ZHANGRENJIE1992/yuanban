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
from django.http import JsonResponse
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
from .models import ieltsModel
from yuanban_end.settings import BASE_DIR
from yuanban_end.settings import IMAGES_URL
from backendusers.models import UserProFile
import shortuuid
import traceback
# from users.Serializers import UserRegSerializer

now = datetime.datetime.now()


def createuuid():
    return shortuuid.uuid()

class createieltsdetailinfo(views.APIView):
    '''
    雅思信息
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def post(self, request):
        try:
            datechoice = request.data['riqi_index']
            print(request.data)
            # if (datechoice == 0):
            date = datetime.date.today()
            delaystatus = False
            if (datechoice == 1):
                date = datetime.date.today() + datetime.timedelta(days=-1)
                delaystatus = True
            elif (datechoice == 2):
                date = datetime.date.today() + datetime.timedelta(days=-2)
                delaystatus = True
            userid = request.data['username']
            wordnumber = request.data['new_danci']
            readpercent = request.data['new_read']
            listenpercent = request.data['new_listen']
            print(listenpercent)
            # 雅思单词图片组
            ieltswordPicset = request.data['upImgArr']
            print(ieltswordPicset)
            ieltswordPath = os.path.join(BASE_DIR, 'upload/ielts/word/')
            # 雅思阅读图片组
            ieltsreadPicset = request.data['upImgArr_read']
            ieltsreadPath = os.path.join(BASE_DIR, 'upload/ielts/read/')
            # 雅思写作图片组
            ieltswritePicset = request.data['upImgArr_write']
            ieltswritePath = os.path.join(BASE_DIR, 'upload/ielts/write/')
            # 雅思听力图片组
            ieltslistenPicset = request.data['upImgArr_listen']
            ieltslistenPath = os.path.join(BASE_DIR, 'upload/ielts/listen/')
            # 雅思口语图片组
            ieltsspeakPicset = request.data['upImgArr_speak']
            ieltsspeakPath = os.path.join(BASE_DIR, 'upload/ielts/speak/')

            ieltsdetail = ieltsModel()
            user = UserProFile.objects.get(username=userid)

            ieltsdetail.user = user
            ieltsdetail.signdate = date
            ieltsdetail.buqianstatus = delaystatus
            ieltsdetail.wordnumber = wordnumber
            ieltsdetail.readpercent = readpercent
            ieltsdetail.listenpercent = listenpercent
            wordimageset = ''
            for item in ieltswordPicset:
                ieltswordname = ieltswordPath + createuuid() + ".png"
                # image = Image.open(BytesIO(item.content))
                image = Image.open(item['path'])
                print(555)
                print(type(image))
                image.save(ieltswordname)
                wordimageset = wordimageset + ',' + ieltswordname
            ieltsdetail.wordimageset = wordimageset

            readimageset = ''
            for item in ieltsreadPicset:
                ieltsreadname = ieltsreadPath + createuuid() + ".png"
                # image = Image.open(BytesIO(item.content))
                image = Image.open(item['path'])
                image.save(ieltsreadname)
                readimageset = readimageset + ',' + ieltsreadname
            ieltsdetail.readimageset = readimageset

            writeimageset = ''
            for item in ieltswritePicset:
                ieltswritename = ieltswritePath + createuuid() + ".png"
                # image = Image.open(BytesIO(item.content))
                image = Image.open(item['path'])
                image.save(ieltswritename)
                writeimageset = writeimageset + ',' + ieltswritename
            ieltsdetail.writeimageset = writeimageset

            listenimageset = ''
            for item in ieltslistenPicset:
                ieltslistenname = ieltslistenPath + createuuid() + ".png"
                # image = Image.open(BytesIO(item.content))
                image = Image.open(item['path'])
                image.save(ieltslistenname)
                listenimageset = listenimageset + ',' + ieltslistenname
            ieltsdetail.listenimageset = listenimageset

            speakimageset = ''
            for item in ieltsspeakPicset:
                ieltsspeakname = ieltsspeakPath + + createuuid() + ".png"
                # image = Image.open(BytesIO(item.content))
                image = Image.open(item['path'])
                image.save(ieltsspeakname)
                speakimageset = speakimageset + ',' + ieltsspeakname
            ieltsdetail.speakimageset = speakimageset

            ieltsdetail.save()
        except Exception as e:
            # print(e)
            # print("20000")
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # print('e.message:\t', e.message)
            print('traceback.print_exc():', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            print("10000")
            return Response(status=status.HTTP_201_CREATED)






