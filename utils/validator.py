#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-17
# @Desc :自定义验证器
import logging
from django.db import DataError
from rest_framework.exceptions import APIException
from rest_framework.validators import UniqueValidator

logger = logging.getLogger(__name__)  # 创建一个日志记录器


class CustomValidationError(APIException):
    """
    自定义验证错误类，用于处理验证失败的情况。
    避免在错误信息中暴露敏感字段，提供更安全的错误反馈。
    """

    def __init__(self, detail, code=None):
        super().__init__(detail=detail, code=code)
        logger.error("Validation error occurred with detail: %s", detail)


def qs_exists(queryset):
    """
    检查queryset是否存在任何元素。
    在发生类型错误、值错误或数据库数据错误时，返回False。
    """
    try:
        return queryset.exists()
    except (TypeError, ValueError, DataError) as e:
        logger.error("Error checking queryset existence: %s", e)
        return False


def qs_filter(queryset, **kwargs):
    """
    使用提供的关键字参数过滤queryset。
    在发生类型错误、值错误或数据库数据错误时，返回一个空的queryset。
    """
    try:
        return queryset.filter(**kwargs)
    except (TypeError, ValueError, DataError) as e:
        logger.error("Error filtering queryset: %s", e)
        return queryset.none()


class CustomUniqueValidator(UniqueValidator):
    """
    自定义唯一性验证器，用于确保字段的唯一性。
    当字段值在数据库中已经存在时，会抛出CustomValidationError异常。
    支持在更新操作中排除当前实例，避免误判为重复。
    """

    def filter_queryset(self, value, queryset, field_name):
        """
        根据给定的属性过滤queryset。
        """
        filter_kwargs = {'%s__%s' % (field_name, self.lookup): value}
        return qs_filter(queryset, **filter_kwargs)

    def exclude_current_instance(self, queryset, instance):
        """
        如果正在进行更新操作，排除当前实例本身，以避免将其视为唯一性冲突。
        """
        if instance is not None:
            return queryset.exclude(pk=instance.pk)
        return queryset

    def __call__(self, value, serializer_field):
        field_name = serializer_field.source_attrs[-1]
        instance = getattr(serializer_field.parent, 'instance', None)
        queryset = self.queryset
        queryset = self.filter_queryset(value, queryset, field_name)
        queryset = self.exclude_current_instance(queryset, instance)
        if qs_exists(queryset):
            raise CustomValidationError(self.message)

    def __repr__(self):
        return super().__repr__()

