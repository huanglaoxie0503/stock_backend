#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-31
# @Desc :
import xadmin
from datetime import datetime
from loguru import logger
from django.core.cache import cache


from apps.stock_picker.models import (
    StockAuction,
    StockLimitUpAuction,
    StockAuctionConditions,
)
from utils.common import format_color
from utils.models import BaseColorAdmin


class StockAuctionAdmin(object):
    list_display = ['trade_date_color', 'stock_code', 'stock_name', 'latest_price', 'limit_up_order_amount', 'cap', 'limit_up_reason']
    list_filter = ['trade_date', 'stock_code', 'stock_name']
    search_fields = ['trade_date', 'stock_code', 'stock_name']
    ordering = ['-trade_date']
    list_per_page = 10
    list_display_links = ['trade_date']
    list_editable = []
    app_icon = 'fa fa-anchor'
    model_icon = 'fa fa-hand-o-up'

    def trade_date_color(self, obj):
        current_date = datetime.now().date()
        thresholds = [
            lambda x: x == current_date
        ]
        colors = ['red']
        return format_color(obj.trade_date, thresholds, colors)

    trade_date_color.short_description = '交易日'


class StockLimitUpAuctionAdmin(object):
    list_display = ['trade_date_color', 'stock_code', 'stock_name', 'limit_up_days', 'vol_ratio_color', 'vol_ratio_oa_color', 'cap_color', 'auction_amount', 'auction_volume', 'pre_max_volume', 'pre_volume', 'open_price', 'pre_close', 'limit_up_opening_nums', 'last_limit_up_time', 'limit_up_reasons', 'cb', 'model_name', 'is_ops', 'profit_chg', 'profit_chg_close']
    list_filter = ['trade_date', 'stock_code', 'stock_name', 'is_ops', 'limit_up_days']
    search_fields = ['trade_date', 'stock_code', 'stock_name', 'is_ops', 'limit_up_days']
    # 排序字段
    ordering = ['-trade_date', '-limit_up_days', '-pre_open_vol_ratio']
    list_per_page = 15
    list_display_links = ['trade_date']
    list_editable = []
    model_icon = 'fa fa-thumbs-o-up'

    def queryset(self):
        qs = super().queryset()
        # 根据日期字段进行排序，并只取最新日期的数据
        latest_date = qs.latest('trade_date').trade_date
        return qs.filter(trade_date=latest_date)

    def get_queryset(self, request):
        logger.debug("get_queryset called")

        # 缓存逻辑
        cache_key = 'stock_limit_up'
        cached_queryset = cache.get(cache_key)

        if cached_queryset is None:
            logger.debug("Cache miss - Querying database")
            queryset = super().get_queryset(request)

            # 默认过滤 limit_up_days 为 1 和 2 的数据
            if not request.GET.get('limit_up_days__exact'):
                queryset = queryset.filter(limit_up_days__in=[1, 2])

            # 将查询集转换为列表以便缓存
            cached_queryset = list(queryset)
            cache.set(cache_key, cached_queryset, timeout=3600)  # 设置缓存有效期为1小时
        else:
            logger.debug("Cache hit")
            queryset = cached_queryset

        # 如果用户指定了筛选条件，应用该筛选条件
        limit_up_days = request.GET.get('limit_up_days__exact')
        if limit_up_days:
            queryset = [item for item in cached_queryset if item.limit_up_days == int(limit_up_days)]

        return queryset

    # 天量比
    def vol_ratio_color(self, obj):
        thresholds = [
            lambda x: 0.09 < x <= 0.20,
            lambda x: x > 0.20
        ]
        colors = ['red', 'blue']
        return format_color(obj.pre_open_vol_ratio, thresholds, colors)

    vol_ratio_color.short_description = '天量比'

    # 分量比
    def vol_ratio_oa_color(self, obj):
        thresholds = [
            lambda x: 0.70 <= x <= 2.0,
            lambda x: x > 2.0
        ]
        colors = ['red', 'blue']
        return format_color(obj.pre_open_max_vol_ratio, thresholds, colors)

    vol_ratio_oa_color.short_description = '分量比'

    # 市值(亿)
    def cap_color(self, obj):
        thresholds = [
            lambda x: x < 30
        ]
        colors = ['red']
        return format_color(obj.cap, thresholds, colors)
    cap_color.short_description = '市值(亿)'

    def trade_date_color(self, obj):
        current_date = datetime.now().date()
        thresholds = [
            lambda x: x == current_date
        ]
        colors = ['red']
        return format_color(obj.trade_date, thresholds, colors)

    trade_date_color.short_description = '交易日'


class StockAuctionConditionsAdmin(BaseColorAdmin):
    list_display = ['trade_date_color', 'stock_code', 'stock_name', 'open_price', 'pre_close', 'high_price', 'vol_ratio_color', 'vol_ratio_oa_color', 'cap', 'gap_type_color', 'cond_name', 'auction_volume', 'pre_max_volume', 'pre_volume', 'auction_amount', 'profit_chg_color', 'profit_chg_close', 'is_ops']
    list_filter = ['trade_date', 'stock_code', 'stock_name', 'is_ops', 'gap_type', 'is_ops']
    search_fields = ['trade_date', 'stock_code', 'stock_name', 'is_ops', 'gap_type', 'is_ops']
    ordering = ['-trade_date',  '-profit_chg']
    model_icon = 'fa fa-legal'
    list_per_page = 15
    list_display_links = ['trade_date']
    list_editable = []

    def vol_ratio_color(self, obj):
        thresholds = [
            lambda x: 0.09 < x <= 0.20,
            lambda x: x > 0.20
        ]
        colors = ['red', 'blue']
        return format_color(obj.pre_open_vol_ratio, thresholds, colors)

    vol_ratio_color.short_description = '天量比'

    # 分量比
    def vol_ratio_oa_color(self, obj):
        thresholds = [
            lambda x: 0.70 <= x <= 2.0,
            lambda x: x > 2.0
        ]
        colors = ['red', 'blue']
        return format_color(obj.pre_open_max_vol_ratio, thresholds, colors)

    vol_ratio_oa_color.short_description = '分量比'

    def profit_chg_color(self, obj):
        thresholds = [
            lambda x: x >= 3.0
        ]
        colors = ['red']
        return format_color(obj.profit_chg, thresholds, colors)

    profit_chg_color.short_description = '竞价盈亏'

    def trade_date_color(self, obj):
        current_date = datetime.now().date()
        thresholds = [
            lambda x: x == current_date
        ]
        colors = ['red']
        return format_color(obj.trade_date, thresholds, colors)

    trade_date_color.short_description = '交易日'

    def gap_type_color(self, obj):
        thresholds = [
            lambda x: x == '高开过顶',
        ]
        colors = ['red']
        return format_color(obj.gap_type, thresholds, colors)
    gap_type_color.short_description = '高开类型'


xadmin.site.register(StockAuction, StockAuctionAdmin)
xadmin.site.register(StockLimitUpAuction, StockLimitUpAuctionAdmin)
xadmin.site.register(StockAuctionConditions, StockAuctionConditionsAdmin)
