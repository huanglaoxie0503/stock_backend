#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-15
# @Desc :
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from utils.filters import CustomFilterBackend, CustomDjangoFilterBackend
from utils.jsonResponse import SuccessResponse, ErrorResponse, DetailResponse
from utils.permission import CustomPermission
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated


class CustomModelViewSet(viewsets.ModelViewSet):
    """
    自定义的 ModelViewSet 类，用于统一标准的返回格式，支持不同的序列化器用于创建、更新操作，
    并提供了性能优化的 ORM 查询方式以及批量删除功能。
    """

    # ORM 性能优化，尽可能使用 values_queryset 形式
    values_queryset = None

    # 排序字段
    ordering_fields = '__all__'

    # 创建和更新时使用的序列化器
    create_serializer_class = None
    update_serializer_class = None

    # 过滤字段
    filterset_fields = ()

    # 搜索字段
    search_fields = ()

    # 额外的过滤后端
    extra_filter_backends = [CustomFilterBackend]

    # 权限类
    permission_classes = [CustomPermission, IsAuthenticated]

    # 过滤后端
    filter_backends = [CustomDjangoFilterBackend, OrderingFilter, SearchFilter]

    def filter_queryset(self, queryset):
        """
        重写 filter_queryset 方法，合并默认过滤后端和额外过滤后端进行过滤。
        """
        for backend in set(self.filter_backends) | set(self.extra_filter_backends or []):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get_queryset(self):
        """
        重写 get_queryset 方法，如果 values_queryset 已设置，则直接返回。
        否则，调用父类方法。
        """
        if self.values_queryset:
            return self.values_queryset
        return super().get_queryset()

    def get_serializer_class(self):
        """
        根据当前动作选择对应的序列化器类。
        """
        action_serializer_name = f'{self.action}_serializer_class'
        action_serializer_class = getattr(self, action_serializer_name, None)
        if action_serializer_class:
            return action_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        """
        重写 create 方法，使用 create_serializer_class 进行序列化。
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return DetailResponse(data=serializer.data, msg='新增成功')

    def list(self, request, *args, **kwargs):
        """
        重写 list 方法，对查询集进行过滤和分页处理。
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data, msg='获取成功')

    def retrieve(self, request, *args, **kwargs):
        """
        重写 retrieve 方法，获取单个对象并序列化。
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data, msg='获取成功')

    def update(self, request, *args, **kwargs):
        """
        重写 update 方法，使用 update_serializer_class 进行序列化。
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return DetailResponse(data=serializer.data, msg='更新成功')

    def destroy(self, request, *args, **kwargs):
        """
        重写 destroy 方法，支持单个对象的删除。
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return DetailResponse(data=[], msg='删除成功')

    def perform_destroy(self, instance):
        """
        执行删除操作。
        """
        instance.delete()

    keys_schema = openapi.Schema(
        description='主键列表',
        type=openapi.TYPE_ARRAY,
        items=openapi.TYPE_STRING
    )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['keys'],
            properties={'keys': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.TYPE_STRING)}
        ),
        operation_summary='批量删除'
    )
    @action(methods=['delete'], detail=False)
    def multiple_delete(self, request, *args, **kwargs):
        """
        批量删除方法，从请求体中获取 keys 列表，然后执行删除操作。
        """
        keys = request.data.get('keys')
        if not keys:
            raise ValidationError("Keys field is required.")

        queryset = self.get_queryset()
        filtered_queryset = queryset.filter(id__in=keys)
        count, _ = filtered_queryset.delete()
        if count > 0:
            return SuccessResponse(data=[], msg=f'成功删除{count}条记录')
        else:
            return ErrorResponse(status=status.HTTP_404_NOT_FOUND, msg='没有找到匹配的记录')
