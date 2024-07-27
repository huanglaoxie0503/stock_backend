from django.db import models

from utils.models import BaseModel, table_prefix

# Create your models here.


class TradingVolume(BaseModel):
    trade_date = models.DateField(verbose_name="交易日期")
    sh_market = models.IntegerField(verbose_name="沪市(亿)")
    sz_market = models.IntegerField(verbose_name="深市(亿)")
    total_market = models.IntegerField(verbose_name="两市总额(亿)")

    class Meta:
        db_table = table_prefix + "trading_volume"
        verbose_name = "两市成交额"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.trade_date} - 沪市:{self.sh_market}, 深市:{self.sz_market}, 两市总额:{self.total_market}"


class StockLimitUpDetail(BaseModel):
    trade_date = models.DateField(verbose_name="交易日期", help_text="交易日期")
    stock_code = models.CharField(max_length=20, verbose_name="股票代码", help_text="股票代码")
    stock_name = models.CharField(max_length=100, verbose_name="股票名称", help_text="股票名称")
    latest_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,  verbose_name="最新价格", help_text="最新价格")
    latest_chg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True,  verbose_name="最新涨跌幅", help_text="最新涨跌幅")
    limit_up_type = models.CharField(max_length=50, null=True, blank=True,  verbose_name="涨停类型", help_text="涨停类型")
    boards = models.CharField(max_length=20, null=True, blank=True,  verbose_name="板数", help_text="板数")
    limit_up_days = models.IntegerField(default=1, verbose_name="涨停天数", help_text="涨停天数")
    first_limit_up_time = models.TimeField(null=True, blank=True,  verbose_name="首次涨停时间", help_text="首次涨停时间")
    last_limit_up_time = models.TimeField(null=True, blank=True,  verbose_name="最后一次涨停时间", help_text="最后一次涨停时间")
    limit_up_opening_nums = models.IntegerField(default=0, verbose_name='涨停开板次数', help_text='涨停开板次数')
    limit_up_volume = models.BigIntegerField(null=True, blank=True,  verbose_name='涨停封单量', help_text='涨停封单量')
    limit_up_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True,  verbose_name='涨停封单金额', help_text='涨停封单金额')
    volume_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True,  verbose_name='涨停封单量占成交量比', help_text='涨停封单量占成交量比')
    cap = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True,  verbose_name='自由流通市值', help_text='自由流通市值')
    volume = models.BigIntegerField(null=True, blank=True,  verbose_name='成交量', help_text='成交量')
    cb = models.CharField(max_length=100, null=True, blank=True, verbose_name='可转债', help_text='可转债')
    limit_up_reasons_hot = models.CharField(max_length=100, verbose_name='热门涨停归因', help_text='热门涨停归因')
    limit_up_reasons = models.CharField(max_length=255, null=True, blank=True, verbose_name="涨停原因", help_text="涨停原因")

    class Meta:
        db_table = table_prefix + "limit_up_detail"
        verbose_name = "涨停股票列表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.trade_date} - 股票名称:{self.stock_name}"

