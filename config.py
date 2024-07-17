#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-16
# @Desc :
DEBUG = True  # 是否调试模式
IS_DEMO = False  # 是否演示模式（演示模式只能查看无法保存、编辑、删除、新增）
IS_SINGLE_TOKEN = False  # 是否只允许单用户单一地点登录(只有一个人在线上)(默认多地点登录),只针对后台用户生效
# 表前缀
TABLE_PREFIX = "stock_"
# 手机号码正则表达式
REGEX_MOBILE = r"^1([358][0-9]|4[579]|66|7[0135678]|9[89])[0-9]{8}$"

# ===============MySQL 数据库 配置=============== #
# 数据库地址
DATABASE_ENGINE = "django.db.backends.mysql"
# 数据库地址
DATABASE_HOST = "127.0.0.1"
# 数据库端口
DATABASE_PORT = 3306
# 数据库用户名
DATABASE_USER = "root"
# 数据库密码
DATABASE_PASSWORD = "oscar&0503"
# 数据库名
DATABASE_NAME = "stock_data"
# 数据库编码
DATABASE_CHARSET = "utf8mb4"
# 数据库长连接时间（默认为0，单位秒）即每次请求都重新连接,debug模式下该值应该写为0 ，mysql默认长连接超时时间为8小时
DATABASE_CONN_MAX_AGE = 0  # 推荐120（2分钟），使用 None 则是无限的持久连接（不推荐）。

REDIS_PASSWORD = 'oscar&0503'
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_URL = f'redis://:{REDIS_PASSWORD or ""}@{REDIS_HOST}:{REDIS_PORT}'
