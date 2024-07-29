#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-26
# @Desc :
import django_filters

from .models import (
    TradingVolume
, StockLimitUpDetail
, StockLimitDownDetail
, StockLimitBlast
)


class BaseTradeDateFilter(django_filters.FilterSet):
    trade_date = django_filters.DateFilter(field_name="trade_date", lookup_expr='gte')

    class Meta:
        abstract = True
        fields = ['trade_date']


class TradingVolumeFilter(BaseTradeDateFilter):
    class Meta(BaseTradeDateFilter.Meta):
        model = TradingVolume


class StockLimitUpDetailFilter(BaseTradeDateFilter):
    class Meta(BaseTradeDateFilter.Meta):
        model = StockLimitUpDetail


class StockLimitDownDetailFilter(BaseTradeDateFilter):
    class Meta(BaseTradeDateFilter.Meta):
        model = StockLimitDownDetail


class StockLimitBlastFilter(BaseTradeDateFilter):
    class Meta(BaseTradeDateFilter.Meta):
        model = StockLimitBlast
