#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-26
# @Desc :
from rest_framework import serializers

from .models import TradingVolume


class TradingVolumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingVolume
        fields = "__all__"
        read_only_fields = ["id"]


class TradingVolumeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingVolume
        fields = '__all__'  # 或者你可以列出具体的字段，例如 ['field1', 'field2']
