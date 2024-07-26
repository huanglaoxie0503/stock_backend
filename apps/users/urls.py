#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-15
# @Desc :
from django.urls import path, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UsersViewSet,
    UserManageViewSet,
    LoginView,
    CaptchaView,
)
from .customer_views import (
    SendSmsCodeView,
    MobileRegisterView,
    UsernamePasswordLoginView,
    MobileSmsLoginView,
    MobilePasswordLoginView,
    ForgetPasswdResetView
)

# 创建一个简单路由器
router = routers.SimpleRouter()
router.register(r'api/user', UsersViewSet, basename='user')
router.register(r'api/users', UserManageViewSet, basename='usermanage')

# 定义 URL 路径
urlpatterns = [
    # 后台禁用用户
    re_path(r'^users/disableuser/(?P<pk>.*?)/$', UserManageViewSet.as_view({'put': 'disable_user'}), name='disable_user'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/captcha/', CaptchaView.as_view(), name='captcha'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # ----------------------------------前端用户登录 ---------------------------------
    # 发送短信验证码
    path('api/sendsms/', SendSmsCodeView.as_view(), name='send_sms_code'),
    # 手机号注册
    path('api/register/', MobileRegisterView.as_view(), name='register'),
    # 使用用户名和密码进行登录
    path('api/login/username/', UsernamePasswordLoginView.as_view(), name='username_login'),
    # 使用手机号和密码进行登录
    path('api/login/mobile/', MobilePasswordLoginView.as_view(), name='mobile_login'),
    # 使用手机号和短信验证码进行登录
    path('api/login/sms/', MobileSmsLoginView.as_view(), name='sms_login'),
    # 手机号重置密码
    path('api/resetpassword/', ForgetPasswdResetView.as_view(), name='reset_password'),
]

# 添加简单路由器的 URL 到 urlpatterns
urlpatterns += router.urls

