#!/usr/bin/python
# -*- coding:UTF-8 -*-
"""
# @Time    :    2024-10-10 19:49
# @Author  :   oscar
# @Desc    :   None
"""
import xadmin
from django.utils.html import format_html

from apps.news.models import ClsNews


class ClsNewsAdmin(object):
    list_display = ['article_id', 'title', 'label', 'stock_code', 'stock_name', 'url_link', 'c_time']
    list_filter = ['article_id', 'title', 'label', 'stock_code', 'stock_name']
    search_fields = ['article_id', 'title', 'label', 'stock_code', 'stock_name']
    ordering = ['-c_time']
    # model_icon = 'fa fa-newspaper'
    model_icon = 'fa fa-bullhorn'
    list_editable = ['label']

    # 调整字段的列宽和对齐
    list_display_links = ('article_id', 'title')  # 设置点击哪些字段可以进入详情页
    list_display_style = 'table'  # 使用表格布局

    # def queryset(self):
    #     qs = super().queryset()
    #     # 根据日期字段进行排序，并只取最新日期的数据
    #     latest_date = qs.latest('c_time').c_time
    #     return qs.filter(c_time=latest_date)

    def url_link(self, obj):
        # URL 只显示简短版本，完整链接作为提示
        return format_html('<a href="{}" title="{}" target="_blank">{}</a>', obj.url, obj.url, obj.url[:30] + '...')

    url_link.short_description = 'URL'  # 列标题

xadmin.site.register(ClsNews, ClsNewsAdmin)