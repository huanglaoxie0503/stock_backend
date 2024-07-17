#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-15
# @Desc :
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from utils.filters import CustomFilterBackend, CustomDjangoFilterBackend
from utils.jsonResponse import SuccessResponse, ErrorResponse, DetailResponse
from utils.permission import CustomPermission
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated


class CustomModelViewSet(ModelViewSet):
    """
    自定义的 ModelViewSet:
    统一标准的返回格式；新增、查询、修改可使用不同序列化器。
    (1) ORM 性能优化，尽可能使用 values_queryset 形式
    (2) create_serializer_class 新增时使用的序列化器
    (3) update_serializer_class 修改时使用的序列化器
    """
    values_queryset = None
    ordering_fields = '__all__'
    create_serializer_class = None
    update_serializer_class = None
    filterset_fields = ()
    search_fields = ()
    extra_filter_backends = [CustomFilterBackend]
    permission_classes = [CustomPermission, IsAuthenticated]
    filter_backends = [CustomDjangoFilterBackend, OrderingFilter, SearchFilter]

    def filter_queryset(self, queryset):
        for backend in set(self.filter_backends) | set(self.extra_filter_backends or []):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get_queryset(self):
        if self.values_queryset:
            return self.values_queryset
        return super().get_queryset()

    def get_serializer_class(self):
        action_serializer_name = f'{self.action}_serializer_class'
        action_serializer_class = getattr(self, action_serializer_name, None)
        if action_serializer_class:
            return action_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return DetailResponse(data=serializer.data, msg='新增成功')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg='获取成功')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data, msg='获取成功')

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, request=request, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if hasattr(instance, '_prefetched_objects_cache'):
            instance._prefetched_objects_cache = {}

        return DetailResponse(data=serializer.data, msg='更新成功')

    def get_object_list(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument named "%s". '
            'Fix your URL conf, or set the `.lookup_field` attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {f'{self.lookup_field}__in': self.kwargs[lookup_url_kwarg].split(',')}
        obj = queryset.filter(**filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object_list()
        self.perform_destroy(instance)
        return DetailResponse(data=[], msg='删除成功')

    def perform_destroy(self, instance):
        instance.delete()

    keys_schema = openapi.Schema(description='主键列表', type=openapi.TYPE_ARRAY, items=openapi.TYPE_STRING)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['keys'],
        properties={'keys': keys_schema}
    ), operation_summary='批量删除')
    @action(methods=['delete'], detail=False)
    def multiple_delete(self, request, *args, **kwargs):
        request_data = request.data
        keys = request_data.get('keys', None)
        if keys:
            self.get_queryset().filter(id__in=keys).delete()
            return SuccessResponse(data=[], msg='删除成功')
        else:
            return ErrorResponse(msg='未获取到 keys 字段')
