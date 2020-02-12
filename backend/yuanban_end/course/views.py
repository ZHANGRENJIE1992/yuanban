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
from .models import ieltsModel, toeflModel, greModel, gmatModel
from yuanban_end.settings import BASE_DIR
from yuanban_end.settings import IMAGES_URL, MEDIA_URL
from backendusers.models import UserProFile
import shortuuid
import traceback
import base64
import calendar
# from users.Serializers import UserRegSerializer

now = datetime.datetime.now()


def createuuid():
    return shortuuid.uuid()


def create_course(data, mold):
    datechoice = int(data['riqi_index'])
    date = datetime.date.today()
    delaystatus = False
    if (datechoice == 1):
        date = datetime.date.today() + datetime.timedelta(days=-1)
        delaystatus = True
    elif (datechoice == 2):
        date = datetime.date.today() + datetime.timedelta(days=-2)
        delaystatus = True
    userid = data['username']
    wordnumber = data['new_danci']
    readpercent = data['new_read']
    listenpercent = data['new_listen']
    print(listenpercent)
    if mold == 1:
        # 雅思单词图片组
        ieltswordPicset = data['upImgArr']
        print(ieltswordPicset)
        ieltswordPath = 'upload/ielts/word/'
        # 雅思阅读图片组
        ieltsreadPicset = data['upImgArr_read']
        ieltsreadPath = 'upload/ielts/read/'
        # 雅思写作图片组
        ieltswritePicset = data['upImgArr_write']
        ieltswritePath = 'upload/ielts/write/'
        # 雅思听力图片组
        ieltslistenPicset = data['upImgArr_listen']
        ieltslistenPath = 'upload/ielts/listen/'
        # 雅思口语图片组
        ieltsspeakPicset = data['upImgArr_speak']
        ieltsspeakPath = 'upload/ielts/speak/'

        user = UserProFile.objects.get(username=userid)
        print(date)
        older = ieltsModel.objects.filter(user=user, signdate=date)
        if older:
            ieltsdetail = older[0]
        else:
            ieltsdetail = ieltsModel()
    else:
        # 雅思单词图片组
        ieltswordPicset = data['upImgArr']
        print(ieltswordPicset)
        ieltswordPath = 'upload/toefl/word/'
        # 雅思阅读图片组
        ieltsreadPicset = data['upImgArr_read']
        ieltsreadPath = 'upload/toefl/read/'
        # 雅思写作图片组
        ieltswritePicset = data['upImgArr_write']
        ieltswritePath = 'upload/toefl/write/'
        # 雅思听力图片组
        ieltslistenPicset = data['upImgArr_listen']
        ieltslistenPath = 'upload/toefl/listen/'
        # 雅思口语图片组
        ieltsspeakPicset = data['upImgArr_speak']
        ieltsspeakPath = 'upload/toefl/speak/'

        user = UserProFile.objects.get(username=userid)
        print(date)
        older = toeflModel.objects.filter(user=user, signdate=date)
        if older:
            ieltsdetail = older[0]
        else:
            ieltsdetail = toeflModel()
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
    return True


