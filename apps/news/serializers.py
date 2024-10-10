#!/usr/bin/python
# -*- coding:UTF-8 -*-
"""
# @Time    :    2024-10-10 19:45
# @Author  :   oscar
# @Desc    :   None
"""
from .models import ClsNews
from utils.serializers import CustomModelSerializer


class ClsNewsSerializer(CustomModelSerializer):
    class Meta:
        model = ClsNews
        fields = "__all__"
        read_only_fields = ["id", "article_id", "create_datetime", "update_datetime"]