#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-17
# @Desc :
import xadmin
from xadmin import views


class BaseSetting(object):
    """
    全站的配置类, 配置主题
    """
    # 主题功能,enable_themes=True 表示要使用它的主题功能，xadmin默认是取消掉的,默认只有两个主题
    enable_themes = True
    # xadmin默认是取消掉的，显示更多主题，可以打开为True，然后会请求https://bootswatch.com/api/3.json，如果请求失败，就只会显示两个默认的
    use_bootswatch = True
    menu_order = 100  # 数字越小，越靠前


class GlobalSettings(object):
    # 设置站点标题
    # site_title = "涨停宝后台"
    site_title = "集合竞价后台"
    # 设置站点的页脚
    site_footer = "stock"
    # 设置菜单折叠
    menu_style = "accordion"
    # 控制是否显示书签功能
    show_bookmarks = True


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)



