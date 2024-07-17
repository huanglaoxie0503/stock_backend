#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-15
# @Desc :自定义权限
import re

from rest_framework.permissions import BasePermission

from config import IS_DEMO
from rest_framework.serializers import ValidationError


def validation_api(req_api, valid_api):
    """
    验证当前用户是否有接口权限
    :param req_api: 当前请求的接口
    :param valid_api: 用于验证的接口
    :return: True或者False
    """
    if valid_api is not None:
        valid_api = valid_api.replace('{uuid}', '.*?')
        matchObj = re.match(valid_api, req_api, re.M | re.I)
        if matchObj:
            return True
        else:
            return False
    else:
        return False


class CustomPermission(BasePermission):
    """
    自定义权限
    """
    def has_permission(self, request, view):

        # 演示模式判断
        if IS_DEMO and not request.method in ['GET', 'OPTIONS']:
            raise ValidationError('演示模式，不允许操作!', 400)
            return False

        # 对ViewSet下的def方法进行权限判断
        # 当权限为空时,则可以访问
        is_head = getattr(view, 'head', None)
        if is_head:
            head_kwargs = getattr(view.head, 'kwargs', None)
            if head_kwargs:
                _permission_classes = getattr(head_kwargs, 'permission_classes', None)
                if _permission_classes is None:
                    return True

        # 判断是否是超级管理员
        if request.user.is_superuser:
            return True
        else:
            api = request.path  # 当前请求接口
            method = request.method  # 当前请求方法
            methodList = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH']
            method = methodList.index(method)  # 将请求方法转换为索引

            if not hasattr(request.user, "role"):
                return False

            userApiList = request.user.role.values('permission__api', 'permission__method')  # 获取当前用户的角色拥有的所有接口

            for item in userApiList:
                valid = validation_api(api, item.get('permission__api'))
                if valid and (method == item.get('permission__method')):
                    return True
        return False
