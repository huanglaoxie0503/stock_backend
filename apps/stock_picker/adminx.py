#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-31
# @Desc :
import xadmin
from datetime import datetime

from django.utils.html import format_html

from apps.stock_picker.models import (
    StockAuction,
    StockTwoToThree,
    StockLimitUpAuction,
    StockAuctionConditions,
    AuctionAggressiveBuyingDetail
)
from utils.common import format_color
from utils.models import BaseColorAdmin


class StockAuctionAdmin(object):
    list_display = ['trade_date_color', 'stock_code', 'stock_name', 'limit_up_order_amount', 'vol_diff_20_25',
                    'vol_diff_24_25', 'cap', 'latest_price', 'limit_up_reason', 'update_datetime']
    list_filter = ['trade_date', 'stock_code', 'stock_name']
    search_fields = ['trade_date', 'stock_code', 'stock_name']
    ordering = ['-limit_up_order_amount']
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


class StockLimitUpAuctionAdminOneToTwoAdmin(object):
    list_display = ['trade_date_color', 'stock_code', 'stock_name', 'vol_ratio_color',
                    'vol_ratio_oa_color', 'fund_attitude_score', 'cap_color', 'vol_diff_20_25', 'vol_diff_24_25',
                    'profit_chg',
                    'limit_up_reasons', 'model_name', 'profit_chg_close', 'limit_up_days', 'is_ops', 'update_datetime']
    list_filter = ['trade_date', 'stock_code', 'stock_name', 'is_ops', 'limit_up_days', 'limit_up_reasons']
    search_fields = ['trade_date', 'stock_code', 'stock_name', 'is_ops', 'limit_up_days', 'limit_up_reasons']
    # 排序字段
    ordering = ['-trade_date', '-limit_up_days', '-vol_diff_20_25']
    list_per_page = 15
    list_display_links = ['trade_date']
    list_editable = []
    model_icon = 'fa fa-thumbs-o-up'

    def queryset(self):
        qs = super().queryset()
        # 根据日期字段进行排序，并只取最新日期的数据
        latest_date = qs.latest('trade_date').trade_date
        # 添加 cap__lte=30 条件到过滤器中
        return qs.filter(
            trade_date=latest_date,
            limit_up_days=1,
            cb__isnull=True,
            cap__lte=30  # lte 表示小于等于 (less than or equal to)
        )

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


class StockTwoToThreeAdmin(object):
    list_display = ['trade_date_color', 'stock_code', 'stock_name', 'vol_ratio_color',
                    'vol_ratio_oa_color', 'fund_attitude_score', 'cap_color', 'vol_diff_20_25', 'vol_diff_24_25',
                    'profit_chg',
                    'limit_up_reasons', 'model_name', 'profit_chg_close', 'limit_up_days', 'is_ops', 'update_datetime']
    list_filter = ['trade_date', 'stock_code', 'stock_name', 'is_ops', 'limit_up_days', 'limit_up_reasons']
    search_fields = ['trade_date', 'stock_code', 'stock_name', 'is_ops', 'limit_up_days', 'limit_up_reasons']
    # 排序字段
    ordering = ['-trade_date', '-limit_up_days', '-vol_diff_20_25']
    list_per_page = 15
    list_display_links = ['trade_date']
    list_editable = []
    model_icon = 'fa fa-thumbs-o-up'

    def queryset(self):
        qs = super().queryset()
        # 根据日期字段进行排序，并只取最新日期的数据
        latest_date = qs.latest('trade_date').trade_date
        # 添加 cap__lte=30 条件到过滤器中
        return qs.filter(
            trade_date=latest_date,
            limit_up_days=2,
            cb__isnull=True,
            cap__lte=60  # lte 表示小于等于 (less than or equal to)
        )

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
    list_display = ['trade_date_color', 'stock_code', 'stock_name', 'vol_ratio_color', 'vol_ratio_oa_color',
                    'vol_diff_20_25', 'vol_diff_24_25', 'profit_chg_color', 'cap', 'gap_type_color', 'cond_name',
                    'concept', 'is_ops', 'profit_chg_close', 'update_datetime']
    list_filter = ['trade_date', 'stock_code', 'stock_name', 'is_ops', 'gap_type', 'is_ops', 'concept']
    search_fields = ['trade_date', 'stock_code', 'stock_name', 'is_ops', 'gap_type', 'is_ops', 'concept']
    ordering = ['-vol_diff_20_25', '-profit_chg']
    model_icon = 'fa fa-legal'
    list_per_page = 15
    list_display_links = ['trade_date']
    list_editable = []

    def queryset(self):
        qs = super().queryset()
        # 根据日期字段进行排序，并只取最新日期的数据
        latest_date = qs.latest('trade_date').trade_date
        # 按最新日期筛选数据，并按 limit_up_order_amount 字段倒序排序
        return qs.filter(trade_date=latest_date)

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


