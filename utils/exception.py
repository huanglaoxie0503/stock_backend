#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-15
# @Desc :


class APIException(Exception):
    """
    通用异常:(1)用于接口请求是抛出移除, 此时code会被当做标准返回的code, message会被当做标准返回的msg
    """

    def __init__(self, code=201, message='API异常', args=('API异常',)):
        self.args = args
        self.code = code
        self.message = message

    def __str__(self):
        return self.message
