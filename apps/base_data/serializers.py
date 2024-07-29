#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-26
# @Desc :
from utils.serializers import CustomModelSerializer

from .models import (
    TradingVolume,
    StockLimitUpDetail,
    StockLimitDownDetail,
    StockLimitBlast
)


class TradingVolumeSerializer(CustomModelSerializer):
    class Meta:
        model = TradingVolume
        fields = "__all__"
        read_only_fields = ["id"]


class StockLimitUpDetailSerializer(CustomModelSerializer):
    class Meta:
        model = StockLimitUpDetail
        fields = "__all__"
        read_only_fields = ["id"]


class StockLimitDownDetailSerializer(CustomModelSerializer):
    class Meta:
        model = StockLimitDownDetail
        fields = "__all__"
        read_only_fields = ["id"]


class StockLimitBlastSerializer(CustomModelSerializer):
    class Meta:
        model = StockLimitBlast
        fields = "__all__"
        read_only_fields = ["id"]
