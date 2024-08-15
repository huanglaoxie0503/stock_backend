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
        verbose_name = "成交额"
        verbose_name_plural = verbose_name
        unique_together = ('trade_date',)

    def __str__(self):
        return f"{self.trade_date} - 沪市:{self.sh_market}, 深市:{self.sz_market}, 两市总额:{self.total_market}"


class StockLimitUpDetail(BaseModel):
    trade_date = models.DateField(verbose_name="交易日期", help_text="交易日期")
    stock_code = models.CharField(max_length=20, verbose_name="股票代码", help_text="股票代码")
    stock_name = models.CharField(max_length=100, verbose_name="股票名称", help_text="股票名称")
    latest_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="价格(元)",
                                       help_text="最新价格")
    latest_chg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="涨跌幅(%)",
                                     help_text="最新涨跌幅")
    limit_up_type = models.CharField(max_length=50, null=True, blank=True, verbose_name="涨停类型",
                                     help_text="涨停类型")
    boards = models.CharField(max_length=20, null=True, blank=True, verbose_name="板数", help_text="板数")
    limit_up_days = models.IntegerField(default=1, verbose_name="涨停天数", help_text="涨停天数")
    first_limit_up_time = models.TimeField(null=True, blank=True, verbose_name="首次涨停时间", help_text="首次涨停时间")
    last_limit_up_time = models.TimeField(null=True, blank=True, verbose_name="最后一次涨停时间",
                                          help_text="最后一次涨停时间")
    limit_up_opening_nums = models.IntegerField(default=0, verbose_name='开板次数', help_text='涨停开板次数')
    limit_up_volume = models.BigIntegerField(null=True, blank=True, verbose_name='封单量(手)', help_text='涨停封单量')
    limit_up_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True,
                                          verbose_name='封单金额(亿)', help_text='涨停封单金额')
    volume_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True,
                                      verbose_name='涨停封单量占成交量比', help_text='涨停封单量占成交量比')
    cap = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name='市值(亿)',
                              help_text='自由流通市值')
    volume = models.BigIntegerField(null=True, blank=True, verbose_name='成交量', help_text='成交量')
    cb = models.CharField(max_length=100, null=True, blank=True, verbose_name='可转债', help_text='可转债')
    limit_up_reasons_hot = models.CharField(max_length=100, null=True, blank=True, verbose_name='涨停归因', help_text='热门涨停归因')
    limit_up_reasons = models.CharField(max_length=255, null=True, blank=True, verbose_name="题材", help_text="涨停原因")

    class Meta:
        db_table = table_prefix + "limit_up_detail"
        verbose_name = "涨停"
        verbose_name_plural = verbose_name
        # (`trade_date`,`stock_code`)
        unique_together = ('trade_date', 'stock_code')

    def __str__(self):
        return f"{self.trade_date} - 股票名称:{self.stock_name}"


class StockLimitDownDetail(BaseModel):
    trade_date = models.DateField(verbose_name="交易日期", help_text="交易日期")
    stock_code = models.CharField(max_length=20, verbose_name="股票代码", help_text="股票代码")
    stock_name = models.CharField(max_length=100, verbose_name="股票名称", help_text="股票名称")
    latest_chg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="涨跌幅(%)",
                                     help_text="最新涨跌幅(%)")
    limit_down_days = models.IntegerField(default=1, verbose_name="跌停天数", help_text="跌停天数")
    limit_down_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True,
                                            verbose_name='跌停封单额(亿)', help_text='跌停封单金额(亿)')
    limit_down_volume = models.BigIntegerField(null=True, blank=True, verbose_name='跌停封单量(手)', help_text='跌停封单量(手)')
    volume = models.BigIntegerField(null=True, blank=True, verbose_name='成交量', help_text='成交量')
    cap = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name='自由流通市值',
                              help_text='自由流通市值')
    limit_down_type = models.CharField(max_length=50, null=True, blank=True, verbose_name="跌停类型",
                                       help_text="跌停类型")
    limit_down_reason = models.CharField(max_length=200, null=True, blank=True, verbose_name="跌停原因",
                                         help_text="跌停原因")
    limit_down_time = models.TimeField(null=True, blank=True, verbose_name="跌停时间", help_text="跌停时间")
    concept = models.TextField(null=True, blank=True, verbose_name="所属概念", help_text="所属概念")

    class Meta:
        db_table = table_prefix + "limit_down_detail"
        verbose_name = "跌停"
        verbose_name_plural = verbose_name
        unique_together = ('trade_date', 'stock_code')

    def __str__(self):
        return f"{self.trade_date} - 股票名称:{self.stock_name}"


