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

from .views import *

from django.conf.urls import url, include
from django.urls import path,include,re_path

router = DefaultRouter()
router.register(r'course', createieltsdetailinfo, basename='coursedetailinfo')  #ielts 基础信息

urlpatterns = [
    #url(r'^', include(router.urls)),
    re_path('^ielts/Create/', createieltsdetailinfo.as_view(), name='createieltscourse'),
    re_path('^GetIelts/', Getieltsdetailinfo.as_view(), name='GetIelts'),  # 用户
    re_path('^GetIelts/list/', GetIeltsList.as_view(), name='GetIeltList'),  # 用户
    re_path('^toefl/Create/', createtoefldetailinfo.as_view(), name='createtoeflcourse'),
    re_path('^GetToefl/', Gettoefldetailinfo.as_view(), name='GetToefl'),  # 用户
    re_path('^GetToefl/list/', GetToeflList.as_view(), name='GetToeflList'),  # 用户
    re_path('^gre/Create/', creategredetailinfo.as_view(), name='creategrecourse'),
    re_path('^GetGre/', Getgredetailinfo.as_view(), name='GetGre'),  # 用户
    re_path('^GetGre/list/', GetGreList.as_view(), name='GetGreList'),  # 用户
    re_path('^gmat/Create/', creategmatdetailinfo.as_view(), name='creategmatcourse'),
    re_path('^GetGmat/', Getgmatdetailinfo.as_view(), name='GetGmat'),  # 用户
    re_path('^GetGmat/list/', GetGmatList.as_view(), name='GetGmatList'),  # 用户
]