class createieltsdetailinfo(views.APIView):
    '''
    雅思信息
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def post(self, request):
        try:
            create_course(data=request.data, mold=1)
            # datechoice = int(request.data['riqi_index'])
            # print(request.data)
            # # if (datechoice == 0):
            # date = datetime.date.today()
            # delaystatus = False
            # if (datechoice == 1):
            #     date = datetime.date.today() + datetime.timedelta(days=-1)
            #     delaystatus = True
            # elif (datechoice == 2):
            #     date = datetime.date.today() + datetime.timedelta(days=-2)
            #     delaystatus = True
            # userid = request.data['username']
            # wordnumber = request.data['new_danci']
            # readpercent = request.data['new_read']
            # listenpercent = request.data['new_listen']
            # print(listenpercent)
            # # 雅思单词图片组
            # ieltswordPicset = request.data['upImgArr']
            # print(ieltswordPicset)
            # # ieltswordPath = os.path.join(BASE_DIR, 'media/upload/ielts/word/')
            # ieltswordPath = 'upload/ielts/word/'
            # # 雅思阅读图片组
            # ieltsreadPicset = request.data['upImgArr_read']
            # ieltsreadPath = 'upload/ielts/read/'
            # # 雅思写作图片组
            # ieltswritePicset = request.data['upImgArr_write']
            # ieltswritePath = 'upload/ielts/write/'
            # # 雅思听力图片组
            # ieltslistenPicset = request.data['upImgArr_listen']
            # ieltslistenPath = 'upload/ielts/listen/'
            # # 雅思口语图片组
            # ieltsspeakPicset = request.data['upImgArr_speak']
            # ieltsspeakPath = 'upload/ielts/speak/'
            #
            # user = UserProFile.objects.get(username=userid)
            # print(date)
            # older = ieltsModel.objects.filter(user=user, signdate=date)
            # if older:
            #     ieltsdetail = older[0]
            # else:
            #     ieltsdetail = ieltsModel()
            # ieltsdetail.user = user
            # ieltsdetail.signdate = date
            # ieltsdetail.buqianstatus = delaystatus
            # ieltsdetail.wordnumber = wordnumber
            # ieltsdetail.readpercent = readpercent
            # ieltsdetail.listenpercent = listenpercent
            # wordimageset = []
            # for item in ieltswordPicset:
            #     ieltswordname = ieltswordPath + createuuid() + ".png"
            #     # image = Image.open(BytesIO(item.content))
            #     # image = Image.open(item['base64'])
            #     imgdata = base64.b64decode(item['base64'])
            #     impath = os.path.join(BASE_DIR, 'media/', ieltswordname)
            #     file = open(impath, 'wb')
            #     file.write(imgdata)
            #     file.close()
            #     # print(555)
            #     # print(type(image))
            #     # image.save(ieltswordname)
            #     wordimageset.append(ieltswordname)
            # if wordimageset:
            #     if len(wordimageset) == 1:
            #         ieltsdetail.wordimageset = wordimageset[0]
            #     else:
            #         ieltsdetail.wordimageset = ','.join(wordimageset)
            # else:
            #         ieltsdetail.wordimageset = ''
            #
            # readimageset = []
            # for item in ieltsreadPicset:
            #     ieltsreadname = ieltsreadPath + createuuid() + ".png"
            #     imgdata = base64.b64decode(item['base64'])
            #     impath = os.path.join(BASE_DIR, 'media/', ieltsreadname)
            #     file = open(impath, 'wb')
            #     file.write(imgdata)
            #     file.close()
            #     readimageset.append(ieltsreadname)
            # # ieltsdetail.readimageset = ','.join(readimageset)
            # if readimageset:
            #     if len(readimageset) == 1:
            #         ieltsdetail.readimageset = readimageset[0]
            #     else:
            #         ieltsdetail.readimageset = ','.join(readimageset)
            # else:
            #     ieltsdetail.readimageset = ''
            #
            # writeimageset = []
            # for item in ieltswritePicset:
            #     ieltswritename = ieltswritePath + createuuid() + ".png"
            #     imgdata = base64.b64decode(item['base64'])
            #     impath = os.path.join(BASE_DIR, 'media/', ieltswritename)
            #     file = open(impath, 'wb')
            #     file.write(imgdata)
            #     file.close()
            #     writeimageset.append(ieltswritename)
            # if writeimageset:
            #     if len(writeimageset) == 1:
            #         ieltsdetail.writeimageset = writeimageset[0]
            #     else:
            #         ieltsdetail.writeimageset = ','.join(writeimageset)
            # else:
            #     ieltsdetail.writeimageset = ''
            #
            # listenimageset = []
            # for item in ieltslistenPicset:
            #     ieltslistenname = ieltslistenPath + createuuid() + ".png"
            #     imgdata = base64.b64decode(item['base64'])
            #     impath = os.path.join(BASE_DIR, 'media/', ieltslistenname)
            #     file = open(impath, 'wb')
            #     file.write(imgdata)
            #     file.close()
            #     listenimageset.append(ieltslistenname)
            # if listenimageset:
            #     if len(listenimageset) == 1:
            #         ieltsdetail.listenimageset = listenimageset[0]
            #     else:
            #         ieltsdetail.listenimageset = ','.join(listenimageset)
            # else:
            #     ieltsdetail.listenimageset = ''
            # speakimageset = []
            # for item in ieltsspeakPicset:
            #     ieltsspeakname = ieltsspeakPath + createuuid() + ".png"
            #     imgdata = base64.b64decode(item['base64'])
            #     impath = os.path.join(BASE_DIR, 'media/', ieltsspeakname)
            #     file = open(impath, 'wb')
            #     file.write(imgdata)
            #     file.close()
            #     speakimageset.append(ieltsspeakname)
            # if speakimageset:
            #     if len(speakimageset) == 1:
            #         ieltsdetail.speakimageset = speakimageset[0]
            #     else:
            #         ieltsdetail.speakimageset = ','.join(speakimageset)
            # else:
            #     ieltsdetail.speakimageset = ''
            #
            # ieltsdetail.save()
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


class createtoefldetailinfo(views.APIView):
    '''
    托福信息
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def post(self, request):
        try:
            create_course(data=request.data, mold=2)
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


