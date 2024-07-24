#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-15
# @Desc :自定义权限
import re

from rest_framework.serializers import ValidationError
from rest_framework.permissions import BasePermission

from config import IS_DEMO


class CustomPermission(BasePermission):
    """
    自定义权限类，用于检查用户是否有访问特定API的权限。
    """

    def has_permission(self, request, view):
        # 演示模式判断
        if IS_DEMO and request.method not in ['GET', 'OPTIONS']:
            raise ValidationError('演示模式，不允许操作!', 400)

        # 当权限为空时，则可以访问
        if getattr(view, 'head', None):
            head_kwargs = getattr(view.head, 'kwargs', {})
            if head_kwargs.get('permission_classes') is None:
                return True

        # 超级管理员直接放行
        if request.user.is_superuser:
            return True

        # 获取当前请求的接口和方法
        api = request.path
        method = request.method.lower()

        # 检查用户身份是否有访问权限
        if hasattr(request.user, "identity") and request.user.profile:
            profile_data = request.user.identity.data  # 假设profile数据存储在data字段中
            if 'permissions' in profile_data:
                for permission in profile_data['permissions']:
                    if validation_api(api, permission['api']) and method == permission['method'].lower():
                        return True
        return False


def validation_api(req_api, valid_api):
    """
    验证当前用户是否有接口权限。
    """
    if valid_api is not None:
        valid_api = valid_api.replace('{uuid}', '.*?')
        return bool(re.match(valid_api, req_api, re.IGNORECASE))
    return False
