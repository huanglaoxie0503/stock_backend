from django.db import models
from django.contrib.auth.models import AbstractUser

from config import TABLE_PREFIX
from utils.models import BaseModel, CoreModel


# Create your models here.


class UserProfile(AbstractUser, CoreModel):
    """
    用户管理
    """
    GENDER_CHOICES = (
        (0, "女"),
        (1, "男"),
    )
    IDENTITY_CHOICES = (
        (0, "超级管理员"),
        (1, "系统管理员"),
        (2, "前端用户"),
    )
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名", help_text='姓名')
    mobile = models.CharField(max_length=11, verbose_name="手机号码", help_text='手机号码')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱", help_text='邮箱')
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月", help_text='出生年月')
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True, verbose_name="性别",help_text="性别")
    # 自定义
    identity = models.SmallIntegerField(choices=IDENTITY_CHOICES, verbose_name="身份标识", null=True, blank=True, default=2, help_text="身份标识")
    # permissions = models.JSONField(default=list, verbose_name="权限列表", help_text="权限列表")
    is_delete = models.BooleanField(default=False, verbose_name="是否逻辑删除", help_text="是否逻辑删除")

    class Meta:
        db_table = TABLE_PREFIX + "users"
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

    def __str__(self):
        return self.username


class Counter(models.Model):
    role = models.CharField(max_length=10, unique=True)
    count = models.IntegerField(default=1)  # 初始值从1开始

    @classmethod
    def next_id(cls, role):
        counter, created = cls.objects.get_or_create(role=role)
        next_id = f'{role}-{counter.count:09d}'  # 9位数字，不足的地方补0
        counter.count += 1
        counter.save()
        return next_id
