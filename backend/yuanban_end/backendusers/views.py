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
from .models import UserProFile
from yuanban_end.settings import BASE_DIR
from yuanban_end.settings import IMAGES_URL,MEDIA_URL
from .Serializers import UserRegSerializer
from .user import User as UserCommon
from .common import Common
from djtool.views import SignOutView
from djtool.review import View, ListView
from .models import User
from django.http import JsonResponse
from course.models import *

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
encoding='unicode_escape'

# Create your views here.
class READJSONWebTokenAPIView(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        try:
            username = self.request.data

            api = WXAPPAPI(appid=MINI_APP_ID, app_secret=MINI_APP_SECRET)
            code = username['code']  # 获取到code
            session_info = api.exchange_code_for_session_key(code=code)
            session_key = session_info.get('session_key')
            crypt = WXBizDataCrypt(MINI_APP_ID, session_key)
            encrypted_data = username['username']  # 获取到encrypted_data
            iv = username['password']  # 获取到iv
            user_info = crypt.decrypt(encrypted_data, iv)  # 获取到用户的登陆信息

            # 获取用户的信息
            openid = user_info['openId']  # 获取openid
            avatarUrl = user_info['avatarUrl']  # 获取到头像
            nickName = user_info['nickName']  # 获取昵称
            # 找到用户更新用户的微信昵称和头像
            this_user = UserProFile.objects.filter(openid=openid)

            if this_user:
                this_user = this_user[0]
                this_user.avatarUrl = avatarUrl
                this_user.nickName = nickName
                # this_user.avatar = 'avatar/' + openid + '.png'
                this_user.save()

            username['username'] = openid
            username['password'] = openid
            del username['code']
        except:
            pass

        return {
            'request': self.request,
            'view': self,
        }

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainJSONWebToken(READJSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = JSONWebTokenSerializer


class CustomBackend(ModelBackend):
    '''
    '''

    def authenticate(self, request, username=None, password=None, **kwargs):
        '''
        :param request:
        :param username:
        :param password:
        :param kwargs:
        :return:
        '''
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class Registered(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    Registered
    '''

    serializer_class = UserRegSerializer
    queryset = UserProFile.objects.all()

    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # 认证

    def get_permissions(self):
        '''
        :return:
        '''
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []
        pass

    def create(self, request, *args, **kwargs):
        # print(request.data)
        # try:
        api = WXAPPAPI(appid=MINI_APP_ID, app_secret=MINI_APP_SECRET)
        code = request.data['code']  # 获取到code
        session_info = api.exchange_code_for_session_key(code=code)
        session_key = session_info.get('session_key')
        crypt = WXBizDataCrypt(MINI_APP_ID, session_key)
        encrypted_data = request.data['username']  # 获取到encrypted_data
        iv = request.data['password']  # 获取到iv
        user_info = crypt.decrypt(encrypted_data, iv)  # 获取到用户的登陆信息
        # 获取用户的信息
        openid = user_info['openId']  # 获取openid
        avatarUrl = user_info['avatarUrl']  # 获取头像
        country = user_info['country']  # 获取国家
        province = user_info['province']  # 获取城市
        city = user_info['city']  # 获取区域
        gender = user_info['gender']  # 获取性别
        language = user_info['language']  # 获取语言
        nickName = user_info['nickName']  # 获取昵称
        # 保存用户头像到本地
        avatarPath = os.path.join(BASE_DIR, 'media/upload/UserProFilebg/avatar/')
        avatarGet = requests.get(avatarUrl)
        avatar_name = avatarPath + openid + '.png'
        image = Image.open(BytesIO(avatarGet.content))
        image.save(avatar_name)
        # 判断用户是否存在
        if UserProFile.objects.filter(openid=openid):
            this_user = UserProFile.objects.filter(openid=openid)
            this_user.nickName = nickName  # 更新用户的微信昵称
            this_user.avatarUrl = avatarUrl  # 更新用户微信头像
            this_user.gender = str(gender)  # 更新用户的性别
            this_user.avatar = 'avatar/' + openid + '.png'
            this_user.update()
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            # 保存用户信息
            if len(nickName) > 6:
                nickName = nickName[0:6]
            user_info_save = UserProFile()
            user_info_save.openid = openid  # 保存用户openid
            user_info_save.avatarUrl = avatarUrl  # 保存用户微信头像
            user_info_save.country = country  # 保存用户所在的国家
            user_info_save.province = province  # 保存用户所在的城市
            user_info_save.city = city  # 保存用户所在的区域
            user_info_save.avatar = 'UserProFilebg/avatar/' + openid + '.png'
            user_info_save.gender = str(gender)  # 保存用户的性别
            user_info_save.language = language  # 保存用户当前使用的语言
            user_info_save.nickName = nickName  # 保存用户的微信昵称
            user_info_save.name = nickName  # 用户原始的用户名
            user_info_save.username = openid  # 保存用户的昵称
            user_info_save.password = make_password(openid)  # 保存用户的密码
            user_info_save.zhong_jifen = 0
            user_info_save.save()
        # except:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(status=status.HTTP_201_CREATED)

    def get_object(self):
        '''
        :return:
        '''
        return self.request.user

    def perform_create(self, serializer):
        '''
        :param serializer:
        :return:
        '''
        return serializer.save()


class GetUser(views.APIView):
    '''
    修改和获取用户的个人信息
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get(self, request):
        '''
        获取用户信息
        :param request:
        :return:
        '''
        name = self.request.user.name
        avatar = self.request.user.avatar
        thesignature = self.request.user.thesignature
        background = self.request.user.background
        gender = self.request.user.gender
        birthay = self.request.user.birthay
        nickName = self.request.user.nickName
        mobile = self.request.user.mobile
        username = self.request.user.username
        if gender == '1':
            gender = '男'
        else:
            gender = '女'
        user_info = {
            'name': name,
            'avatar': IMAGES_URL + MEDIA_URL + 'upload/' + str(avatar),
            'thesignature': thesignature,
            'gender': gender,
            'nickName': nickName,
            'mobile': mobile,
            'birthay': datetime.datetime.strftime(birthay, "%Y-%m-%d"),
            'background': IMAGES_URL + MEDIA_URL + 'upload/' + str(background),
            'username':username
        }
        return Response(user_info, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        '''
        修改用户个人信息
        :param request:
        :return:
        '''
        try:
            type = request.data['types']
        except:
            type = None
        # if (type != None) and (image_files != None):
        if type == 'GHTX':
            image_files = request.data['file']
            self.request.user.avatar = image_files
            self.request.user.save()
            return Response(status=status.HTTP_200_OK)
        elif type == 'GHBJ':
            image_files = request.data['file']
            print("打印:", image_files)
            self.request.user.background = image_files
            self.request.user.save()
            return Response(status=status.HTTP_200_OK)
        elif type == 'GHXB':
            self.request.user.gender = request.data['new_shengri']
            self.request.user.save()
            return Response(status=status.HTTP_200_OK)
        elif type == 'GHSRI':
            self.request.user.birthay = request.data['sr']
            self.request.user.save()
            return Response(status=status.HTTP_200_OK)
        elif type == 'GHNAME':
            name_all = UserProFile.objects.filter(name=request.data['new_name'])
            if name_all:
                return Response({'message': '昵称已存在'}, status=status.HTTP_202_ACCEPTED)
            self.request.user.name = request.data['new_name']
            self.request.user.save()
            return Response({'message': '昵称更改成功'}, status=status.HTTP_200_OK)
        elif type == 'GHPHONE':
            phone_all = UserProFile.objects.filter(mobile=request.data['new_phone'])
            if phone_all:
                return Response({'message': '手机号已存在'}, status=status.HTTP_202_ACCEPTED)
            self.request.user.mobile = request.data['new_phone']
            self.request.user.save()
            return Response({'message': '手机号已更换'}, status=status.HTTP_200_OK)
        elif type == 'thesignature':
            self.request.user.thesignature = request.data['new_thesignature']
            self.request.user.save()
            return Response({'message': '签名已更新'}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class CreateUserView(Common, View):

    def post(self, request, *args, **kwargs):
        try:
            data = request.POST
            assert data.get('name') and data.get('password') and data.get('wechat_name') and data.get('cellphone')
            print(33, data)
            name = data.get('name')
            password = data.get('password')
            cellphone = data.get('cellphone','')
            wechat_name = data.get('wechat_name')
            email = data.get('email')
            school = data.get('school')
            grade = data.get('grade')
            system_role = data.get('system_role',0)
            user = User.objects.get(uuid=request.session['login'], del_state=1)
            if data.get('belong_uuid'):
                print(333)
                belong = User.objects.get(uuid=data.get('belong_uuid'), del_state=1)
            else:
                belong = user
            if system_role == 1:
                belong = None
            if User.objects.filter(wechat_name=wechat_name, del_state=1).exists():
              return JsonResponse(self.msg(20000, remsg='用户已存在'))
            user = UserCommon()
            password = user.make_password(password)
            User.objects.create(
              name=name,
              password=password,
              wechat_name=wechat_name,
                school=school,
                grade=grade,
              cellphone=cellphone,
              email=email,
              system_role=system_role,
                belong=belong,
            )
        except Exception as e:
            print(e)
            return JsonResponse(self.msg(20000), status=status.HTTP_200_OK)
        else:
          return JsonResponse(self.msg(10000), status=status.HTTP_200_OK)


class AllTeacher(Common, ListView):

    def get(self, request, *args, **kwargs):
        users = User.objects.filter(del_state=1, system_role__in=[1, 2])
        data = []
        i = 0
        for row in users:
            i += 1
            data.append({
                "uuid":
                    row.uuid,
                "name":
                    row.name,
            })
        res = {}
        res['count'] = users.count()
        res['results'] = data
        return JsonResponse(self.msg(10000, res))


class AllTeacherPage(Common, ListView):

    def get(self, request, *args, **kwargs):
        data = request.GET
        pg = int(data.get("page", 1))
        pre = int(data.get("limit", 15))
        users = User.objects.filter(del_state=1, system_role=1)
        if data.get('name'):
            users = users.filter(name__icontains=data.get('name'))
        # # if data.get('personal_ID'):
        # #     users = users.filter(personal_ID__contains=data.get('personal_ID'))
        # if data.get('email'):
        #     users = users.filter(email__icontains=data.get('email'))
        data = []
        i = 0
        page = self.page(users, pg, pre=pre)
        for row in page.object_list:
            i += 1
            data.append({
                "uuid":
                    row.uuid,
                "name":
                    row.name,
                "school":
                    row.school or '',
                "grade":
                    row.grade or '',
                'cellphone': row.cellphone or '',
                "email":
                    row.email,
                'system_role':
                    row.system_role,
                'wechat_name':
                    row.wechat_name,
            })
        res = {}
        res['count'] = users.count()
        res['results'] = data
        return JsonResponse(self.msg(10000, res))


class OneUserView(Common, View):

    def get(self, request, *args, **kwargs):
        try:
            data = request.GET
            assert data.get('uuid')
            user = User.objects.get(uuid=data.get('uuid'), del_state=1)
            info = {
              'name': user.name,
              'wechat_name': user.wechat_name,
              'cellphone': user.cellphone or '',
              'grade': user.grade,
              'school': user.school,
              'email': user.email,
              'system_role':user.system_role,
                'belong_uuid':user.belong.uuid if user.belong else '',
                'belong_name':user.belong.name if user.belong else '',
                'has_students':user.has_students(),
            }
        except:
            return JsonResponse(self.msg(20000))
        else:
            return JsonResponse(self.msg(10000, info))

    def post(self, request, *args, **kwargs):
        try:
            data = request.POST
            assert data.get('uuid')
            name = data.get('name')
            wechat_name = data.get('wechat_name')
            cellphone = data.get('cellphone', '')
            email = data.get('email')
            grade = data.get('grade')
            school = data.get('school')
            uuid = data.get('uuid')
            has_students = data.get('has_students')
            if data.get('belong_uuid'):
                print(333)
                belong = User.objects.get(uuid=data.get('belong_uuid'), del_state=1)
            else:
                belong = User.objects.get(uuid=data.get('uuid'), del_state=1).belong
            # system_role = data.get('system_role')
            print(555)
            if User.objects.filter(wechat_name=wechat_name, del_state=1).exclude(uuid=uuid).exists():
                return JsonResponse(self.msg(20000, remsg='用户已存在'))
            print(name)
            User.objects.filter(uuid=uuid).update(
              name=name,
              wechat_name=wechat_name,
              cellphone=cellphone,
              email=email,
                grade=grade,
                school=school,
                belong=belong,
              # system_role=system_role,
            )
            if has_students:
                has_students = has_students.split(',')
                User.objects.filter(uuid=uuid).update(belong=None)
                user = User.objects.get(uuid=data.get('uuid'), del_state=1)
                print(has_students)
                uuids = []
                for one in has_students:
                    uuids.append(one)
                User.objects.filter(uuid__in=uuids).update(belong=user)
        except Exception as e:
            print(e)
            return JsonResponse(self.msg(20000))
        else:
            return JsonResponse(self.msg(10000))


class LoginView(Common,View):

    def post(self, request, *args, **kwargs):
        '''登录'''
        user = UserCommon()
        # if request.session.get('validate', '').lower() == request.POST.get(
        #   'code', '').lower():
        print(request.POST)
        result = user.login(request,
                            request.POST.get('cellphone'),
                            request.POST.get('password'))
        return JsonResponse(result)


class LogoutView(Common, View):

    def post(self, request, *args, **kwargs):
        print(7777)
        try:
            del request.session['login']
            response = JsonResponse(self.msg(10000))
        except:
            response = JsonResponse(self.msg(20000))
        return response


class AllUser(Common, ListView):

    def get(self, request, *args, **kwargs):
        data = request.GET
        pg = int(data.get("page", 1))
        pre = int(data.get("limit", 15))
        # users = User.objects.filter(del_state=1, system_role=0)
        users = User.objects.filter(del_state=1)

        if data.get('name'):
            users = users.filter(name__icontains=data.get('name'))
        if data.get('system_role'):
            users = users.filter(system_role=int(data.get('system_role')))
        # # if data.get('personal_ID'):
        # #     users = users.filter(personal_ID__contains=data.get('personal_ID'))
        # if data.get('email'):
        #     users = users.filter(email__icontains=data.get('email'))
        print(users)
        data = []
        i = 0
        page = self.page(users, pg, pre=pre)
        for row in page.object_list:
            i += 1
            data.append({
                "uuid":
                    row.uuid,
                "name":
                    row.name,
                "school":
                    row.school or '',
                "grade":
                    row.grade or '',
                'cellphone': row.cellphone or '',
                "email":
                    row.email,
                'system_role':
                    row.system_role,
                'wechat_name':
                    row.wechat_name,
                'belong':row.belong.name if row.belong else '',
            })
        res = {}
        res['count'] = users.count()
        res['results'] = data
        return JsonResponse(self.msg(10000, res))


class ResetPwdView(Common, View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        assert data.get('uuid')
        user = UserCommon()
        password = user.make_password('111111')
        try:
            user_obj = User.objects.get(uuid=data.get('uuid'), del_state=1)
            user_obj.password = password
            user_obj.save()
        except:
            return JsonResponse(self.msg(20000))
        else:
            return JsonResponse(self.msg(10000))


class DelUser(Common, View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        assert data.get('uuid')
        try:
            user_obj = User.objects.get(uuid=data.get('uuid'), del_state=1)
            user_obj.del_state = 0
            user_obj.save()
        except:
            return JsonResponse(self.msg(20000))
        else:
            return JsonResponse(self.msg(10000))


class CurrentUser(Common, View):
    def get(self, request, *args, **kwargs):
        try:
            print(33333)
            print(request.session.values)
            print(dir(request.session))
            user = User.objects.get(uuid=request.session['login'], del_state=1)
            info = {
                'name': user.name,
                'wechat_name': user.wechat_name,
                'school': user.school or '',
                'grade': user.grade or '',
                'email': user.email,
                'system_role': user.system_role,
                'uuid': user.uuid,
                'cellphone': user.cellphone
            }
        except Exception as e:
            print(e)
            return JsonResponse(self.msg(20000))
        else:
            return JsonResponse(self.msg(10000, info))


class ChangePwdView(Common, View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        assert data.get('uuid') and data.get('old_password') and data.get('new_password')

        try:
            user_obj = User.objects.get(uuid=data.get('uuid'), del_state=1)
            user = UserCommon()
            if user.check_password(data.get('old_password'), user_obj.password):
                password = user.make_password(data.get('new_password'))
                user_obj.password = password
                user_obj.save()
            else:
                return JsonResponse(self.msg(20000))
        except Exception as e:
            print(e)
            return JsonResponse(self.msg(20000))
        else:
            return JsonResponse(self.msg(10000))


class studentLogin(views.APIView):
    '''
    微信学员登录信息
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def post(self, request):
        user = UserCommon()
        # if request.session.get('validate', '').lower() == request.POST.get(
        #   'code', '').lower():
        print(request.POST)
        result = user.login(request,
                            request.POST.get('cellphone'),
                            request.POST.get('password'))
        if result['code'] == 10000:
            u_obj = User.objects.get(cellphone=request.POST.get('cellphone'), del_state=1)
            u_obj.wechat_user = request.user
            u_obj.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class StudyDetail(Common, View):

    def get_sum(self, query, attr):
        num = 0
        for i in query:
            num += getattr(i, attr)
        return num

    def get_avg(self, query, attr):
        num = 0
        for i in query:
            num += getattr(i, attr)
        avg = int(num/query.count())
        return avg

    def get(self, request, *args, **kwargs):
        try:
            data = request.GET
            course = int(data.get("course", 1))
            start_time = data.get("start_time")
            end_time = data.get("end_time")
            user_id = data.get("uuid")
            assert course and start_time and end_time and user_id
            user = User.objects.get(uuid=user_id)
            user = user.wechat_user
            start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d').date()
            end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d').date()
            tt = end_time - start_time
            print(tt.days)
            if course == 1:
                ver_names = ieltsModel.ver_name()
                cous = ieltsModel.objects.filter(user=user, signdate__gte=start_time, signdate__lte=end_time)
                summary = {}
                summary['wordnumber'] = self.get_sum(cous, 'wordnumber') if cous.count() > 0 else 0
                summary['readpercent'] = self.get_avg(cous, 'readpercent') if cous.count() > 0 else 0
                summary['listenpercent'] = self.get_avg(cous, 'listenpercent') if cous.count() > 0 else 0
                curve = []
                # if cous.count() == 0:
                #     detail = {
                #         'wordnumber': 0,
                #         'readpercent': 0,
                #         'listenpercent': 0,
                #         'signdate': '',
                #     }
                #     curve.append(detail)
                # else:
                for i in range(tt.days + 1):
                    day = start_time + datetime.timedelta(days=i)
                    one = None
                    if cous.filter(signdate=day).count() > 0:
                        one = cous.filter(signdate=day)[0]
                    detail = {
                        ver_names['wordnumber']: one.wordnumber if one else 0,
                        ver_names['readpercent']: one.readpercent if one else 0,
                        ver_names['listenpercent']: one.listenpercent if one else 0,
                        'signdate': datetime.date.strftime(day, "%Y-%m-%d"),
                    }
                    curve.append(detail)
            elif course == 2:
                ver_names = toeflModel.ver_name()
                cous = toeflModel.objects.filter(user=user, signdate__gte=start_time, signdate__lte=end_time)
                summary = {}
                summary['wordnumber'] = self.get_sum(cous, 'wordnumber') if cous.count() > 0 else 0
                summary['readpercent'] = self.get_avg(cous, 'readpercent') if cous.count() > 0 else 0
                summary['listenpercent'] = self.get_avg(cous, 'listenpercent') if cous.count() > 0 else 0
                curve = []
                for i in range(tt.days + 1):
                    day = start_time + datetime.timedelta(days=i)
                    one = None
                    if cous.filter(signdate=day).count() > 0:
                        one = cous.filter(signdate=day)[0]
                    detail = {
                        ver_names['wordnumber']: one.wordnumber if one else 0,
                        ver_names['readpercent']: one.readpercent if one else 0,
                        ver_names['listenpercent']: one.listenpercent if one else 0,
                        'signdate': datetime.date.strftime(day, "%Y-%m-%d"),
                    }
                    curve.append(detail)
            elif course == 3:
                ver_names = greModel.ver_name()
                cous = greModel.objects.filter(user=user, signdate__gte=start_time, signdate__lte=end_time)
                summary = {}
                summary['wordnumber'] = self.get_sum(cous, 'wordnumber') if cous.count() > 0 else 0
                summary['fill_blank_number'] = self.get_sum(cous, 'fill_blank_number') if cous.count() > 0 else 0
                summary['readpercent'] = self.get_avg(cous, 'readpercent') if cous.count() > 0 else 0
                summary['mathpercent'] = self.get_avg(cous, 'mathpercent') if cous.count() > 0 else 0
                curve = []
                for i in range(tt.days + 1):
                    day = start_time + datetime.timedelta(days=i)
                    one = None
                    if cous.filter(signdate=day).count() > 0:
                        one = cous.filter(signdate=day)[0]
                    detail = {
                        ver_names['wordnumber']: one.wordnumber if one else 0,
                        ver_names['readpercent']: one.readpercent if one else 0,
                        ver_names['fill_blank_number']: one.fill_blank_number if one else 0,
                        ver_names['mathpercent']: one.mathpercent if one else 0,
                        'signdate': datetime.date.strftime(day, "%Y-%m-%d"),
                    }
                    curve.append(detail)
            elif course == 4:
                ver_names = gmatModel.ver_name()
                cous = gmatModel.objects.filter(user=user, signdate__gte=start_time, signdate__lte=end_time)
                summary = {}
                summary['wordnumber'] = self.get_sum(cous, 'wordnumber') if cous.count() > 0 else 0
                summary['grammarnumber'] = self.get_sum(cous, 'grammarnumber') if cous.count() > 0 else 0
                summary['readpercent'] = self.get_avg(cous, 'readpercent') if cous.count() > 0 else 0
                summary['mathpercent'] = self.get_avg(cous, 'mathpercent') if cous.count() > 0 else 0
                summary['logicpercent'] = self.get_avg(cous, 'logicpercent') if cous.count() > 0 else 0
                curve = []
                for i in range(tt.days + 1):
                    day = start_time + datetime.timedelta(days=i)
                    one = None
                    if cous.filter(signdate=day).count() > 0:
                        one = cous.filter(signdate=day)[0]
                    detail = {
                        ver_names['wordnumber']: one.wordnumber if one else 0,
                        ver_names['readpercent']: one.readpercent if one else 0,
                        ver_names['grammarnumber']: one.grammarnumber if one else 0,
                        ver_names['mathpercent']: one.mathpercent if one else 0,
                        ver_names['logicpercent']: one.logicpercent if one else 0,
                        'signdate': datetime.date.strftime(day, "%Y-%m-%d"),
                    }
                    curve.append(detail)
            res = {}
            res['summary'] = summary
            res['curve'] = curve
        except Exception as e:
            print(e)
            return JsonResponse(self.msg(20000))
        else:
            return JsonResponse(self.msg(10000, res))


class ImageDetail(Common, View):

    def get(self, request, *args, **kwargs):
        try:
            data = request.GET
            course = int(data.get("course", 1))
            s_time = data.get("s_time")
            user_id = data.get("uuid")
            assert course and s_time and user_id
            user = User.objects.get(uuid=user_id)
            user = user.wechat_user
            detail = {}
            if course == 1:
                cous = ieltsModel.objects.filter(user=user, signdate=s_time,)
                if cous.count() > 0:
                    one = cous[0]
                    detail = {
                        'wordimageset': [IMAGES_URL + MEDIA_URL + w for w in one.wordimageset.split(',')] if one.wordimageset else [],
                        # 'readimageset': one.readimageset,
                        'readimageset': [IMAGES_URL + MEDIA_URL + w for w in one.readimageset.split(',')] if one.wordimageset else [],
                        # 'writeimageset': one.writeimageset,
                        'writeimageset': [IMAGES_URL + MEDIA_URL + w for w in one.writeimageset.split(',')] if one.writeimageset else [],
                        'listenimageset': [IMAGES_URL + MEDIA_URL + w for w in one.listenimageset.split(',')] if one.listenimageset else [],
                        'speakimageset': [IMAGES_URL + MEDIA_URL + w for w in one.speakimageset.split(',')] if one.speakimageset else [],
                        'signdate': datetime.date.strftime(one.signdate, "%Y-%m-%d"),
                    }
            elif course == 2:
                cous = toeflModel.objects.filter(user=user, signdate=s_time,)
                if cous.count() > 0:
                    one = cous[0]
                    detail = {
                        'wordimageset': [IMAGES_URL + MEDIA_URL + w for w in one.wordimageset.split(',')] if one.wordimageset else [],
                        # 'readimageset': one.readimageset,
                        'readimageset': [IMAGES_URL + MEDIA_URL + w for w in one.readimageset.split(',')] if one.wordimageset else [],
                        # 'writeimageset': one.writeimageset,
                        'writeimageset': [IMAGES_URL + MEDIA_URL + w for w in one.writeimageset.split(',')] if one.writeimageset else [],
                        'listenimageset': [IMAGES_URL + MEDIA_URL + w for w in one.listenimageset.split(',')] if one.listenimageset else [],
                        'speakimageset': [IMAGES_URL + MEDIA_URL + w for w in one.speakimageset.split(',')] if one.speakimageset else [],
                        'signdate': datetime.date.strftime(one.signdate, "%Y-%m-%d"),
                    }
            elif course == 3:
                cous = greModel.objects.filter(user=user, signdate=s_time,)
                if cous.count() > 0:
                    one = cous[0]
                    detail = {
                        'mathpercent': one.mathpercent,
                        'wordimageset': [IMAGES_URL + MEDIA_URL + w for w in one.wordimageset.split(',')] if one.wordimageset else [],
                        'readimageset': [IMAGES_URL + MEDIA_URL + w for w in one.readimageset.split(',')] if one.readimageset else [],
                        'writeimageset': [IMAGES_URL + MEDIA_URL + w for w in one.writeimageset.split(',')] if one.writeimageset else [],
                        'fill_blank_imageset': [IMAGES_URL + MEDIA_URL + w for w in one.fill_blank_imageset.split(',')] if one.fill_blank_imageset else [],
                        'mathimageset': [IMAGES_URL + MEDIA_URL + w for w in one.mathimageset.split(',')] if one.mathimageset else [],
                        'signdate': datetime.date.strftime(one.signdate, "%Y-%m-%d"),
                    }
            elif course == 4:
                cous = gmatModel.objects.filter(user=user, signdate__gte=s_time,)
                if cous.count() > 0:
                    one = cous[0]
                    detail = {
                        'wordimageset': [IMAGES_URL + MEDIA_URL + w for w in one.wordimageset.split(',')] if one.wordimageset else [],
                        'readimageset': [IMAGES_URL + MEDIA_URL + w for w in one.readimageset.split(',')] if one.readimageset else [],
                        'writeimageset': [IMAGES_URL + MEDIA_URL + w for w in one.writeimageset.split(',')] if one.writeimageset else [],
                        'grammarimageset': [IMAGES_URL + MEDIA_URL + w for w in one.grammarimageset.split(',')] if one.grammarimageset else [],
                        'mathimageset': [IMAGES_URL + MEDIA_URL + w for w in one.mathimageset.split(',')] if one.mathimageset else [],
                        'logicimageset': [IMAGES_URL + MEDIA_URL + w for w in one.logicimageset.split(',')] if one.logicimageset else [],
                        'signdate': datetime.date.strftime(one.signdate, "%Y-%m-%d"),
                    }
        except Exception as e:
            print(e)
            return JsonResponse(self.msg(20000))
        else:
            return JsonResponse(self.msg(10000, detail))