class StockLimitBlast(BaseModel):
    trade_date = models.DateField(verbose_name="交易日期", help_text="交易日期")
    stock_code = models.CharField(max_length=20, verbose_name="股票代码", help_text="股票代码")
    stock_name = models.CharField(max_length=100, verbose_name="股票名称", help_text="股票名称")
    has_limit_up = models.CharField(max_length=20, null=True, blank=True, verbose_name="曾涨停", help_text="曾涨停")
    limit_up_opened_cnt = models.IntegerField(default=1, verbose_name='开板次数', help_text='涨停开板次数')
    limit_up_duration = models.CharField(max_length=20, null=True, blank=True, verbose_name="封板时长", help_text="涨停封板时长")
    first_limit_up_time = models.TimeField(null=True, blank=True, verbose_name="涨停时间", help_text="首次涨停时间")
    pre_close = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name='收盘价', help_text='收盘价')
    latest_chg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="涨跌幅", help_text="最新涨跌幅")
    limit_up_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name='涨停价', help_text='涨停价')
    volume = models.BigIntegerField(null=True, blank=True, verbose_name='成交量', help_text='成交量')
    cap = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name='市值(亿)', help_text='自由流通市值(亿)')
    concept = models.TextField(null=True, blank=True, verbose_name="所属概念", help_text="所属概念")

    class Meta:
        db_table = table_prefix + "limit_blast"
        verbose_name = "炸板"
        verbose_name_plural = verbose_name
        unique_together = ('trade_date', 'stock_code')

    def __str__(self):
        return f"{self.trade_date} - 股票名称:{self.stock_name}"


class StockDailyData(BaseModel):
    trade_date = models.DateField(verbose_name="交易日期", help_text="交易日期")
    ts_code = models.CharField(max_length=20, verbose_name="股票代码", help_text="股票代码")
    open = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='开盘价', help_text='开盘价')
    high = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='最高价', help_text='最高价')
    low = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='最低价', help_text='最低价')
    close = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='收盘价', help_text='收盘价')
    pre_close = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='昨收价', help_text='昨收价')
    change = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='涨跌额', help_text='涨跌额')
    pct_chg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='涨跌幅', help_text='涨跌幅')
    vol = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='成交量（手）', help_text='成交量（手）')
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='成交金额（万元）', help_text='成交金额（万元）')
    turnover_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='换手率（%）', help_text='换手率（%)')

    class Meta:
        db_table = table_prefix + "daily_data"
        verbose_name = "日线"
        verbose_name_plural = verbose_name
        unique_together = ('trade_date', 'ts_code')

    def __str__(self):
        return f"{self.trade_date} - 股票名称:{self.ts_code}"


class StockTickTimeDataDays(BaseModel):
    trade_date = models.DateField(verbose_name="交易日期", help_text="交易日期")
    stock_code = models.CharField(max_length=20, verbose_name="股票代码", help_text="股票代码")
    stock_name = models.CharField(max_length=100, verbose_name="股票名称", help_text="股票名称")
    volume = models.IntegerField(null=True, blank=True, verbose_name='成交量', help_text='成交量')
    tick_time = models.TimeField(null=True, blank=True, verbose_name="分时", help_text="分时")

    class Meta:
        db_table = table_prefix + "tick_time_data_days"
        verbose_name = "分时"
        verbose_name_plural = verbose_name
        # 设置联合唯一索引 (`trade_date`,`tick_time`,`stock_code`)
        unique_together = (('trade_date', 'stock_code', 'tick_time'),)

    def __str__(self):
        return f"{self.trade_date} - 股票名称:{self.stock_name}"


class StockTradeCalendar(BaseModel):
    trade_date = models.DateField(verbose_name="交易日期", help_text="交易日期")
    market_open = models.SmallIntegerField(null=True, blank=True, verbose_name="是否开市", help_text="是否开市")
    trade_month = models.CharField(max_length=50, null=True, blank=True, verbose_name="年月", help_text="年月")

    class Meta:
        db_table = table_prefix + "trade_calendar"
        verbose_name = "交易日历"
        verbose_name_plural = verbose_name
        # 设置联合唯一索引
        unique_together = (('trade_date',),)

    def __str__(self):
        return f"{self.trade_date} - 是否开市:{self.market_open}"


class StockConditionalPicker(BaseModel):
    trade_date = models.DateField(verbose_name="交易日期", help_text="交易日期")
    stock_code = models.CharField(max_length=20, verbose_name="股票代码", help_text="股票代码")
    stock_name = models.CharField(max_length=100, verbose_name="股票名称", help_text="股票名称")
    cond_name = models.CharField(max_length=50, verbose_name="选股条件", help_text="选股条件")
    pre_close = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='收盘价', help_text='收盘价')
    high_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='最高价', help_text='最高价')
    chg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='涨跌幅', help_text='涨跌幅')
    cap = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='市值(亿)', help_text='自由流通市值')
    volume = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='成交量(手)', help_text='成交量')
    concept = models.TextField(null=True, blank=True, verbose_name="所属概念", help_text="所属概念")

    class Meta:
        db_table = table_prefix + "conditional_picker"
        verbose_name = "选股"
        verbose_name_plural = verbose_name
        # 设置联合唯一索引
        unique_together = (('trade_date', 'stock_code', 'cond_name'),)

    def __str__(self):
        return f"{self.trade_date} - 股票名称:{self.stock_name}"


