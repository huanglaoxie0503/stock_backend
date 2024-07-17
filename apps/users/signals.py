#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-17
# @Desc :
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import UserProfile, Counter


@receiver(pre_save, sender=UserProfile)
def generate_user_id(sender, instance, **kwargs):
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