class Getieltsdetailinfo(views.APIView):
    '''
    修改和获取打卡信息
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get(self, request):
        '''
        获取用户信息
        :param request:
        :return:
        '''
        dateinfo = request.data.get('date', None)
        user = self.request.user
        if not dateinfo:
            dateinfo = datetime.date.today()
        else:
            dateinfo = datetime.datetime.strptime(dateinfo, '%Y-%m-%d').date()
        ielts = ieltsModel.objects.get(user=user, signdate=dateinfo)
        ielts_info = {
            'new_danci': ielts.wordnumber,
            'new_read': ielts.readpercent,
            'new_listen': ielts.listenpercent,
            'upImgArr': [IMAGES_URL + MEDIA_URL + w for w in ielts.wordimageset],
            'upImgArr_read': [IMAGES_URL + MEDIA_URL + r for r in ielts.readimageset],
            'upImgArr_listen': [IMAGES_URL + MEDIA_URL + l for l in ielts.listenimageset],
            'upImgArr_write': [IMAGES_URL + MEDIA_URL + wr for wr in ielts.writeimageset],
            'upImgArr_speak': [IMAGES_URL + MEDIA_URL + s for s in ielts.speakimageset],
            'signdate': datetime.date.strftime(ielts.signdate, "%Y-%m-%d"),
            'buqianstatus': ielts.buqianstatus,
            'username': user.name
        }
        return Response(ielts_info, status=status.HTTP_200_OK)


class Gettoefldetailinfo(views.APIView):
    '''
    修改和获取打卡信息
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get(self, request):
        '''
        获取用户信息
        :param request:
        :return:
        '''
        dateinfo = request.data.get('date', None)
        user = self.request.user
        if not dateinfo:
            dateinfo = datetime.date.today()
        else:
            dateinfo = datetime.datetime.strptime(dateinfo, '%Y-%m-%d').date()
        ielts = toeflModel.objects.get(user=user, signdate=dateinfo)
        ielts_info = {
            'new_danci': ielts.wordnumber,
            'new_read': ielts.readpercent,
            'new_listen': ielts.listenpercent,
            'upImgArr': [IMAGES_URL + MEDIA_URL + w for w in ielts.wordimageset],
            'upImgArr_read': [IMAGES_URL + MEDIA_URL + r for r in ielts.readimageset],
            'upImgArr_listen': [IMAGES_URL + MEDIA_URL + l for l in ielts.listenimageset],
            'upImgArr_write': [IMAGES_URL + MEDIA_URL + wr for wr in ielts.writeimageset],
            'upImgArr_speak': [IMAGES_URL + MEDIA_URL + s for s in ielts.speakimageset],
            'signdate': datetime.date.strftime(ielts.signdate, "%Y-%m-%d"),
            'buqianstatus': ielts.buqianstatus,
            'username': user.name
        }
        return Response(ielts_info, status=status.HTTP_200_OK)


