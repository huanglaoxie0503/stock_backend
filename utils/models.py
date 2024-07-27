#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-12
# @Desc :
import uuid

from django.db import models

from stock_backend import settings


def make_guid():
    # 生成一个 UUID 对象
    guid_object = uuid.uuid4()
    # 将 UUID 对象转换为字符串形式
    guid_str = str(guid_object)
    return guid_str


class CoreModel(models.Model):
    """
    核心标准抽象模型模型,可直接继承使用
    增加审计字段, 覆盖字段时, 字段名称请勿修改, 必须统一审计字段名称
    """
    id = models.AutoField(primary_key=True, verbose_name="自增ID", help_text="自增ID")
    user_id = models.UUIDField(default=make_guid, editable=False, unique=True, verbose_name="UUID", help_text="UUID")
    description = models.CharField(max_length=100, null=True, blank=True, verbose_name="描述", help_text="描述")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间", help_text="创建时间")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="修改时间", help_text="修改时间")

    class Meta:
        abstract = True
        verbose_name = '核心模型'
        verbose_name_plural = verbose_name


class BaseModel(models.Model):
    """
        auto_now=True：每次对象保存时自动设置字段为当前时间。
        auto_now_add=True：对象第一次创建时自动设置字段为当前时间。
    """
    id = models.AutoField(primary_key=True, verbose_name="自增ID", help_text="自增ID")
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    class Meta:
        abstract = True  # 表示该类是一个抽象类，只用来继承，不参与迁移操作
        verbose_name = '基本模型'
        verbose_name_plural = verbose_name


if __name__ == '__main__':
    r = make_guid()
    print(r)
