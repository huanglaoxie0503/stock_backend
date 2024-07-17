#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-15
# @Desc :
from django.urls import path, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UsersViewSet, UserManageViewSet, LoginView, CaptchaView

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
]

# 添加简单路由器的 URL 到 urlpatterns
urlpatterns += router.urls

