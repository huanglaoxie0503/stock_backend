#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-17
# @Desc :
import uuid

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import UserProfile, Counter


@receiver(pre_save, sender=UserProfile)
def generate_user_id(sender, instance, **kwargs):
    # 确保不覆盖命令行创建的超级用户
    if instance.is_superuser:
        if not instance.user_id:
            instance.user_id = Counter.next_id('super')
            instance.identity = 0
        return

    if instance.role == 'emp':
        instance.user_id = Counter.next_id('emp')
        instance.identity = 1
        instance.is_staff = True
    elif instance.role == 'cus':
        instance.user_id = Counter.next_id('cus')
        instance.is_superuser = False
        instance.is_staff = False
        instance.identity = 2
    else:
        instance.user_id = Counter.next_id('vis')
        instance.is_superuser = False
        instance.is_staff = False
        instance.identity = 3
