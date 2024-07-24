#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-15
# @Desc :自定义的JsonResponse文件
from enum import Enum
from typing import Any, Optional, Dict, Union, List
from rest_framework.response import Response

from .codes import HTTP_STATUS_CODES, StatusCodes


class BaseResponse(Response):
    """
    基础响应类，用于构建所有API响应的基础结构。
    """

    def __init__(
            self,
            code: int,
            data: Optional[Any] = None,
            message: str = 'success',
            http_status: Optional[int] = None,
            template_name: Optional[str] = None,
            headers: Optional[Dict[str, str]] = None,
            exception: bool = False,
            content_type: Optional[str] = None
    ):
        response_data = {
            "code": code,
            "message": message,
            "data": data
        }
        http_status = http_status or HTTP_STATUS_CODES.get(code, 200)
        super().__init__(response_data, status=http_status, template_name=template_name, headers=headers,
                         exception=exception, content_type=content_type)


class SuccessResponse(BaseResponse):
    """
    成功响应类，用于构建成功的API响应。
    """

    def __init__(
            self,
            data: Optional[Any] = None,
            message: str = '操作成功',
            http_status: Optional[int] = None,
            template_name: Optional[str] = None,
            headers: Optional[Dict[str, str]] = None,
            exception: bool = False,
            content_type: Optional[str] = None
    ):
        # 设置响应状态码为成功
        code = StatusCodes.OK.value

        # 如果没有指定HTTP状态码，则使用默认的HTTP_OK
        http_status = http_status or HTTP_STATUS_CODES[200]

        # 调用基类构造函数
        super().__init__(
            code=code,
            data=data,
            message=message,
            http_status=http_status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type
        )


class ErrorResponse(BaseResponse):
    """
    错误响应类，用于构建错误的API响应。
    """

    def __init__(
            self,
            error_message: str,
            data: Optional[Any] = None,
            http_status: Optional[int] = None,
            template_name: Optional[str] = None,
            headers: Optional[Dict[str, str]] = None,
            exception: bool = False,
            content_type: Optional[str] = None
    ):
        # 设置响应状态码为错误
        code = StatusCodes.BAD_REQUEST.value

        # 如果没有指定HTTP状态码，则使用默认的HTTP_BAD_REQUEST
        http_status = http_status or HTTP_STATUS_CODES[400]

        # 调用基类构造函数
        super().__init__(
            code=code,
            data=data,
            message=error_message,
            http_status=http_status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type
        )


class DetailResponse(BaseResponse):
    """
    详情响应类，用于返回单条数据查询的结果。
    此类不包含分页信息，主要用于单条数据的查询响应。
    默认的code返回为Success (2000)，不支持指定其他返回码。
    """

    def __init__(self,
                 data: Optional[Any] = None,
                 msg: str = 'success',
                 status: Optional[int] = None,
                 template_name: Optional[str] = None,
                 headers: Optional[Dict[str, str]] = None,
                 exception: bool = False,
                 content_type: Optional[str] = None):
        # 使用枚举中的OK状态码作为默认code
        code = StatusCodes.OK.value

        # 调用基类构造函数，传入默认的code和其他参数
        super().__init__(code=code,
                         data=data,
                         message=msg,
                         http_status=status,
                         template_name=template_name,
                         headers=headers,
                         exception=exception,
                         content_type=content_type)


class NotFoundResponse(BaseResponse):
    """
    未找到响应类，用于构建资源未找到的API响应。
    """

    def __init__(
            self,
            not_found_message: str,
            data: Optional[Any] = None,
            http_status: Optional[int] = None,
            template_name: Optional[str] = None,
            headers: Optional[Dict[str, str]] = None,
            exception: bool = False,
            content_type: Optional[str] = None
    ):
        # 设置响应状态码为未找到
        code = StatusCodes.NOT_FOUND.value

        # 如果没有指定HTTP状态码，则使用默认的HTTP_NOT_FOUND
        http_status = http_status or HTTP_STATUS_CODES[404]

        # 调用基类构造函数
        super().__init__(
            code=code,
            data=data,
            message=not_found_message,
            http_status=http_status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type
        )
