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
import base64
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
            datechoice = int(request.data['riqi_index'])
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
            # ieltswordPath = os.path.join(BASE_DIR, 'media/upload/ielts/word/')
            ieltswordPath = 'upload/ielts/word/'
            # 雅思阅读图片组
            ieltsreadPicset = request.data['upImgArr_read']
            ieltsreadPath = 'upload/ielts/read/'
            # 雅思写作图片组
            ieltswritePicset = request.data['upImgArr_write']
            ieltswritePath = 'upload/ielts/write/'
            # 雅思听力图片组
            ieltslistenPicset = request.data['upImgArr_listen']
            ieltslistenPath = 'upload/ielts/listen/'
            # 雅思口语图片组
            ieltsspeakPicset = request.data['upImgArr_speak']
            ieltsspeakPath = 'upload/ielts/speak/'

            ieltsdetail = ieltsModel()
            user = UserProFile.objects.get(username=userid)
            print(date)
            ieltsdetail.user = user
            ieltsdetail.signdate = date
            ieltsdetail.buqianstatus = delaystatus
            ieltsdetail.wordnumber = wordnumber
            ieltsdetail.readpercent = readpercent
            ieltsdetail.listenpercent = listenpercent
            wordimageset = []
            for item in ieltswordPicset:
                ieltswordname = ieltswordPath + createuuid() + ".png"
                # image = Image.open(BytesIO(item.content))
                # image = Image.open(item['base64'])
                imgdata = base64.b64decode(item['base64'])
                impath = os.path.join(BASE_DIR, 'media/', ieltswordname)
                file = open(impath, 'wb')
                file.write(imgdata)
                file.close()
                # print(555)
                # print(type(image))
                # image.save(ieltswordname)
                wordimageset.append(ieltswordname)
            if wordimageset:
                if len(wordimageset) == 1:
                    ieltsdetail.wordimageset = wordimageset[0]
                else:
                    ieltsdetail.wordimageset = ','.join(wordimageset)
            else:
                    ieltsdetail.wordimageset = ''

            readimageset = []
            for item in ieltsreadPicset:
                ieltsreadname = ieltsreadPath + createuuid() + ".png"
                imgdata = base64.b64decode(item['base64'])
                impath = os.path.join(BASE_DIR, 'media/', ieltsreadname)
                file = open(impath, 'wb')
                file.write(imgdata)
                file.close()
                readimageset.append(ieltsreadname)
            # ieltsdetail.readimageset = ','.join(readimageset)
            if readimageset:
                if len(readimageset) == 1:
                    ieltsdetail.readimageset = readimageset[0]
                else:
                    ieltsdetail.readimageset = ','.join(readimageset)
            else:
                ieltsdetail.readimageset = ''

            writeimageset = []
            for item in ieltswritePicset:
                ieltswritename = ieltswritePath + createuuid() + ".png"
                imgdata = base64.b64decode(item['base64'])
                impath = os.path.join(BASE_DIR, 'media/', ieltswritename)
                file = open(impath, 'wb')
                file.write(imgdata)
                file.close()
                writeimageset.append(ieltswritename)
            if writeimageset:
                if len(writeimageset) == 1:
                    ieltsdetail.writeimageset = writeimageset[0]
                else:
                    ieltsdetail.writeimageset = ','.join(writeimageset)
            else:
                ieltsdetail.writeimageset = ''

            listenimageset = []
            for item in ieltslistenPicset:
                ieltslistenname = ieltslistenPath + createuuid() + ".png"
                imgdata = base64.b64decode(item['base64'])
                impath = os.path.join(BASE_DIR, 'media/', ieltslistenname)
                file = open(impath, 'wb')
                file.write(imgdata)
                file.close()
                listenimageset.append(ieltslistenname)
            if listenimageset:
                if len(listenimageset) == 1:
                    ieltsdetail.listenimageset = listenimageset[0]
                else:
                    ieltsdetail.listenimageset = ','.join(listenimageset)
            else:
                ieltsdetail.listenimageset = ''
            speakimageset = []
            for item in ieltsspeakPicset:
                ieltsspeakname = ieltsspeakPath + createuuid() + ".png"
                imgdata = base64.b64decode(item['base64'])
                impath = os.path.join(BASE_DIR, 'media/', ieltsspeakname)
                file = open(impath, 'wb')
                file.write(imgdata)
                file.close()
                speakimageset.append(ieltsspeakname)
            if speakimageset:
                if len(speakimageset) == 1:
                    ieltsdetail.speakimageset = speakimageset[0]
                else:
                    ieltsdetail.speakimageset = ','.join(speakimageset)
            else:
                ieltsdetail.speakimageset = ''

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






