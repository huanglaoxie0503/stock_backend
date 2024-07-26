#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-17
# @Desc :
import xadmin
from apps.base_data.models import TradingVolume
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "涨停宝后台"
    site_footer = "stock"
    menu_style = "accordion"


class VerifyCodeAdmin(object):
    list_display = ['code', 'mobile', "create_datetime"]


class TradingVolumeAdmin(object):
    list_display = ['trade_date', 'total_market', 'sh_market', 'sz_market']
    list_filter = ['trade_date']
    search_fields = ['trade_date']
    ordering = ['-trade_date']
    model_icon = 'fa fa-cube'
    list_per_page = 10
    list_display_links = ['trade_date']
    list_editable = []


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(TradingVolume, TradingVolumeAdmin)