class AuctionAggressiveBuyingDetailAdmin(BaseColorAdmin):
    list_display = ['trade_date_color', 'stock_code', 'stock_name', 'vol_diff_20_25', 'vol_diff_24_25', 'chg_color',
                    'is_remark_color', 'vol_25', 'vol_24', 'vol_20', 'buy_1_vol', 'is_limit_up_color']
    list_filter = ['trade_date', 'stock_code', 'stock_name', 'is_limit_up']
    search_fields = ['trade_date', 'stock_code', 'stock_name']
    ordering = ['-vol_diff_20_25']
    model_icon = 'fa fa-heart'
    list_per_page = 20
    list_display_links = ['trade_date']
    list_editable = []

    def queryset(self):
        qs = super().queryset()

        # 根据日期字段进行排序，并只取最新日期的数据
        latest_date = qs.latest('trade_date').trade_date

        # 按最新日期筛选数据，并按 limit_up_order_amount 字段倒序排序
        # 添加过滤条件：open_chg（字符串类型）大于 "0"
        qs = qs.filter(trade_date=latest_date, open_chg__gt="0")

        return qs

    def trade_date_color(self, obj):
        current_date = datetime.now().date()
        thresholds = [
            lambda x: x == current_date
        ]
        colors = ['red']
        return format_color(obj.trade_date, thresholds, colors)

    trade_date_color.short_description = '交易日'

    def chg_color(self, obj):
        open_chg = obj.open_chg if obj.open_chg is not None else None

        # 确保 open_chg 是浮点数
        try:
            open_chg = float(open_chg) if open_chg is not None else None
        except ValueError:
            open_chg = None

        if open_chg == 0.00:
            color = 'gray'
            formatted_chg = "N/A"  # 显示为 N/A 或其他提示文字
        elif open_chg > 5:
            color = 'red'
            formatted_chg = f"{open_chg:.2f}%"
        elif 0 < open_chg <= 5:
            color = 'purple'
            formatted_chg = f"{open_chg:.2f}%"
        else:
            color = 'green'
            formatted_chg = f"{open_chg:.2f}%"

        return format_html('<span style="color: {};">{}</span>', color, formatted_chg)

    chg_color.short_description = '涨幅'

    def is_limit_up_color(self, obj):
        # 获取 is_limit_up 属性的值
        is_limit_up = getattr(obj, 'is_limit_up', None)

        # 根据 is_limit_up 的值设置颜色和显示的文字
        if is_limit_up == '涨停':
            color = 'red'
            formatted_text = "涨停"
        else:
            color = 'gray'
            formatted_text = "N/A"  # 或者你可以选择其他默认显示的文字

        return format_html('<span style="color: {};">{}</span>', color, formatted_text)

    # 设置短描述
    is_limit_up_color.short_description = '涨停状态'

    def is_remark_color(self, obj):
        # 获取 is_limit_up 属性的值
        remark = getattr(obj, 'remark', None)

        # 根据 is_limit_up 的值设置颜色和显示的文字
        if remark == '首板涨停':
            color = 'red'
            formatted_text = "首板"
        elif remark == '跌停':
            color = 'green'
            formatted_text = remark
        elif remark == '炸板':
            color = 'purple'
            formatted_text = remark
        else:
            color = 'gray'
            formatted_text = remark  # 或者你可以选择其他默认显示的文字

        return format_html('<span style="color: {};">{}</span>', color, formatted_text)

    # 设置短描述
    is_remark_color.short_description = '备注'


xadmin.site.register(StockAuction, StockAuctionAdmin)
xadmin.site.register(StockLimitUpAuction, StockLimitUpAuctionAdminOneToTwoAdmin)
xadmin.site.register(StockTwoToThree, StockTwoToThreeAdmin)
xadmin.site.register(StockAuctionConditions, StockAuctionConditionsAdmin)
xadmin.site.register(AuctionAggressiveBuyingDetail, AuctionAggressiveBuyingDetailAdmin)