class GetIeltsList(views.APIView):
    '''
    修改和获取打卡周期信息
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get(self, request):
        user = self.request.user
        monthinfo = request.data.get('month', None)
        if not monthinfo:
            dateinfo = datetime.date.today()
            last = calendar.monthrange(dateinfo.year, dateinfo.month)[1]
        else:
            year, month = monthinfo.split('-')
            last = calendar.monthrange(year, month)[1]
            dateinfo = datetime.datetime.strptime(monthinfo, '%Y-%m').date()
        fistday = dateinfo.replace(day=1)
        lastday = dateinfo.replace(day=last)
        ies = ieltsModel.objects.filter(user=user, signdate__lte=lastday, signdate__gte=fistday)
        res = {}
        data = []
        for i in range(1, last+1):
            info = {
                'date': datetime.date.strftime((dateinfo.replace(day=i)), "%Y-%m-%d"),
                'sign': 0
                    }
            for row in ies:
                if row.signdate == dateinfo.replace(day=i):
                    info['sign'] = 1
                    break
            data.append(info)
        res['data'] = data
        res['type'] = 'ielts'

        return Response(res, status=status.HTTP_200_OK)


class GetToeflList(views.APIView):
    '''
    修改和获取打卡周期信息
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get(self, request):
        user = self.request.user
        monthinfo = request.data.get('month', None)
        if not monthinfo:
            dateinfo = datetime.date.today()
            last = calendar.monthrange(dateinfo.year, dateinfo.month)[1]
        else:
            year, month = monthinfo.split('-')
            last = calendar.monthrange(year, month)[1]
            dateinfo = datetime.datetime.strptime(monthinfo, '%Y-%m').date()
        fistday = dateinfo.replace(day=1)
        lastday = dateinfo.replace(day=last)
        ies = toeflModel.objects.filter(user=user, signdate__lte=lastday, signdate__gte=fistday)
        res = {}
        data = []
        for i in range(1, last+1):
            info = {
                'date': datetime.date.strftime((dateinfo.replace(day=i)), "%Y-%m-%d"),
                'sign': 0
                    }
            for row in ies:
                if row.signdate == dateinfo.replace(day=i):
                    info['sign'] = 1
                    break
            data.append(info)
        res['data'] = data
        res['type'] = 'toefl'

        return Response(res, status=status.HTTP_200_OK)


