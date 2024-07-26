#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-15
# @Desc :
from django.urls import path, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import TradingVolumeViewSet

# 创建一个简单路由器
router = routers.SimpleRouter()
router.register(r'amount', TradingVolumeViewSet, basename='amount')

# 定义 URL 路径
urlpatterns = [

]

# 添加简单路由器的 URL 到 urlpatterns
urlpatterns += router.urls

