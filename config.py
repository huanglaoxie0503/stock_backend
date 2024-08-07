#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-16
# @Desc :
import os
import platform
import subprocess


# ===============MySQL 数据库 配置=============== #
def load_env_from_bash_profile():
    command = 'source ~/.bash_profile && env'
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, executable='/bin/bash')
    for line in proc.stdout:
        (key, _, value) = line.decode('utf-8').partition('=')
        os.environ[key.strip()] = value.strip()


if platform.system() == 'Darwin':
    load_env_from_bash_profile()

# 数据库地址
DATABASE_ENGINE = "django.db.backends.mysql"
# 数据库地址
DATABASE_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
# 数据库端口
DATABASE_PORT = os.getenv('MYSQL_PORT', 3306)
# 数据库用户名
DATABASE_USER = os.getenv('MYSQL_USER', 'root')
# 数据库密码
DATABASE_PASSWORD = os.getenv('MYSQL_PASSWORD', 'oscar&0503')
# 数据库名
DATABASE_NAME = os.getenv('MYSQL_DB', 'stock_data')
# 数据库编码
DATABASE_CHARSET = os.getenv('MYSQL_CHARSET', 'utf8mb4')
# 数据库长连接时间（默认为0，单位秒）即每次请求都重新连接,debug模式下该值应该写为0 ，mysql默认长连接超时时间为8小时
DATABASE_CONN_MAX_AGE = 120  # 推荐120（2分钟），使用 None 则是无限的持久连接（不推荐）。

# ======================Redis 配置=========================== #
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', 'oscar&0503')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_URL = f'redis://:{REDIS_PASSWORD or ""}@{REDIS_HOST}:{REDIS_PORT}'

# ====================== 阿里云发送短信 配置=========================== #
ALI_YUN_SMS_ACCESS_KEY_ID = ""
ALI_YUN_SMS_ACCESS_KEY_SECRET = ""
ALI_YUN_SMS_SIGN = '测试'  # 短信签名名称
ALI_YUM_SMS_TEMPLATE = 'SMS_302035344'  # 模板code

# ====================== 系统 配置=========================== #
DEBUG = True  # 是否调试模式
IS_DEMO = False  # 是否演示模式（演示模式只能查看无法保存、编辑、删除、新增）
IS_SINGLE_TOKEN = False  # 是否只允许单用户单一地点登录(只有一个人在线上)(默认多地点登录),只针对后台用户生效
# 表前缀
TABLE_PREFIX = "stock_"
# 手机号码正则表达式
REGEX_MOBILE = r"^1([358][0-9]|4[579]|66|7[0135678]|9[89])[0-9]{8}$"