class creategredetailinfo(views.APIView):
    '''
    gre信息
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
            fill_blank_number = request.data['new_blank']
            readpercent = request.data['new_read']
            mathpercent = request.data['new_math']
            # 雅思单词图片组
            ieltswordPicset = request.data['upImgArr']
            print(ieltswordPicset)
            # ieltswordPath = os.path.join(BASE_DIR, 'media/upload/ielts/word/')
            ieltswordPath = 'upload/gre/word/'
            # 雅思阅读图片组
            ieltsreadPicset = request.data['upImgArr_read']
            ieltsreadPath = 'upload/gre/read/'
            # 雅思写作图片组
            ieltswritePicset = request.data['upImgArr_write']
            ieltswritePath = 'upload/gre/write/'
            # # 雅思听力图片组
            # ieltslistenPicset = request.data['upImgArr_listen']
            # ieltslistenPath = 'upload/gre/listen/'
            # 雅思口语图片组
            ieltsmathPicset = request.data['upImgArr_math']
            ieltsmathPath = 'upload/gre/math/'
            ieltsblankPicset = request.data['upImgArr_blank']
            ieltsblankPath = 'upload/gre/blank/'

            user = UserProFile.objects.get(username=userid)
            print(date)
            older = greModel.objects.filter(user=user, signdate=date)
            if older:
                ieltsdetail = older[0]
            else:
                ieltsdetail = greModel()
            ieltsdetail.user = user
            ieltsdetail.signdate = date
            ieltsdetail.buqianstatus = delaystatus
            ieltsdetail.wordnumber = wordnumber
            ieltsdetail.readpercent = readpercent
            ieltsdetail.fill_blank_number = fill_blank_number
            ieltsdetail.mathpercent = mathpercent
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
            # 数学照片
            mathimageset = []
            for item in ieltsmathPicset:
                ieltslistenname = ieltsmathPath + createuuid() + ".png"
                imgdata = base64.b64decode(item['base64'])
                impath = os.path.join(BASE_DIR, 'media/', ieltslistenname)
                file = open(impath, 'wb')
                file.write(imgdata)
                file.close()
                mathimageset.append(ieltslistenname)
            if mathimageset:
                if len(mathimageset) == 1:
                    ieltsdetail.mathimageset = mathimageset[0]
                else:
                    ieltsdetail.mathimageset = ','.join(mathimageset)
            else:
                ieltsdetail.mathimageset = ''
            # 填空照片
            fill_blank_imageset = []
            for item in ieltsblankPicset:
                ieltsspeakname = ieltsblankPath + createuuid() + ".png"
                imgdata = base64.b64decode(item['base64'])
                impath = os.path.join(BASE_DIR, 'media/', ieltsspeakname)
                file = open(impath, 'wb')
                file.write(imgdata)
                file.close()
                fill_blank_imageset.append(ieltsspeakname)
            if fill_blank_imageset:
                if len(fill_blank_imageset) == 1:
                    ieltsdetail.fill_blank_imageset = fill_blank_imageset[0]
                else:
                    ieltsdetail.fill_blank_imageset = ','.join(fill_blank_imageset)
            else:
                ieltsdetail.fill_blank_imageset = ''

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


class Getgredetailinfo(views.APIView):
    '''
    修改和获取打卡信息
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get(self, request):
        '''
        获取用户信息
        :param request:
        :return:
        '''
        dateinfo = request.data.get('date', None)
        user = self.request.user
        if not dateinfo:
            dateinfo = datetime.date.today()
        else:
            dateinfo = datetime.datetime.strptime(dateinfo, '%Y-%m-%d').date()
        ielts = greModel.objects.get(user=user, signdate=dateinfo)
        ielts_info = {
            'new_danci': ielts.wordnumber,
            'new_read': ielts.readpercent,
            'new_blank': ielts.fill_blank_number,
            'new_math': ielts.mathpercent,
            'upImgArr': [IMAGES_URL + MEDIA_URL + w for w in ielts.wordimageset],
            'upImgArr_read': [IMAGES_URL + MEDIA_URL + r for r in ielts.readimageset],
            'upImgArr_blank': [IMAGES_URL + MEDIA_URL + l for l in ielts.fill_blank_imageset],
            'upImgArr_write': [IMAGES_URL + MEDIA_URL + wr for wr in ielts.writeimageset],
            'upImgArr_math': [IMAGES_URL + MEDIA_URL + s for s in ielts.mathimageset],
            'signdate': datetime.date.strftime(ielts.signdate, "%Y-%m-%d"),
            'buqianstatus': ielts.buqianstatus,
            'username': user.name
        }
        return Response(ielts_info, status=status.HTTP_200_OK)


