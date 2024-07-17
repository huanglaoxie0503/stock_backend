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
    ROLE_CHOICES = (
        ('emp', 'employee'),  # 员工
        ('cus', 'customer'),  # 客户
        ('vis', 'visitor'),  # 游客
    )
    IDENTITY_CHOICES = (
        (0, "超级管理员"),
        (1, "系统管理员"),
        (2, "前端用户"),
        (3, "游客用户"),
    )
    user_id = models.CharField(max_length=30, verbose_name="用户ID", help_text='用户ID')
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名", help_text='姓名')
    mobile = models.CharField(max_length=11, verbose_name="手机号码", help_text='手机号码')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱", help_text='邮箱')
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月", help_text='出生年月')
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True, verbose_name="性别",
                                      help_text="性别")
    # 自定义
    identity = models.SmallIntegerField(choices=IDENTITY_CHOICES, verbose_name="身份标识", null=True, blank=True,
                                        default=2, help_text="身份标识")
    role = models.CharField(max_length=3, choices=ROLE_CHOICES, verbose_name='角色', help_text='角色')
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
        next_id = f'{role}-{counter.count:09d}'  # 7位数字，不足的地方补0
        counter.count += 1
        counter.save()
        return next_id
