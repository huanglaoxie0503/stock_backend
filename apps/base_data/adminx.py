#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-31
# @Desc :
from datetime import datetime

import xadmin
from utils.common import format_color

from utils.models import BaseQueryAdmin, BaseColorAdmin
from apps.base_data.models import (
    TradingVolume,
    StockLimitUpDetail,
    StockLimitDownDetail,
    StockLimitBlast,
    StockTradeCalendar,
    StockConditionalPicker,
    ConceptHistoryMaxLimitUp,
    DailyConceptLeaders
)


class StockLimitUpDetailAdmin(BaseQueryAdmin):
    list_display = ['trade_date', 'stock_code', 'stock_name', 'limit_up_days_color', 'fund_attitude_score_color', 'cap', 'limit_up_reasons_hot', 'limit_up_reasons', 'limit_up_type', 'first_limit_up_time', 'cb', 'update_datetime']
    list_filter = ['trade_date', 'stock_code', 'stock_name', 'limit_up_reasons_hot', 'limit_up_reasons']
    search_fields = ['trade_date', 'stock_code', 'stock_name', 'limit_up_reasons_hot', 'limit_up_reasons']
    ordering = ['-limit_up_days']
    model_icon = 'fa fa-database'
    # list_per_page = 15
    list_display_links = ['trade_date']
    list_editable = ['limit_up_reasons_hot']

    def queryset(self):
        qs = super().queryset()
        # 根据日期字段进行排序，并只取最新日期的数据
        latest_date = qs.latest('trade_date').trade_date
        return qs.filter(trade_date=latest_date)

    def limit_up_days_color(self, obj):
        thresholds = [
            lambda x: x >= 2
        ]
        colors = ['red']
        return format_color(obj.limit_up_days, thresholds, colors)
    limit_up_days_color.short_description = '连板数'

    def fund_attitude_score_color(self, obj):
        thresholds = [
            lambda x: x >= 10
        ]
        colors = ['red']
        return format_color(obj.fund_attitude_score, thresholds, colors)

    fund_attitude_score_color.short_description = '资金态度'


class StockLimitDownDetailAdmin(BaseQueryAdmin):
    list_display = ['trade_date', 'stock_code', 'stock_name', 'limit_down_type', 'limit_down_amount',
                    'limit_down_volume', 'limit_down_days', 'limit_down_time', 'latest_chg', 'limit_down_reason']
    list_filter = ['trade_date']
    search_fields = ['trade_date']
    ordering = ['-trade_date']
    model_icon = 'fa fa-cube'
    list_per_page = 15
    list_display_links = ['trade_date']
    list_editable = []


class StockLimitBlastAdmin(BaseQueryAdmin):
    list_display = ['trade_date', 'stock_code', 'stock_name', 'limit_up_price','pre_close', 'latest_chg', 'volume', 'limit_up_opened_cnt', 'concept']
    list_filter = ['trade_date']
    search_fields = ['trade_date']
    ordering = ['-trade_date']
    model_icon = 'fa fa-cube'
    list_editable = ['concept']
    list_per_page = 15


class TradingVolumeAdmin(BaseColorAdmin):
    list_display = ['trade_date_color', 'total_market', 'sh_market', 'sz_market']
    list_filter = ['trade_date']
    search_fields = ['trade_date']
    ordering = ['-trade_date']
    list_per_page = 15
    list_display_links = ['trade_date']
    list_editable = []
    model_icon = 'fa fa-cube'


class StockTradeCalendarAdmin(BaseColorAdmin):
    list_display = ['trade_date_color', 'market_color', 'trade_month']
    list_filter = ['trade_date']
    search_fields = ['trade_date']
    ordering = ['-trade_date']
    readonly_fields = ['trade_date']
    list_per_page = 15
    list_display_links = ['trade_date']
    model_icon = 'fa fa-cube'

    def queryset(self):
        current_year_month = datetime.now().strftime('%Y-%m')
        qs = StockTradeCalendar.objects.all()
        # 打印 QuerySet 中的每一个对象
        # 使用 filter 进行查询
        data = qs.filter(trade_month=current_year_month)
        return data

    # 自定义字段内容颜色
    def market_color(self, obj):
        thresholds = [
            lambda x: x == 1,
            lambda x: x == 0
        ]
        colors = ['red', 'green']
        return format_color(obj.market_open, thresholds, colors)

    market_color.short_description = '是否开市'


class StockConditionalPickerAdmin(BaseQueryAdmin):
    list_display = ['trade_date', 'stock_code', 'stock_name', 'cond_name', 'pre_close', 'high_price', 'chg', 'cap',
                    'volume', 'concept', 'update_datetime']
    list_filter = ['trade_date', 'stock_code', 'stock_name', 'cond_name', 'concept']
    search_fields = ['trade_date', 'stock_code', 'stock_name', 'cond_name', 'concept']
    ordering = ['-trade_date']
    list_per_page = 15
    list_display_links = ['trade_date']
    list_editable = ['concept']
    model_icon = 'fa fa-cube'


class ConceptHistoryMaxLimitUpAdmin(object):
    list_display = ['trade_date', 'stock_code', 'stock_name', 'concept', 'max_limit_up_days', 'related_data_breakthrough'
        ,'related_data_broken','related_data_suppression', 'create_datetime']
    list_filter = ['trade_date', 'stock_code', 'stock_name', 'concept', 'max_limit_up_days']
    search_fields = ['trade_date', 'stock_code', 'stock_name', 'concept', 'max_limit_up_days']
    ordering = ['-trade_date', '-max_limit_up_days']
    list_per_page = 15
    list_display_links = ['trade_date']
    list_editable = ['concept']
    model_icon = 'fa fa-cube'


class DailyConceptLeadersAdmin(object):
    list_display = ['trade_date', 'stock_code', 'stock_name', 'concept', 'highest_limit_up_days', 'stock_count', 'create_datetime']
    list_filter = ['trade_date', 'stock_code', 'stock_name', 'concept', 'highest_limit_up_days', 'stock_count']
    search_fields = ['trade_date', 'stock_code', 'stock_name', 'concept', 'highest_limit_up_days', 'stock_count']
    ordering = ['-trade_date', '-stock_count']
    list_per_page = 15
    list_display_links = ['trade_date']
    list_editable = ['concept']
    model_icon = 'fa fa-cube'


xadmin.site.register(StockLimitUpDetail, StockLimitUpDetailAdmin)
xadmin.site.register(StockLimitDownDetail, StockLimitDownDetailAdmin)
xadmin.site.register(StockLimitBlast, StockLimitBlastAdmin)
xadmin.site.register(StockConditionalPicker, StockConditionalPickerAdmin)
xadmin.site.register(ConceptHistoryMaxLimitUp, ConceptHistoryMaxLimitUpAdmin)
xadmin.site.register(DailyConceptLeaders, DailyConceptLeadersAdmin)
xadmin.site.register(TradingVolume, TradingVolumeAdmin)
xadmin.site.register(StockTradeCalendar, StockTradeCalendarAdmin)