class GetGreList(views.APIView):
    '''
    修改和获取打卡周期信息
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get(self, request):
        user = self.request.user
        monthinfo = request.data.get('month', None)
        if not monthinfo:
            dateinfo = datetime.date.today()
            last = calendar.monthrange(dateinfo.year, dateinfo.month)[1]
        else:
            year, month = monthinfo.split('-')
            last = calendar.monthrange(year, month)[1]
            dateinfo = datetime.datetime.strptime(monthinfo, '%Y-%m').date()
        fistday = dateinfo.replace(day=1)
        lastday = dateinfo.replace(day=last)
        ies = greModel.objects.filter(user=user, signdate__lte=lastday, signdate__gte=fistday)
        res = {}
        data = []
        for i in range(1, last+1):
            info = {
                'date': datetime.date.strftime((dateinfo.replace(day=i)), "%Y-%m-%d"),
                'sign': 0
                    }
            for row in ies:
                if row.signdate == dateinfo.replace(day=i):
                    info['sign'] = 1
                    break
            data.append(info)
        res['data'] = data
        res['type'] = 'gre'

        return Response(res, status=status.HTTP_200_OK)


class creategmatdetailinfo(views.APIView):
    '''
    gmat信息
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
            grammarnumber = request.data['new_grammar']
            readpercent = request.data['new_read']
            mathpercent = request.data['new_math']
            logicpercent = request.data['new_logic']
            # 雅思单词图片组
            ieltswordPicset = request.data['upImgArr']
            print(ieltswordPicset)
            # ieltswordPath = os.path.join(BASE_DIR, 'media/upload/ielts/word/')
            ieltswordPath = 'upload/gmat/word/'
            # 雅思阅读图片组
            ieltsreadPicset = request.data['upImgArr_read']
            ieltsreadPath = 'upload/gmat/read/'
            # 雅思写作图片组
            ieltswritePicset = request.data['upImgArr_write']
            ieltswritePath = 'upload/gmat/write/'
            # 雅思听力图片组
            ieltslogicPicset = request.data['upImgArr_logic']
            ieltslogicPath = 'upload/gmat/logic/'
            # 雅思口语图片组
            ieltsmathPicset = request.data['upImgArr_math']
            ieltsmathPath = 'upload/gmat/math/'
            ieltsgrammarPicset = request.data['upImgArr_grammar']
            ieltsgrammarPath = 'upload/gmat/grammar/'

            user = UserProFile.objects.get(username=userid)
            print(date)
            older = gmatModel.objects.filter(user=user, signdate=date)
            if older:
                ieltsdetail = older[0]
            else:
                ieltsdetail = gmatModel()
            ieltsdetail.user = user
            ieltsdetail.signdate = date
            ieltsdetail.buqianstatus = delaystatus
            ieltsdetail.wordnumber = wordnumber
            ieltsdetail.readpercent = readpercent
            ieltsdetail.grammarnumber = grammarnumber
            ieltsdetail.mathpercent = mathpercent
            ieltsdetail.logicpercent = logicpercent
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
            # 数学照片
            mathimageset = []
            for item in ieltsmathPicset:
                ieltslistenname = ieltsmathPath + createuuid() + ".png"
                imgdata = base64.b64decode(item['base64'])
                impath = os.path.join(BASE_DIR, 'media/', ieltslistenname)
                file = open(impath, 'wb')
                file.write(imgdata)
                file.close()
                mathimageset.append(ieltslistenname)
            if mathimageset:
                if len(mathimageset) == 1:
                    ieltsdetail.mathimageset = mathimageset[0]
                else:
                    ieltsdetail.mathimageset = ','.join(mathimageset)
            else:
                ieltsdetail.mathimageset = ''
            # 逻辑照片
            logicimageset = []
            for item in ieltslogicPicset:
                ieltsspeakname = ieltslogicPath + createuuid() + ".png"
                imgdata = base64.b64decode(item['base64'])
                impath = os.path.join(BASE_DIR, 'media/', ieltsspeakname)
                file = open(impath, 'wb')
                file.write(imgdata)
                file.close()
                logicimageset.append(ieltsspeakname)
            if logicimageset:
                if len(logicimageset) == 1:
                    ieltsdetail.logicimageset = logicimageset[0]
                else:
                    ieltsdetail.logicimageset = ','.join(logicimageset)
            else:
                ieltsdetail.logicimageset = ''
            # 语法照片
            grammarimageset = []
            for item in ieltsgrammarPicset:
                ieltsspeakname = ieltsgrammarPath + createuuid() + ".png"
                imgdata = base64.b64decode(item['base64'])
                impath = os.path.join(BASE_DIR, 'media/', ieltsspeakname)
                file = open(impath, 'wb')
                file.write(imgdata)
                file.close()
                grammarimageset.append(ieltsspeakname)
            if grammarimageset:
                if len(grammarimageset) == 1:
                    ieltsdetail.grammarimageset = grammarimageset[0]
                else:
                    ieltsdetail.grammarimageset = ','.join(grammarimageset)
            else:
                ieltsdetail.grammarimageset = ''

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


