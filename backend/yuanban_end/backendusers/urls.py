"""Yiqi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import Registered, ObtainJSONWebToken, GetUser
from .views import *
from django.urls import path,include,re_path
from django.views.decorators.csrf import csrf_exempt
app_name = 'users'
router = DefaultRouter()
router.register(r'Registered', Registered, basename='Registered')  # 注册

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^login/$', ObtainJSONWebToken.as_view()),  # 登录
    re_path(r'^student/login/$', studentLogin.as_view()),  # 登录
    re_path('^GetUser/', GetUser.as_view(), name='GetUser'),  # 用户
    re_path('^teacher/userlogin/', csrf_exempt(LoginView.as_view()), name="login"),
    re_path('^teacher/logout/', csrf_exempt(LogoutView.as_view()), name="logout"),
    re_path('^teacher/create/user/', csrf_exempt(CreateUserView.as_view()), name="createuser"),
    re_path('^teacher/oneuser/', csrf_exempt(OneUserView.as_view()), name="oneuser"),
    re_path('^teacher/alluser/', csrf_exempt(AllUser.as_view()), name='alluser'),
    re_path('^teacher/allteacher/', csrf_exempt(AllTeacher.as_view()), name='allteacher'),
    re_path('^teacher/allteacherpage/', csrf_exempt(AllTeacherPage.as_view()), name='allteacherpage'),
    re_path('^teacher/deluser/', csrf_exempt(DelUser.as_view()), name='deluser'),
    re_path('^teacher/resetpwd/', csrf_exempt(ResetPwdView.as_view()), name='resetpwd'),
    re_path('^teacher/currentuser/', csrf_exempt(CurrentUser.as_view()), name='currentuser'),
    re_path('^teacher/studentdetail/', csrf_exempt(StudyDetail.as_view()), name='currentuser'),
    re_path('^teacher/changepwd/', csrf_exempt(ChangePwdView.as_view()), name='changepwd'),
]
