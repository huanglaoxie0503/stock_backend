from django.db import models

from utils.models import BaseModel, table_prefix


# Create your models here.
class BaseStockModel(BaseModel):
    trade_date = models.DateField(verbose_name="交易日期", help_text="交易日期")
    stock_code = models.CharField(max_length=20, verbose_name="股票代码", help_text="股票代码")
    stock_name = models.CharField(max_length=100, verbose_name="股票名称", help_text="股票名称")
    open_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='开盘价', help_text='开盘价')
    pre_close = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='昨收价', help_text='昨收价')
    pre_open_vol_ratio = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name='天量比', help_text='集合竞价成交量/昨日成交量（比率）')
    pre_open_max_vol_ratio = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name='分量比', help_text='集合竞价成交量/昨日分时最大成交量（比率）')
    auction_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='竞价金额', help_text='集合竞价成交金额')
    auction_volume = models.BigIntegerField(null=True, blank=True, verbose_name='竞价量',  help_text='集合竞价成交量')
    pre_max_volume = models.BigIntegerField(null=True, blank=True, verbose_name='成交量(Max)', help_text='昨日(分时)最大成交量')
    pre_volume = models.BigIntegerField(null=True, blank=True, verbose_name='成交量', help_text='昨日成交量')
    cap = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='市值(亿)', help_text='自由流通市值')
    is_ops = models.BooleanField(default=False, verbose_name="是否操作", help_text="是否操作")
    profit_chg = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name='竞价涨幅', help_text='竞价盈亏')
    profit_chg_close = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name='收盘盈亏', help_text='收盘时的盈亏')

    class Meta:
        abstract = True


class StockAuction(BaseModel):
    trade_date = models.DateField(verbose_name="交易日期", help_text="交易日期")
    stock_code = models.CharField(max_length=20, verbose_name="股票代码", help_text="股票代码")
    stock_name = models.CharField(max_length=100, verbose_name="股票名称", help_text="股票名称")
    latest_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='价格', help_text='最新价格')
    limit_up_order_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='竞价封单(亿)', help_text='涨停封单金额')
    cap = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='市值(亿)', help_text='自由流通市值')
    limit_up_reason = models.CharField(max_length=255, null=True, blank=True, verbose_name="涨停归因", help_text="涨停原因")

    class Meta:
        db_table = table_prefix + "auction_limit_up"
        verbose_name = "竞价涨停"
        verbose_name_plural = verbose_name
        # 设置联合唯一索引
        constraints = [
            models.UniqueConstraint(fields=['trade_date', 'stock_code'], name='unique_trade_date_stock_code')]

    def __str__(self):
        return f"{self.trade_date} - 股票名称:{self.stock_name}"


class StockLimitUpAuction(BaseStockModel):
    limit_up_opening_nums = models.IntegerField(default=0, blank=True, verbose_name='开板次数', help_text='涨停开板次数')
    last_limit_up_time = models.TimeField(null=True, blank=True, verbose_name='涨停时间', help_text='最后涨停时间')
    limit_up_days = models.IntegerField(default=1, blank=True, verbose_name='连板数', help_text='连板天数')
    limit_up_reasons = models.CharField(max_length=225, null=True, blank=True, verbose_name="涨停归因", help_text="涨停原因")
    model_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="模型名称", help_text="模型名称")
    cb = models.CharField(max_length=50, null=True, blank=True, verbose_name="可转债", help_text="可转债")

    class Meta:
        db_table = 'stock_limit_up_series'
        verbose_name = "雏龙选股(全)"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['trade_date', 'stock_code'], name='unique_trade_date_stock_code_limit_up_auction')]

    def __str__(self):
        return f"{self.trade_date} - 股票名称:{self.stock_name}"


class StockLimitUpAuctionReal(BaseStockModel):
    limit_up_opening_nums = models.IntegerField(default=0, blank=True, verbose_name='开板次数', help_text='涨停开板次数')
    last_limit_up_time = models.TimeField(null=True, blank=True, verbose_name='涨停时间', help_text='最后涨停时间')
    limit_up_days = models.IntegerField(default=1, blank=True, verbose_name='连板数', help_text='连板天数')
    limit_up_reasons = models.CharField(max_length=225, null=True, blank=True, verbose_name="涨停归因", help_text="涨停原因")
    model_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="模型名称", help_text="模型名称")
    cb = models.CharField(max_length=50, null=True, blank=True, verbose_name="可转债", help_text="可转债")

    class Meta:
        db_table = 'stock_limit_up_series_real'
        verbose_name = "雏龙选股(real)"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['trade_date', 'stock_code'], name='unique_trade_date_stock_limit_up_series_real')]

    def __str__(self):
        return f"{self.trade_date} - 股票名称:{self.stock_name}"


class StockAuctionConditions(BaseStockModel):
    high_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='最高价', help_text='最高价')
    gap_type = models.CharField(max_length=20, null=True, blank=True, verbose_name="高开类型", help_text="高开类型")
    cond_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="选股条件", help_text="选股条件名称")
    concept = models.TextField(null=True, blank=True, verbose_name="行业", help_text="所属行业")

    class Meta:
        db_table = 'stock_auction_conditions'
        verbose_name = "条件选股"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['trade_date', 'stock_code', 'cond_name'],
                                    name='unique_trade_date_stock_code_cond_name')]

    def __str__(self):
        return f"{self.trade_date} - 股票名称:{self.stock_name}"
