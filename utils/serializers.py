#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-15
# @Desc :
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.request import Request
from django.contrib.auth import get_user_model
from apps.users.signals import generate_user_id

Users = get_user_model()


class CustomModelSerializer(serializers.ModelSerializer):
    """
    增强DRF的ModelSerializer, 可自动更新模型的审计字段记录
        - self.request 能获取到 rest_framework.request.Request 对象
    """

    def __init__(self, instance=None, data=serializers.empty, request=None, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.request: Request = request or self.context.get('request')

    # 修改人的审计字段名称, 默认 modifier, 继承使用时可自定义覆盖
    modifier_field_name = 'modifier'
    modifier_name = serializers.SerializerMethodField(read_only=True)

    def get_modifier_name(self, instance):
        if not hasattr(instance, self.modifier_field_name):
            return None
        user_name = Users.objects.filter(uuid=getattr(instance, self.modifier_field_name)).values_list('name',
                                                                                                       flat=True).first()
        return user_name

    # 创建人的审计字段名称, 默认 creator, 继承使用时可自定义覆盖
    creator_field_name = 'creator'
    creator_name = serializers.SlugRelatedField(slug_field="name", source="creator", read_only=True)
    # 数据所属部门字段
    # 添加默认时间返回格式
    create_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    def create(self, validated_data):
        if self.request and self.request.user.is_authenticated:
            if self.modifier_field_name in self.fields.fields:
                validated_data[self.modifier_field_name] = self.get_request_user_id()
            if self.creator_field_name in self.fields.fields:
                validated_data[self.creator_field_name] = self.request.user

        instance = super().create(validated_data)

        # 调用 generate_user_id 处理 user_id 生成逻辑，传递实例而不是 validated_data
        generate_user_id(sender=self.__class__, instance=instance)

        return instance

    def update(self, instance, validated_data):
        if self.request and self.request.user.is_authenticated:
            if self.modifier_field_name in self.fields.fields:
                validated_data[self.modifier_field_name] = self.get_request_user_id()
            if hasattr(instance, self.modifier_field_name):
                setattr(instance, self.modifier_field_name, self.get_request_user_id())

        instance = super().update(instance, validated_data)

        # Call generate_user_id here if needed
        generate_user_id(sender=self.__class__, instance=instance)

        return instance

    def get_request_username(self):
        return getattr(self.request.user, 'username', None) if self.request and self.request.user else None

    def get_request_name(self):
        return getattr(self.request.user, 'name', None) if self.request and self.request.user else None

    def get_request_user_id(self):
        return getattr(self.request.user, 'uuid', None) if self.request and self.request.user else None


# class CustomModelSerializer(serializers.ModelSerializer):
#     """
#     增强DRF的ModelSerializer, 可自动更新模型的审计字段记录
#         - self.request 能获取到 rest_framework.request.Request 对象
#     """
#
#     def __init__(self, instance=None, data=empty, request=None, **kwargs):
#         super().__init__(instance, data, **kwargs)
#         self.request: Request = request or self.context.get('request')
#
#     # 修改人的审计字段名称, 默认 modifier, 继承使用时可自定义覆盖
#     modifier_field_name = 'modifier'
#     modifier_name = serializers.SerializerMethodField(read_only=True)
#
#     def get_modifier_name(self, instance):
#         if not hasattr(instance, self.modifier_field_name):
#             return None
#         user_name = Users.objects.filter(uuid=getattr(instance, self.modifier_field_name)).values_list('name',
#                                                                                                        flat=True).first()
#         return user_name
#
#     # 创建人的审计字段名称, 默认 creator, 继承使用时可自定义覆盖
#     creator_field_name = 'creator'
#     creator_name = serializers.SlugRelatedField(slug_field="name", source="creator", read_only=True)
#     # 数据所属部门字段
#     # dept_belong_field_name = 'dept_belong_id'
#     # 添加默认时间返回格式
#     create_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
#     update_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
#
#     def create(self, validated_data):
#         if self.request and self.request.user.is_authenticated:
#             if self.modifier_field_name in self.fields.fields:
#                 validated_data[self.modifier_field_name] = self.get_request_user_id()
#             if self.creator_field_name in self.fields.fields:
#                 validated_data[self.creator_field_name] = self.request.user
#
#         # 创建 UserProfile 实例，将 validated_data 直接传递给 UserProfile.objects.create
#         instance = Users.objects.create(**validated_data)
#
#         # 调用 generate_user_id 处理 user_id 生成逻辑，传递实例而不是 validated_data
#         generate_user_id(sender=self.__class__, instance=instance)
#
#         # 直接调用 self.save() 而不是 super().create(validated_data)
#         return self.save()
#
#     def update(self, instance, validated_data):
#         if self.request and self.request.user.is_authenticated:
#             if self.modifier_field_name in self.fields.fields:
#                 validated_data[self.modifier_field_name] = self.get_request_user_id()
#             if hasattr(instance, self.modifier_field_name):
#                 setattr(instance, self.modifier_field_name, self.get_request_user_id())
#
#         # Call generate_user_id here if needed
#         generate_user_id(self, validated_data)
#
#         # 直接调用 self.save() 而不是 super().update(instance, validated_data)
#         return self.save()
#
#     def save(self, **kwargs):
#         return super().save(**kwargs)
#
#     def get_request_username(self):
#         return getattr(self.request.user, 'username', None) if self.request and self.request.user else None
#
#     def get_request_name(self):
#         return getattr(self.request.user, 'name', None) if self.request and self.request.user else None
#
#     def get_request_user_id(self):
#         return getattr(self.request.user, 'uuid', None) if self.request and self.request.user else None
