from django.db import models

from utils.models import BaseModel
from config import TABLE_PREFIX

# Create your models here.


class TradingVolume(BaseModel):
    trade_date = models.DateField(verbose_name="交易日期")
    sh_market = models.IntegerField(verbose_name="沪市(亿)")
    sz_market = models.IntegerField(verbose_name="深市(亿)")
    total_market = models.IntegerField(verbose_name="两市总额(亿)")

    class Meta:
        db_table = TABLE_PREFIX + "trading_volume"
        verbose_name = "两市成交额"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.trade_date} - 沪市:{self.sh_market}, 深市:{self.sz_market}, 两市总额:{self.total_market}"
