#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-24
# @Desc :
from enum import Enum


class StatusCodes(Enum):
    CONTINUE = 100  # 继续
    SWITCHING_PROTOCOLS = 101  # 切换协议
    PROCESSING = 102  # 处理 (WebDAV)

    OK = 200  # 请求成功
    CREATED = 201  # 已创建
    ACCEPTED = 202  # 已接受
    NON_AUTHORITATIVE_INFORMATION = 203  # 非权威信息
    NO_CONTENT = 204  # 无内容
    RESET_CONTENT = 205  # 重置内容
    PARTIAL_CONTENT = 206  # 部分内容
    MULTI_STATUS = 207  # 多状态 (WebDAV)
    ALREADY_REPORTED = 208  # 已报告 (WebDAV)
    IM_USED = 226  # IM Used (HTTP Delta encoding)

    MULTIPLE_CHOICES = 300  # 多种选择
    MOVED_PERMANENTLY = 301  # 永久移动
    FOUND = 302  # 临时移动 (以前叫做“Found”)
    SEE_OTHER = 303  # 查看其他
    NOT_MODIFIED = 304  # 未修改
    USE_PROXY = 305  # 使用代理
    TEMPORARY_REDIRECT = 307  # 临时重定向
    PERMANENT_REDIRECT = 308  # 永久重定向

    BAD_REQUEST = 400  # 错误请求
    UNAUTHORIZED = 401  # 未授权
    PAYMENT_REQUIRED = 402  # 需支付
    FORBIDDEN = 403  # 禁止
    NOT_FOUND = 404  # 未找到
    METHOD_NOT_ALLOWED = 405  # 方法不允许
    NOT_ACCEPTABLE = 406  # 不可接受
    PROXY_AUTHENTICATION_REQUIRED = 407  # 代理认证要求
    REQUEST_TIMEOUT = 408  # 请求超时
    CONFLICT = 409  # 冲突
    GONE = 410  # 已消失
    LENGTH_REQUIRED = 411  # 长度要求
    PRECONDITION_FAILED = 412  # 前提条件失败
    REQUEST_ENTITY_TOO_LARGE = 413  # 请求实体太大
    REQUEST_URI_TOO_LONG = 414  # 请求URI太长
    UNSUPPORTED_MEDIA_TYPE = 415  # 不支持的媒体类型
    REQUESTED_RANGE_NOT_SATISFIABLE = 416  # 请求范围不满足
    EXPECTATION_FAILED = 417  # 期望失败
    I_AM_A_TEAPOT = 418  # 我是一个茶壶 (RFC 2324)
    MISDIRECTED_REQUEST = 421  # 请求被误导向
    UNPROCESSABLE_ENTITY = 422  # 无法处理的实体 (WebDAV)
    LOCKED = 423  # 锁定 (WebDAV)
    FAILED_DEPENDENCY = 424  # 依赖失败 (WebDAV)
    TOO_EARLY = 425  # 太早 (RFC 8470)
    UPGRADE_REQUIRED = 426  # 升级要求
    PRECONDITION_REQUIRED = 428  # 前提条件要求
    TOO_MANY_REQUESTS = 429  # 请求过多
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431  # 请求头字段太大
    UNAVAILABLE_FOR_LEGAL_REASONS = 451  # 因法律原因不可用

    INTERNAL_SERVER_ERROR = 500  # 内部服务器错误
    NOT_IMPLEMENTED = 501  # 未实现
    BAD_GATEWAY = 502  # 错误网关
    SERVICE_UNAVAILABLE = 503  # 服务不可用
    GATEWAY_TIMEOUT = 504  # 网关超时
    HTTP_VERSION_NOT_SUPPORTED = 505  # HTTP版本不受支持
    VARIANT_ALSO_NEGOTIATES = 506  # 变体也协商 (Experimental)
    INSUFFICIENT_STORAGE = 507  # 存储不足 (WebDAV)
    LOOP_DETECTED = 508  # 循环检测 (WebDAV)
    NOT_EXTENDED = 510  # 未扩展
    NETWORK_AUTHENTICATION_REQUIRED = 511  # 网络认证要求


# HTTP_STATUS_CODES 字典用于映射 HTTP 状态码到其对应的描述性文本
# 这个字典在发送响应时很有用，可以提供给客户端更详细的错误或状态信息