class Getgmatdetailinfo(views.APIView):
    '''
    修改和获取打卡信息
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get(self, request):
        '''
        获取用户信息
        :param request:
        :return:
        '''
        dateinfo = request.data.get('date', None)
        user = self.request.user
        if not dateinfo:
            dateinfo = datetime.date.today()
        else:
            dateinfo = datetime.datetime.strptime(dateinfo, '%Y-%m-%d').date()
        ielts = gmatModel.objects.get(user=user, signdate=dateinfo)
        ielts_info = {
            'new_danci': ielts.wordnumber,
            'new_read': ielts.readpercent,
            'new_grammar': ielts.grammarnumber,
            'new_math': ielts.mathpercent,
            'new_logic': ielts.logicpercent,
            'upImgArr': [IMAGES_URL + MEDIA_URL + w for w in ielts.wordimageset],
            'upImgArr_read': [IMAGES_URL + MEDIA_URL + r for r in ielts.readimageset],
            'upImgArr_grammar': [IMAGES_URL + MEDIA_URL + l for l in ielts.grammarimageset],
            'upImgArr_write': [IMAGES_URL + MEDIA_URL + wr for wr in ielts.writeimageset],
            'upImgArr_math': [IMAGES_URL + MEDIA_URL + s for s in ielts.mathimageset],
            'upImgArr_logic': [IMAGES_URL + MEDIA_URL + s for s in ielts.logicimageset],
            'signdate': datetime.date.strftime(ielts.signdate, "%Y-%m-%d"),
            'buqianstatus': ielts.buqianstatus,
            'username': user.name
        }
        return Response(ielts_info, status=status.HTTP_200_OK)


class GetGmatList(views.APIView):
    '''
    修改和获取打卡周期信息
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get(self, request):
        user = self.request.user
        monthinfo = request.data.get('month', None)
        if not monthinfo:
            dateinfo = datetime.date.today()
            last = calendar.monthrange(dateinfo.year, dateinfo.month)[1]
        else:
            year, month = monthinfo.split('-')
            last = calendar.monthrange(year, month)[1]
            dateinfo = datetime.datetime.strptime(monthinfo, '%Y-%m').date()
        fistday = dateinfo.replace(day=1)
        lastday = dateinfo.replace(day=last)
        ies = gmatModel.objects.filter(user=user, signdate__lte=lastday, signdate__gte=fistday)
        res = {}
        data = []
        for i in range(1, last+1):
            info = {
                'date': datetime.date.strftime((dateinfo.replace(day=i)), "%Y-%m-%d"),
                'sign': 0
                    }
            for row in ies:
                if row.signdate == dateinfo.replace(day=i):
                    info['sign'] = 1
                    break
            data.append(info)
        res['data'] = data
        res['type'] = 'gmat'

        return Response(res, status=status.HTTP_200_OK)


