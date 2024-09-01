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
    StockLimitUpAuctionReal,
    StockAuctionConditions,
)
from utils.common import format_color
from utils.models import BaseColorAdmin


class StockAuctionAdmin(object):
    list_display = ['trade_date_color', 'stock_code', 'stock_name', 'limit_up_order_amount', 'cap', 'latest_price', 'limit_up_reason', 'update_datetime']
    list_filter = ['trade_date', 'stock_code', 'stock_name']
    search_fields = ['trade_date', 'stock_code', 'stock_name']
    ordering = ['-trade_date']
    list_per_page = 10
    list_display_links = ['trade_date']
    list_editable = []
    app_icon = 'fa fa-anchor'
    model_icon = 'fa fa-hand-o-up'

    def queryset(self):
        qs = super().queryset()
        # 根据日期字段进行排序，并只取最新日期的数据
        latest_date = qs.latest('trade_date').trade_date
        # 按最新日期筛选数据，并按 limit_up_order_amount 字段倒序排序
        return qs.filter(trade_date=latest_date).order_by('-limit_up_order_amount')

    def trade_date_color(self, obj):
        current_date = datetime.now().date()
        thresholds = [
            lambda x: x == current_date
        ]
        colors = ['red']
        return format_color(obj.trade_date, thresholds, colors)

    trade_date_color.short_description = '交易日'


class StockLimitUpAuctionAdmin(object):
    list_display = ['trade_date_color', 'stock_code', 'stock_name', 'limit_up_days', 'vol_ratio_color', 'vol_ratio_oa_color', 'cap_color', 'open_price', 'pre_close', 'model_name', 'last_limit_up_time', 'limit_up_reasons', 'is_ops', 'profit_chg', 'profit_chg_close', 'cb', 'update_datetime']
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
        return qs.filter(trade_date=latest_date, limit_up_days__in=[1, 2])

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


class StockLimitUpAuctionRealAdmin(object):
    list_display = ['trade_date_color', 'stock_code', 'stock_name', 'limit_up_days', 'vol_ratio_color',
                    'vol_ratio_oa_color', 'cap_color', 'open_price', 'pre_close', 'model_name', 'last_limit_up_time',
                    'limit_up_reasons', 'is_ops', 'profit_chg', 'profit_chg_close', 'cb', 'update_datetime']
    list_filter = ['trade_date', 'stock_code', 'stock_name', 'is_ops', 'limit_up_days']
    search_fields = ['trade_date', 'stock_code', 'stock_name', 'is_ops', 'limit_up_days']
    # 排序字段
    # ordering = ['-trade_date', '-limit_up_days', '-pre_open_vol_ratio']
    list_per_page = 15
    list_display_links = ['trade_date']
    list_editable = []
    model_icon = 'fa fa-thumbs-o-up'

    def queryset(self):
        from django.db.models import F, Window
        from django.db.models.functions import RowNumber
        qs = super().queryset()
        latest_date = qs.latest('trade_date').trade_date

        # 使用 Window 函数为每个 limit_up_reasons 分组添加 row_number，并按 cap 从小到大排序
        annotated_qs = qs.filter(
            trade_date=latest_date
        ).annotate(
            row_number=Window(
                expression=RowNumber(),
                partition_by=[F('limit_up_reasons')],
                order_by=F('cap').asc()  # 确保这里是升序排序
            )
        )

        # 按 row_number 排序
        return annotated_qs.order_by('row_number')

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
    list_display = ['trade_date_color', 'stock_code', 'stock_name', 'vol_ratio_color', 'vol_ratio_oa_color', 'open_price', 'profit_chg_color', 'cap', 'gap_type_color', 'cond_name', 'concept', 'is_ops', 'profit_chg_close', 'update_datetime']
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

    profit_chg_color.short_description = '竞价涨幅'

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
xadmin.site.register(StockLimitUpAuctionReal, StockLimitUpAuctionRealAdmin)
xadmin.site.register(StockAuctionConditions, StockAuctionConditionsAdmin)