HTTP_STATUS_CODES = {
    100: '继续',  # 客户端应继续发送请求的剩余部分
    101: '切换协议',  # 服务器将遵从客户端的Upgrade请求头升级到一个不同的协议
    102: '处理',  # 服务器已接受请求，正在处理，但处理还未完成（WebDAV）

    200: '成功',  # 请求已成功，信息已返回
    201: '已创建',  # 请求已成功，资源已创建
    202: '已接受',  # 服务器已接受请求，但尚未处理
    203: '非权威信息',  # 请求已成功，但是返回的信息可能来自另一来源
    204: '无内容',  # 服务器成功处理了请求，但没有返回任何内容
    205: '重置内容',  # 服务器成功处理了请求，但没有返回任何内容，告诉用户代理重置文档视图
    206: '部分内容',  # 服务器成功返回了部分内容
    207: '多状态',  # 服务器成功处理了多个独立的操作（WebDAV）
    208: '已报告',  # 已经报告了成员的当前状态（WebDAV）
    226: 'IM Used',  # 服务器支持Delta encoding

    300: '多种选择',  # 请求的资源有多个位置，服务器提供了多个选择链接
    301: '永久移动',  # 请求的资源已被永久移动到新位置
    302: '临时移动',  # 请求的资源已被临时移动到新位置
    303: '查看其他',  # 由于请求的资源引发了一个新的动作，所以应查看其他地址
    304: '未修改',  # 自从上次请求后，请求的资源未修改过
    305: '使用代理',  # 请求的资源必须通过代理访问
    307: '临时重定向',  # 请求的资源已被临时移动到新位置
    308: '永久重定向',  # 请求的资源已被永久移动到新位置

    400: '错误请求',  # 服务器无法理解请求的格式，客户端不应重复提交相同的请求
    401: '未授权',  # 请求需要用户的身份认证
    402: '需支付',  # 保留将来使用
    403: '禁止',  # 服务器理解请求客户端的请求，但是拒绝执行此请求
    404: '未找到',  # 服务器找不到请求的网页
    405: '方法禁用',  # 请求的方法与请求的资源不兼容
    406: '不接受',  # 请求的资源的内容特性无法满足请求头中的条件，因而无法生成响应实体
    407: '代理认证要求',  # 请求需要代理的身份认证
    408: '请求超时',  # 服务器等待请求时发生超时
    409: '冲突',  # 请求的资源与资源的当前状态发生冲突
    410: '已消失',  # 请求的资源在服务器上已经不再可用，而且没有任何已知的转发地址
    411: '长度要求',  # 服务器拒绝在没有定义Content-Length头的情况下接受请求
    412: '前提条件失败',  # 服务器在验证在请求的头字段中给出的前提条件后，未能满足其中一个前提条件
    413: '负载过大',  # 服务器拒绝处理请求，因为请求实体过大
    414: '请求URI过长',  # URI提供的信息超过了服务器的限制
    415: '不支持的媒体类型',  # 请求的格式不受请求页面的支持
    416: '请求范围不符合要求',  # 服务器无法满足请求者在请求头字段Range中指定的字节范围
    417: '期望失败',  # 服务器不能满足期望请求
    418: '我是一个茶壶',  # 一个非官方的HTTP状态码，通常用于表示客户端不应该尝试用错误的方法煮水
    421: '请求被误导向',  # 请求的目标提供了不一致的响应
    422: '无法处理的实体',  # 服务器理解请求的结构，但无法处理其实体（WebDAV）
    423: '锁定',  # 所请求的资源被锁定（WebDAV）
    424: '依赖失败',  # 由于前一请求出错，导致当前请求无法完成（WebDAV）
    425: '太早',  # 服务器不愿意冒险处理可能会被取消的请求（RFC 8470）
    426: '升级要求',  # 服务器拒绝提供请求的数据，除非终端设备升级
    428: '前提条件要求',  # 服务器要求请求者在请求中添加一个或多个前提条件
    429: '请求过多',  # 用户在给定的时间段内发起了太多的请求
    431: '请求头字段过大',  # 请求头字段的大小超过了服务器愿意解释的限制
    451: '因法律原因不可用',  # 服务器拒绝提供对请求页面的访问，因为合法的原因

    500: '内部服务器错误',  # 服务器遇到了一个未曾预料的状况，导致了它无法完成对请求的处理
    501: '未实现',  # 服务器不支持当前请求所需要的某个功能
    502: '错误网关',  # 作为网关或代理工作的服务器，从上游服务器收到了无效的响应
    503: '服务不可用',  # 服务器目前无法使用（由于超载或停机维护）
    504: '网关超时',  # 作为网关或代理工作的服务器，没有及时从上游服务器收到请求
    505: 'HTTP版本不受支持',  # 服务器不支持请求中所使用的HTTP协议版本
    506: '变体也协商',  # 服务器有一个由Range请求头字段指定的内部配置错误（实验性）
    507: '存储不足',  # 服务器无法存储完成请求所必需的内容（WebDAV）
    508: '循环检测',  # 服务器检测到一个无限循环的引用（WebDAV）
    510: '未扩展',  # 服务器不愿意使用客户端现有的内容协商能力
    511: '网络认证要求',  # 服务器要求用户代理进行身份验证，以便获取网络访问权限
}

