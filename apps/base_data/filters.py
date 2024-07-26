#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-26
# @Desc :
import django_filters

from .models import TradingVolume


class TradingVolumeFilter(django_filters.FilterSet):
    trade_date = django_filters.DateFilter(field_name="trade_date", lookup_expr='gte')

    class Meta:
        model = TradingVolume
        fields = ['trade_date']
