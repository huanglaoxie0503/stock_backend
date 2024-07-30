#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-17
# @Desc :
import xadmin
from xadmin import views

from apps.base_data.models import (
    TradingVolume,
    StockLimitUpDetail,
    StockLimitDownDetail,
    StockLimitBlast,
    StockTradeCalendar, StockConditionalPicker
)
from apps.stock_picker.models import (
    StockAuction,
    StockLimitUpAuction,
    StockAuctionConditions,
)


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True
    menu_order = 100  # 数字越小，越靠前


class GlobalSettings(object):
    site_title = "涨停宝后台"
    site_footer = "stock"
    menu_style = "accordion"


class StockLimitUpDetailAdmin(object):
    list_display = ['trade_date', 'stock_code', 'stock_name', 'limit_up_type', 'limit_up_amount', 'limit_up_volume',
                    'limit_up_days', 'limit_up_opening_nums', 'limit_up_reasons', 'limit_up_reasons_hot',
                    'first_limit_up_time', 'last_limit_up_time', 'latest_price', 'latest_chg']
    list_filter = ['trade_date']
    search_fields = ['trade_date']
    ordering = ['-trade_date']
    model_icon = 'fa fa-cube'
    list_per_page = 15
    list_display_links = ['trade_date']
    list_editable = ['limit_up_reasons_hot']


class StockLimitDownDetailAdmin(object):
    list_display = ['trade_date', 'stock_code', 'stock_name', 'limit_down_type', 'limit_down_amount',
                    'limit_down_volume', 'limit_down_days', 'limit_down_reason', 'limit_down_time', 'latest_chg']
    list_filter = ['trade_date']
    search_fields = ['trade_date']
    ordering = ['-trade_date']
    model_icon = 'fa fa-cube'
    list_per_page = 20
    list_display_links = ['trade_date']
    list_editable = []


class StockLimitBlastAdmin(object):
    list_display = ['trade_date', 'stock_code', 'stock_name', 'has_limit_up', 'limit_up_duration', 'limit_up_price',
                    'pre_close', 'latest_chg', 'volume', 'limit_up_opened_cnt']
    list_filter = ['trade_date']
    search_fields = ['trade_date']
    ordering = ['-trade_date']
    model_icon = 'fa fa-cube'
    list_per_page = 20


class TradingVolumeAdmin(object):
    list_display = ['trade_date', 'total_market', 'sh_market', 'sz_market']
    list_filter = ['trade_date']
    search_fields = ['trade_date']
    ordering = ['-trade_date']
    list_per_page = 10
    list_display_links = ['trade_date']
    list_editable = []
    model_icon = 'fa fa-cube'


class StockTradeCalendarAdmin(object):
    list_display = ['trade_date', 'market_open', 'trade_month']
    list_filter = ['trade_date']
    search_fields = ['trade_date']
    ordering = ['-trade_date']
    readonly_fields = ['trade_date']
    list_per_page = 10
    list_display_links = ['trade_date']
    model_icon = 'fa fa-cube'


class StockConditionalPickerAdmin(object):
    list_display = ['trade_date', 'stock_code', 'stock_name', 'cond_name', 'pre_close', 'high_price', 'chg', 'cap', 'volume', 'concept']
    list_filter = ['trade_date']
    search_fields = ['trade_date']
    ordering = ['-trade_date']
    list_per_page = 10
    list_display_links = ['trade_date']
    list_editable = []
    model_icon = 'fa fa-cube'


class StockAuctionAdmin(object):
    list_display = ['trade_date', 'stock_code', 'stock_name', 'latest_price', 'limit_up_order_amount', 'cap', 'limit_up_reason']
    list_filter = ['trade_date', 'stock_code', 'stock_name']
    search_fields = ['trade_date', 'stock_code', 'stock_name']
    ordering = ['-trade_date']
    list_per_page = 10
    list_display_links = ['trade_date']
    list_editable = []
    model_icon = 'fa fa-cube'


class StockLimitUpAuctionAdmin(object):
    list_display = ['trade_date', 'stock_code', 'stock_name', 'open_price', 'pre_close', 'pre_open_vol_ratio', 'pre_open_max_vol_ratio', 'auction_amount', 'auction_volume', 'pre_max_volume', 'pre_volume', 'limit_up_opening_nums', 'last_limit_up_time', 'limit_up_reasons', 'limit_up_days', 'model_name', 'cap', 'cb', 'is_ops', 'profit_chg', 'profit_chg_close']
    list_filter = ['trade_date', 'stock_code', 'stock_name', 'is_ops']
    search_fields = ['trade_date', 'stock_code', 'stock_name', 'is_ops']
    ordering = ['-trade_date']
    list_per_page = 10
    list_display_links = ['trade_date']
    list_editable = []
    model_icon = 'fa fa-cube'


class StockAuctionConditionsAdmin(object):
    list_display = ['trade_date', 'stock_code', 'stock_name', 'open_price', 'pre_close', 'high_price', 'pre_open_vol_ratio', 'pre_open_max_vol_ratio', 'auction_volume', 'pre_max_volume', 'pre_volume', 'auction_amount', 'cap', 'gap_type', 'cond_name', 'concept', 'is_ops', 'profit_chg', 'profit_chg_close']
    list_filter = ['trade_date', 'stock_code', 'stock_name', 'is_ops', 'gap_type', 'is_ops']
    search_fields = ['trade_date', 'stock_code', 'stock_name', 'is_ops', 'gap_type', 'is_ops']
    ordering = ['-trade_date']
    model_icon = 'fa fa-cube'
    list_per_page = 10
    list_display_links = ['trade_date']
    list_editable = []


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
# 第三方应用
xadmin.site.register(StockLimitUpDetail, StockLimitUpDetailAdmin)
xadmin.site.register(StockLimitDownDetail, StockLimitDownDetailAdmin)
xadmin.site.register(StockLimitBlast, StockLimitBlastAdmin)
xadmin.site.register(StockConditionalPicker, StockConditionalPickerAdmin)
xadmin.site.register(TradingVolume, TradingVolumeAdmin)
xadmin.site.register(StockTradeCalendar, StockTradeCalendarAdmin)

xadmin.site.register(StockAuction, StockAuctionAdmin)
xadmin.site.register(StockLimitUpAuction, StockLimitUpAuctionAdmin)
xadmin.site.register(StockAuctionConditions, StockAuctionConditionsAdmin)
