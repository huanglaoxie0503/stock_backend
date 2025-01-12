#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-26
# @Desc :
import ast
from django.http import QueryDict
from django.utils.html import format_html
from rest_framework.request import Request


# 通用的颜色格式化函数
def format_color(value, thresholds, colors):
    """
    根据指定的阈值和颜色列表，返回带颜色且根据条件加粗的 HTML 格式化字符串。

    :param value: 需要格式化的值
    :param thresholds: 用于判断的阈值列表，每个阈值是一个 lambda 表达式
    :param colors: 与阈值对应的颜色列表
    :return: 带颜色且根据条件加粗的 HTML 格式化字符串
    """
    if value is None:
        return '-'

    for threshold, color in zip(thresholds, colors):
        if threshold(value):
            return format_html(
                '<span style="color:{}; font-weight:bold;">{}</span>',
                color,
                value,
            )

    # 默认情况下仅使用黑色，不加粗
    return format_html(
        '<span style="color:black;">{}</span>',
        value,
    )


def ast_convert(ast_str):
    if ast_str:
        try:
            my_object = ast.literal_eval(ast_str)
            return my_object
        except Exception as e:
            print(e)
            return ast_str

    return None


def get_parameter_dic(request, *args, **kwargs):
    """
    获取get 或 post的参数
        get_parameter_dic(request)['name'] ：name为获取的参数名 ,此种方式获取name不存在则会报错返回name表示name不存在，需要此参数
        get_parameter_dic(request).get('name') ：name为获取的参数名 ,此种方式获取name不存在不会报错，不存在会返回None
    :param request:Request
    :param args:
    :param kwargs:
    :return:
    """
    if not isinstance(request, Request):
        return {}

    query_params = request.query_params
    if isinstance(query_params, QueryDict):
        query_params = query_params.dict()
    result_data = request.data
    if isinstance(result_data, QueryDict):
        result_data = result_data.dict()

    if query_params != {}:
        return query_params
    else:
        return result_data
