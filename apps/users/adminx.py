#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-17
# @Desc :
import xadmin
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True
    menu_order = 100  # 数字越小，越靠前


class GlobalSettings(object):
    site_title = "涨停宝后台"
    site_footer = "stock"
    menu_style = "accordion"


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)



