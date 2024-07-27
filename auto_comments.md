### Django 项目中使用“添加表和字段注释”管理命令的文档

#### 一、概述
用户如何在 Django 项目中根据模型中的 `verbose_name` 属性自动添加数据库表和字段注释。此功能有助于提高数据库的可读性和维护性，并在某些数据库工具中直接展示字段的意义，从而提高开发效率。

#### 二、准备工作
1. **环境准备**：
   - 确保 Django 项目环境已搭建完成，并且项目中至少有一个应用（app）。
   - 数据库必须支持 UTF-8 编码，以正确存储和显示中文字符。

2. **数据库配置**：
   - 确认你的数据库配置（位于 `settings.py` 文件中）使用了正确的字符集：
     - 对于 MySQL：`'ENGINE': 'django.db.backends.mysql'`，`'OPTIONS': {'charset': 'utf8mb4'}`。
     - 对于 PostgreSQL：`'ENGINE': 'django.db.backends.postgresql'`。

#### 三、安装与配置
1. **创建管理命令**：
- 在你的 Django 应用目录下的 `auto_add_comments/management/commands` 目录(package)中，创建一个名为 `add_comments.py` 的文件（如果目录不存在，请创建）。
 ```
stock_backend/
    auto_add_comments/
        __init__.py
        management/
            __init__.py
            commands/
                __init__.py
                add_comments.py
    stock_backend/
        __init__.py
        settings.py
        urls.py
        wsgi.py
        ...
    manage.py
```

  - 将以下代码复制到 `add_comments.py` 文件中：
```python
#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-27
# @Desc :
from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS, connections
from django.apps import apps
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    # 帮助信息，描述命令的功能
    help = '修改数据库表字段的注释，使其与模型的verbose_name一致'

    def add_arguments(self, parser):
        # 添加命令行参数，允许指定数据库
        parser.add_argument(
            '--database',
            default=DEFAULT_DB_ALIAS,
            help='指定要操作的数据库，默认为"default"数据库',
        )

    def handle(self, *args, **options):
        # 连接到数据库
        connection = self.get_db_connection(options)
        try:
            with connection.cursor() as cursor:
                # 获取所有自定义的模型
                models = apps.get_models()
                custom_models = [model for model in models if 'django.contrib' not in str(model)]
                # 确定数据库类型
                connection_type_info = str(connection)
                processed = False
                # 根据数据库类型调用相应的注释添加方法
                if "mysql" in connection_type_info:
                    self.add_comments(cursor, connection, custom_models, self.mysql_add_comment)
                    processed = True
                elif "postgresql" in connection_type_info:
                    self.add_comments(cursor, connection, custom_models, self.postgresql_add_comment)
                    processed = True
                if not processed:
                    # 如果数据库类型不支持，则输出错误信息
                    self.stdout.write(f"不支持的数据库类型: {connection_type_info}，当前只支持MySQL和PostgreSQL")
        finally:
            # 关闭数据库连接
            connection.close()

    def get_db_connection(self, options):
        # 获取数据库连接
        database = options['database']
        connection = connections[database]
        connection.prepare_database()
        return connection

    def is_field_type_to_be_processed(self, field):
        # 判断字段类型是否需要处理
        return field.get_internal_type() not in ["AutoField", "ForeignKey"]

    def get_comment_text(self, field, db_column):
        # 获取字段注释文本
        comment_text = field.verbose_name or field.help_text
        if not comment_text or comment_text == db_column.replace("_", " ").strip():
            return None
        return comment_text

    def add_comments(self, cursor, connection, custom_models, add_comment_method):
        # 处理所有模型，添加注释
        processed_tables = set()
        for modelobj in custom_models:
            if not modelobj._meta.managed:
                continue
            table_name = modelobj._meta.db_table
            if table_name in processed_tables:
                continue
            # 调用特定数据库类型的注释添加方法
            add_comment_method(cursor, connection, modelobj)
            processed_tables.add(table_name)
            # 提交事务
            connection.commit()

    def mysql_add_comment(self, cursor, connection, modelobj):
        # 为MySQL数据库添加注释
        table_name = modelobj._meta.db_table
        fields = modelobj._meta.fields
        for field in fields:
            db_column = field.db_column or field.name
            if not self.is_field_type_to_be_processed(field):
                continue
            comment_text = self.get_comment_text(field, db_column)
            if not comment_text:
                continue
            try:
                # 使用参数化查询防止SQL注入
                cursor.execute(
                    f"ALTER TABLE `{table_name}` MODIFY COLUMN `{db_column}` {field.db_type(connection)} COMMENT %s;",
                    (comment_text,))
                # 输出成功信息
                self.stdout.write(f"已为{table_name}.{db_column}添加注释: {comment_text}")
            except Exception as e:
                # 记录错误信息
                logger.error(f"未能为{table_name}.{db_column}添加注释: {e}")

        # 添加表注释
        table_comment = modelobj._meta.verbose_name
        if table_comment:
            try:
                cursor.execute(f"ALTER TABLE `{table_name}` COMMENT=%s;", (table_comment,))
                self.stdout.write(f"已为表{table_name}添加注释: {table_comment}")
            except Exception as e:
                logger.error(f"未能为表{table_name}添加注释: {e}")

    def postgresql_add_comment(self, cursor, connection, modelobj):
        # 为PostgreSQL数据库添加注释
        table_name = modelobj._meta.db_table
        fields = modelobj._meta.fields
        for field in fields:
            db_column = field.db_column or field.name
            if not self.is_field_type_to_be_processed(field):
                continue
            comment_text = self.get_comment_text(field, db_column)
            if not comment_text:
                continue
            try:
                # 使用参数化查询防止SQL注入
                cursor.execute(f"COMMENT ON COLUMN {table_name}.{db_column} IS %s;", (comment_text,))
                # 输出成功信息
                self.stdout.write(f"已为{table_name}.{db_column}添加注释: {comment_text}")
            except Exception as e:
                # 记录错误信息
                logger.error(f"未能为{table_name}.{db_column}添加注释: {e}")

        # 添加表注释
        table_comment = modelobj._meta.verbose_name
        if table_comment:
            try:
                cursor.execute(f"COMMENT ON TABLE {table_name} IS %s;", (table_comment,))
                self.stdout.write(f"已为表{table_name}添加注释: {table_comment}")
            except Exception as e:
                logger.error(f"未能为表{table_name}添加注释: {e}")
```

