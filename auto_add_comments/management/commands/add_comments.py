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

    @staticmethod
    def get_db_connection(options):
        # 获取数据库连接
        database = options['database']
        connection = connections[database]
        connection.prepare_database()
        return connection

    @staticmethod
    def is_field_type_to_be_processed(field):
        # 判断字段类型是否需要处理
        return field.get_internal_type() not in ["AutoField", "ForeignKey"]

    @staticmethod
    def get_comment_text(field, db_column):
        # 获取字段注释文本
        comment_text = field.verbose_name or field.help_text
        if not comment_text or comment_text == db_column.replace("_", " ").strip():
            return None
        return comment_text

    @staticmethod
    def add_comments(cursor, connection, custom_models, add_comment_method):
        # 处理所有模型，添加注释
        processed_tables = set()
        for model_obj in custom_models:
            if not model_obj._meta.managed:
                continue
            table_name = model_obj._meta.db_table
            if table_name in processed_tables:
                continue
            # 调用特定数据库类型的注释添加方法
            add_comment_method(cursor, connection, model_obj)
            processed_tables.add(table_name)
            # 提交事务
            connection.commit()

    def mysql_add_comment(self, cursor, connection, model_obj):
        # 为MySQL数据库添加注释
        table_name = model_obj._meta.db_table
        fields = model_obj._meta.fields
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
                self.stdout.write(f"已为  {table_name}.{db_column} 添加注释: {comment_text}")
            except Exception as e:
                # 记录错误信息
                logger.error(f"未能为 {table_name}.{db_column} 添加注释: {e}")

        # 添加表注释
        table_comment = model_obj._meta.verbose_name
        if table_comment:
            try:
                cursor.execute(f"ALTER TABLE `{table_name}` COMMENT=%s;", (table_comment,))
                self.stdout.write(f"已为表 {table_name} 添加注释: {table_comment}")
            except Exception as e:
                logger.error(f"未能为表 {table_name} 添加注释: {e}")

    def postgresql_add_comment(self, cursor, model_obj):
        # 为PostgreSQL数据库添加注释
        table_name = model_obj._meta.db_table
        fields = model_obj._meta.fields
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
        table_comment = model_obj._meta.verbose_name
        if table_comment:
            try:
                cursor.execute(f"COMMENT ON TABLE {table_name} IS %s;", (table_comment,))
                self.stdout.write(f"已为表{table_name}添加注释: {table_comment}")
            except Exception as e:
                logger.error(f"未能为表{table_name}添加注释: {e}")
