#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-17
# @Desc :
import xadmin
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


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