2. **配置数据库**：
   - 确保 `settings.py` 文件中的数据库配置正确，特别是字符集设置。

#### 四、使用说明
1. **运行命令**：
   - 打开终端，进入你的 Django 项目根目录。
   - 输入以下命令运行管理命令：
     ```bash
     python manage.py add_comments
     ```

2. **查看输出**：
   - 命令执行过程中，控制台会显示每一步的操作状态，包括成功添加注释的表和字段，以及任何遇到的错误。

#### 五、常见问题与解决方案
1. **问题：运行命令时遇到字符编码错误**。
   - **解决方案**：检查你的数据库配置和数据库本身的字符集设置，确保支持 UTF-8。

2. **问题：某些字段未被添加注释**。
   - **解决方案**：确认模型中的 `verbose_name` 属性已正确设置，且字段类型不是 `AutoField` 或 `ForeignKey`。

#### 六、注意事项
- 在生产环境中运行此命令前，强烈建议备份数据库，以防意外情况。
- 如果数据库中表和字段数量巨大，执行此命令可能耗时较长，需耐心等待。

#### 七、运行效果
```shell
(stock_backend) PS D:\projects\stock_backend> python manage.py add_comments                            
已为authtoken_token.key添加注释: 键
未能为authtoken_token.user添加注释: (1054, "Unknown column 'user' in 'authtoken_token'")
已为authtoken_token.created添加注释: 已创建
已为表authtoken_token添加注释: 令牌
已为表captcha_captchastore添加注释: captcha store
已为xadmin_bookmark.id添加注释: ID
已为xadmin_bookmark.title添加注释: 标题
已为xadmin_bookmark.url_name添加注释: URL名字
已为xadmin_bookmark.query添加注释: Query参数
已为xadmin_bookmark.is_share添加注释: 是否共享
已为表xadmin_bookmark添加注释: 书签
已为xadmin_usersettings.id添加注释: ID
已为xadmin_usersettings.key添加注释: 设置KEY
已为xadmin_usersettings.value添加注释: 设置内容
已为表xadmin_usersettings添加注释: 用户设置
已为xadmin_userwidget.id添加注释: ID
已为xadmin_userwidget.page_id添加注释: 页面
已为xadmin_userwidget.widget_type添加注释: Widget类型
已为xadmin_userwidget.value添加注释: Widget参数
已为表xadmin_userwidget添加注释: 用户小组件
已为xadmin_log.id添加注释: ID
已为xadmin_log.action_time添加注释: 操作时间
已为xadmin_log.ip_addr添加注释: 操作IP
已为xadmin_log.object_id添加注释: 对象id
已为xadmin_log.object_repr添加注释: 对象表示
已为xadmin_log.action_flag添加注释: 动作标志
已为xadmin_log.message添加注释: 修改消息
已为表xadmin_log添加注释: 日志记录
已为stock_users.password添加注释: 密码
已为stock_users.last_login添加注释: 上次登录
已为stock_users.is_superuser添加注释: 超级用户状态
已为stock_users.username添加注释: 用户名
已为stock_users.first_name添加注释: 名字
已为stock_users.last_name添加注释: 姓氏
已为stock_users.is_staff添加注释: 工作人员状态
已为stock_users.is_active添加注释: 有效
已为stock_users.date_joined添加注释: 加入日期
已为stock_users.user_id添加注释: UUID
已为stock_users.description添加注释: 描述
已为stock_users.create_datetime添加注释: 创建时间
已为stock_users.update_datetime添加注释: 修改时间
已为stock_users.name添加注释: 姓名
已为stock_users.mobile添加注释: 手机号码
已为stock_users.email添加注释: 邮箱
已为stock_users.birthday添加注释: 出生年月
已为stock_users.gender添加注释: 性别
已为stock_users.identity添加注释: 身份标识
已为stock_users.permissions添加注释: 权限列表
已为stock_users.is_delete添加注释: 是否逻辑删除
已为表stock_users添加注释: 用户表
已为users_counter.id添加注释: ID
已为表users_counter添加注释: counter
已为stock_trading_volume.create_datetime添加注释: 创建时间
已为stock_trading_volume.update_datetime添加注释: 更新时间
已为stock_trading_volume.trade_date添加注释: 交易日期
已为stock_trading_volume.sh_market添加注释: 沪市(亿)
已为stock_trading_volume.sz_market添加注释: 深市(亿)
已为stock_trading_volume.total_market添加注释: 两市总额(亿)
已为表stock_trading_volume添加注释: 两市成交额
```
