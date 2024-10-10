from django.db import models

from config import TABLE_PREFIX
from utils.models import BaseModel


# Create your models here.

class ClsNews(BaseModel):
    LABEL_CHOICES = [
        ('bullish', '利好'),
        ('bearish', '利空'),
        ('neutral', '中性'),
    ]
    article_id = models.CharField(max_length=255, verbose_name='ID', help_text='文章ID')
    title = models.CharField(max_length=255, verbose_name='标题', help_text='文章标题')
    content = models.TextField(verbose_name='内容', help_text='内容')
    url = models.URLField(max_length=500, null=True, blank=True, verbose_name='链接', help_text='新闻链接')
    c_time = models.DateTimeField(null=True, blank=True, verbose_name='发布时间', help_text='发布时间')
    stock_code = models.CharField(max_length=50, null=True, blank=True, verbose_name='股票代码', help_text='股票代码')
    stock_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='股票名称', help_text="股票名称")
    label = models.CharField(choices=LABEL_CHOICES, max_length=20, default='neutral', blank=True, verbose_name='标签',
                             help_text='标签')

    def __str__(self):
        return self.title

    class Meta:
        db_table = TABLE_PREFIX + "news"
        verbose_name = '新闻资讯'
        verbose_name_plural = verbose_name
        ordering = ('-c_time',)
        unique_together = ('article_id', )
