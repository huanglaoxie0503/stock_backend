#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-15
# @Desc :
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.request import Request
from django.contrib.auth import get_user_model

Users = get_user_model()


class CustomModelSerializer(serializers.ModelSerializer):
    """
    增强DRF的ModelSerializer,自动更新模型的审计字段记录
    1. self.request 能获取到 rest_framework.request.Request 对象
    """
    # 修改人的审计字段名称, 默认 modifier, 继承使用时可自定义覆盖
    modifier_field_id = 'modifier'
    # 修改人姓名的序列化字段, 只读
    modifier_name = serializers.SerializerMethodField(read_only=True)

    # 创建人的审计字段名称, 默认 creator, 继承使用时可自定义覆盖
    creator_field_id = 'creator'
    # 创建人姓名的序列化字段, 只读
    creator_name = serializers.SlugRelatedField(slug_field="name", source="creator", read_only=True)

    # 数据所属部门字段
    # dept_belong_id_field_name = 'dept_belong_id'

    # 添加默认时间返回格式
    create_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    def __init__(self, instance=None, data=empty, request=None, **kwargs):
        """
        初始化方法
        :param instance: 模型实例
        :param data: 序列化数据
        :param request: 请求对象
        :param kwargs: 其他参数
        """
        super().__init__(instance, data, **kwargs)
        # 将 self.request 设置为传入的 request 参数，如果没有传入 request 参数，则从 self.context 中获取 request 对象。
        self.request: Request = request or self.context.get('request', None)

    def save(self, **kwargs):
        """
        保存方法
        :param kwargs: 其他参数
        :return: 保存的实例
        """
        return super().save(**kwargs)

    def create(self, validated_data):
        """
        创建方法
        :param validated_data: 验证后的数据
        :return: 创建的实例
        """
        if self.request:
            if str(self.request.user) != "AnonymousUser":
                # 设置修改人
                if self.modifier_field_id in self.fields.fields:
                    validated_data[self.modifier_field_id] = self.get_request_user_id()
                # 设置创建人
                if self.creator_field_id in self.fields.fields:
                    validated_data[self.creator_field_id] = self.request.user
                # 设置所属部门
                # if self.dept_belong_id_field_name in self.fields.fields and not validated_data.get(self.dept_belong_id_field_name, None):
                #     validated_data[self.dept_belong_id_field_name] = getattr(self.request.user, 'dept_id', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        更新方法
        :param instance: 要更新的实例
        :param validated_data: 验证后的数据
        :return: 更新的实例
        """
        if self.request:
            if str(self.request.user) != "AnonymousUser":
                # 设置修改人
                if self.modifier_field_id in self.fields.fields:
                    validated_data[self.modifier_field_id] = self.get_request_user_id()
            # 更新实例的修改人字段
            if hasattr(self.instance, self.modifier_field_id):
                setattr(self.instance, self.modifier_field_id, self.get_request_user_id())
        return super().update(instance, validated_data)

    def get_request_username(self):
        """
        获取当前请求用户的用户名
        :return: 当前请求用户的用户名
        """
        if getattr(self.request, 'user', None):
            return getattr(self.request.user, 'username', None)
        return None

    def get_request_name(self):
        """
        获取当前请求用户的姓名
        :return: 当前请求用户的姓名
        """
        if getattr(self.request, 'user', None):
            return getattr(self.request.user, 'name', None)
        return None

    def get_request_user_id(self):
        """
        获取当前请求用户的ID
        :return: 当前请求用户的ID
        """
        if getattr(self.request, 'user', None):
            return getattr(self.request.user, 'id', None)
        return None

    @staticmethod
    def get_modifier_name(instance):
        """
        获取修改人的姓名
        :param instance: 模型实例
        :return: 修改人的姓名
        """
        if not hasattr(instance, 'modifier'):
            return None
        queryset = Users.objects.filter(id=instance.modifier).values_list('name', flat=True).first()
        if queryset:
            return queryset
        return None
