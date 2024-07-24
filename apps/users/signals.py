#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-17
# @Desc :
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(pre_save, sender=UserProfile)
def generate_user_id(sender, instance, **kwargs):
    # 确保不覆盖命令行创建的超级用户
    if instance.is_superuser:
        instance.identity = 0
    else:
        if instance.is_staff:
            instance.identity = 1
        else:
            instance.identity = 2
