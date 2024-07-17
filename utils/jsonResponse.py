#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-15
# @Desc :自定义的JsonResponse文件
from rest_framework.response import Response


class BaseResponse(Response):
    """
    基础响应类，定义通用的响应结构
    """

    def __init__(self, code, data=None, msg='success', status=None, template_name=None, headers=None, exception=False, content_type=None):
        std_data = {
            "code": code,
            "data": data,
            "msg": msg
        }
        super().__init__(std_data, status, template_name, headers, exception, content_type)


class SuccessResponse(BaseResponse):
    """
    标准响应成功的返回, SuccessResponse(data)或者SuccessResponse(data=data)
    - 默认code返回2000, 不支持指定其他返回码
    """

    def __init__(self, data=None, msg='success', status=None, template_name=None, headers=None, exception=False, content_type=None, page=1, limit=1, total=None):
        total = total if data else 0
        data = {
            "page": page,
            "limit": limit,
            "total": total,
            "data": data
        }
        super().__init__(2000, data, msg, status, template_name, headers, exception, content_type)


class DetailResponse(BaseResponse):
    """
    不包含分页信息的接口返回, 主要用于单条数据查询
    - 默认code返回2000, 不支持指定其他返回码
    """

    def __init__(self, data=None, msg='success', status=None, template_name=None, headers=None, exception=False, content_type=None):
        super().__init__(2000, data, msg, status, template_name, headers, exception, content_type)


class ErrorResponse(BaseResponse):
    """
    标准响应错误的返回, ErrorResponse(msg='xxx')
    - 默认错误码返回400, 也可以指定其他返回码: ErrorResponse(code=xxx)
    """

    def __init__(self, msg='error', code=400, data=None, status=None, template_name=None, headers=None, exception=False, content_type=None):
        super().__init__(code, data, msg, status, template_name, headers, exception, content_type)

# from rest_framework.response import Response
#
#
# class SuccessResponse(Response):
#     """
#     标准响应成功的返回, SuccessResponse(data)或者SuccessResponse(data=data)
#         -默认code返回2000, 不支持指定其他返回码
#     """
#
#     def __init__(
#             self, data=None,
#             msg='success',
#             status=None,
#             template_name=None,
#             headers=None,
#             exception=False,
#             content_type=None,
#             page=1,
#             limit=1,
#             total=1
#     ):
#         if not data:
#             total = 0
#         std_data = {
#             "code": 2000,
#             "data": {
#                 "page": page,
#                 "limit": limit,
#                 "total": total,
#                 "data": data
#             },
#             "msg": msg
#         }
#         super().__init__(std_data, status, template_name, headers, exception, content_type)
#
#
# class DetailResponse(Response):
#     """
#     不包含分页信息的接口返回,主要用于单条数据查询
#     - 默认code返回2000, 不支持指定其他返回码
#     """
#
#     def __init__(
#             self,
#             data=None,
#             msg='success',
#             status=None,
#             template_name=None,
#             headers=None,
#             exception=False,
#             content_type=None
#     ):
#         std_data = {
#             "code": 2000,
#             "data": data,
#             "msg": msg
#         }
#         super().__init__(std_data, status, template_name, headers, exception, content_type)
#
#
# class ErrorResponse(Response):
#     """
#     标准响应错误的返回,ErrorResponse(msg='xxx')
#     - 默认错误码返回400, 也可以指定其他返回码:ErrorResponse(code=xxx)
#     """
#
#     def __init__(self,
#                  data=None,
#                  msg='error',
#                  code=400,
#                  status=None,
#                  template_name=None,
#                  headers=None,
#                  exception=False,
#                  content_type=None
#                  ):
#         std_data = {
#             "code": code,
#             "data": data,
#             "msg": msg
#         }
#         super().__init__(std_data, status, template_name, headers, exception, content_type)
