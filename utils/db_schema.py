#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-27
# @Desc :
from django.db.backends.mysql.schema import DatabaseSchemaEditor as BaseDatabaseSchemaEditor


class CustomDatabaseSchemaEditor(BaseDatabaseSchemaEditor):
    """
    自定义的 DatabaseSchemaEditor 类，用于在 MySQL 字段创建时自动添加注释。

    这个类继承自 Django 的 BaseDatabaseSchemaEditor，并重写了 column_sql 方法，
    以便在生成 SQL 语句时，为每个字段添加一个 COMMENT 子句，其内容为字段的描述信息。
    这样做可以增强数据库的可读性和维护性。
    """

    def create_model(self, model):
        # 添加表注释
        table_comment = getattr(model._meta, 'db_table_comment', None)
        super().create_model(model)
        if table_comment:
            self.execute(f"ALTER TABLE {self.quote_name(model._meta.db_table)} COMMENT = '{table_comment}'")

    def add_field(self, model, field):
        # 添加字段注释
        field_comment = getattr(field, 'db_column_comment', None)
        super().add_field(model, field)
        if field_comment:
            self.execute(
                f"ALTER TABLE {self.quote_name(model._meta.db_table)} CHANGE {self.quote_name(field.column)} {self.quote_name(field.column)} {self.column_sql(model, field)} COMMENT '{field_comment}'")

    # def create_model(self, model):
    #     """
    #     创建数据库表时，除了调用父类方法外，还添加表注释。
    #     """
    #     super().create_model(model)
    #
    #     if self.connection.vendor == 'mysql':
    #         # 获取表的描述信息，这里假设使用模型的 __doc__ 属性作为表注释
    #         table_comment = model.__doc__
    #
    #         # 构建 SQL 语句，为表添加注释
    #         sql = f"ALTER TABLE `{self.quote_name(model._meta.db_table)}` COMMENT = '{table_comment}';"
    #         pprint(sql)
    #
    #         # 执行 SQL 语句
    #         self.execute(sql)
    #
    # def column_sql(self, table, column, include_default=True):
    #     """
    #     重写的 column_sql 方法，用于生成带有注释的 SQL 字段定义。
    #
    #     Args:
    #         table (str): 数据库表的名称。
    #         column (ColumnDescriptor): 描述字段信息的对象，包含字段的名称、类型等属性。
    #         include_default (bool): 是否在 SQL 字段定义中包含默认值。
    #
    #     Returns:
    #         tuple: 包含 SQL 字段定义字符串和参数列表的元组。
    #     """
    #     sql, params = super().column_sql(table, column, include_default=include_default)
    #
    #     if self.connection.vendor == 'mysql':
    #         # 为字段添加注释，注释内容为字段的描述信息
    #         sql += " COMMENT '%s'" % column.description
    #         pprint(sql)
    #
    #     return sql, params
