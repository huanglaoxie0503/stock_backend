#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-17
# @Desc :
import re
from datetime import datetime, timedelta

from captcha.models import CaptchaStore
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from config import IS_SINGLE_TOKEN, REGEX_MOBILE
from stock_backend import settings
from utils.common import ast_convert
from utils.serializers import CustomModelSerializer
from utils.validator import CustomValidationError, CustomUniqueValidator

Users = get_user_model()


class UserManageSerializer(CustomModelSerializer):
    """
    用户管理-序列化器
    """

    class Meta:
        model = Users
        read_only_fields = ["id", "uuid", "user_id"]
        exclude = ['password', 'user_permissions', 'groups']
        # extra_kwargs = {
        #     'post': {'required': False},
        #     'role': {'required': False},
        # }


class UserManageCreateSerializer(CustomModelSerializer):
    """
    用户管理-序列化器
    """

    # 新增重写
    def create(self, validated_data):
        if "password" in validated_data.keys():
            if validated_data['password']:
                validated_data['password'] = make_password(validated_data['password'])
        validated_data['identity'] = 2
        return super().create(validated_data)

    class Meta:
        model = Users
        fields = '__all__'
        read_only_fields = ["id", "uuid", "user_id"]
        # exclude = ['role', 'post', 'dept']
        extra_kwargs = {
            # 'post': {'required': False},
            # 'role': {'required': False},
            'name': {'required': False},
            'password': {'required': False},
        }


class UserManageUpdateSerializer(CustomModelSerializer):
    """
    用户管理-序列化器
    """

    # 更新重写
    def update(self, instance, validated_data):
        if "password" in validated_data.keys():
            if validated_data['password']:
                validated_data['password'] = make_password(validated_data['password'])
            else:
                validated_data.pop('password', None)
        return super().update(instance, validated_data)

    class Meta:
        model = Users
        read_only_fields = ["id", "uuid", "user_id"]
        exclude = ['identity']
        extra_kwargs = {
            # 'post': {'required': False},
            # 'role': {'required': False},
            'name': {'required': False},
            'password': {'required': False},
        }


# ----------------后端用户Serializer----------------------


class UsersSerializer(CustomModelSerializer):
    """
    后端用户-序列化器
    """

    class Meta:
        model = Users
        read_only_fields = ["id", "uuid", "user_id"]
        exclude = ['password', 'user_permissions', 'groups']
        # extra_kwargs = {
        #     'post': {'required': False},
        # }
        # fields = ("name", "gender", "birthday", "email", "mobile")


class UserCreateSerializer(CustomModelSerializer):
    """
    管理员用户-新增
    """
    username = serializers.CharField(max_length=50, validators=[CustomUniqueValidator(queryset=Users.objects.all(), message='账号必须唯一')])
    password = serializers.CharField(required=False, default=make_password('123456'))
    is_staff = serializers.BooleanField(required=False, default=True)

    def create(self, validated_data):
        if 'password' in validated_data:
            if validated_data['password']:
                validated_data['password'] = make_password(validated_data['password'])
            validated_data['identity'] = 1
        return super().create(validated_data)

    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ["id", "uuid", "user_id"]


class UserUpdateSerializer(CustomModelSerializer):
    username = serializers.CharField(max_length=50, validators=[
        CustomUniqueValidator(queryset=Users.objects.all(), message='账号必须唯一')])
    password = serializers.CharField(required=False, allow_blank=True)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            if validated_data['password']:
                validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

    class Meta:
        # 指定了这个序列化器要序列化的模型是 User，也就是用户模型
        model = Users
        # 表示序列化器要包含模型中的所有字段。这意味着，无论 User 模型中定义了多少字段，都会被包括在这个序列化器的输出中。
        fields = "__all__"
        # 这里使用了 extra_kwargs，它允许你对特定字段进行附加的设置。
        # 在这个例子中，post 字段被设置为不是必需的 (required=False) 并且是只读的 (read_only=True)。这通常用于控制字段在序列化时的行为。
        # extra_kwargs = {'post': {'required': False, 'read_only': True}}
        # read_only_fields 指定了在序列化时应该是只读的字段列表。在这里，uuid 字段被设置为只读，这意味着在创建或更新对象时，客户端提交的值将被忽略。
        read_only_fields = ["id", "uuid", "user_id"]


class LoginSerializer(TokenObtainPairSerializer):
    """
    登录的序列化器:
    重写djangorestframework-simplejwt的序列化器
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_code = None

    captcha = serializers.CharField(max_length=6)
    captcha_key = serializers.CharField(max_length=6)

    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ["id", "uuid", "user_id"]

    default_error_messages = {
        'no_active_account': '该账号已被禁用,请联系管理员'
    }

    # 开启验证码验证
    def validate_captcha(self, captcha):
        initial_data = self.initial_data
        hash_key = initial_data.get('captcha_key')
        self.image_code = CaptchaStore.objects.filter(id=self.initial_data['captcha_key']).first()
        five_minute_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
        if self.image_code and five_minute_ago > self.image_code.expiration:
            self.image_code and self.image_code.delete()
            raise CustomValidationError('图片验证码过期')
        else:
            if self.image_code and (self.image_code.response == captcha or self.image_code.challenge == captcha):
                self.image_code and self.image_code.delete()
            else:
                self.image_code and self.image_code.delete()
                raise CustomValidationError("图片验证码错误")

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        user = Users.objects.filter(username=username).first()

        if not user:
            result = {
                "code": 4000,
                "msg": "账号/密码不正确",
                "data": None
            }
            return result

        if user and not user.is_staff:  # 判断是否允许登录后台
            result = {
                "code": 4000,
                "msg": "您没有权限登录后台",
                "data": None
            }

            return result

        if user and not user.is_active:
            result = {
                "code": 4000,
                "msg": "该账号已被禁用,请联系管理员",
                "data": None
            }
            return result

        if user and user.check_password(password):
            # check_password() 对明文进行加密,并验证
            data = super().validate(attrs)
            refresh = self.get_token(self.user)

            data['id'] = self.user.id
            data['uuid'] = self.user.uuid
            data['user_id'] = self.user.user_id
            data['name'] = self.user.name
            data['mobile'] = self.user.mobile
            data['username'] = self.user.username
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            request = self.context.get('request')
            request.user = self.user
            # 记录登录成功日志
            # save_login_log(request=request)
            # 缓存用户的jwt token
            if IS_SINGLE_TOKEN:
                redis_conn = get_redis_connection("single_token")
                k = "stock-single-token{}".format(user.id)
                TOKEN_EXPIRE_CONFIG = getattr(settings, 'SIMPLE_JWT', None)
                if TOKEN_EXPIRE_CONFIG:
                    TOKEN_EXPIRE = TOKEN_EXPIRE_CONFIG['ACCESS_TOKEN_LIFETIME']
                    redis_conn.set(k, data['access'], TOKEN_EXPIRE)
            result = {
                "code": 2000,
                "msg": "请求成功",
                "data": data
            }
        else:
            result = {
                "code": 4000,
                "msg": "账号/密码不正确",
                "data": None
            }
        return result


# =======================前端用户登录 Serializer========================== #


class SmsSerializer(serializers.Serializer):
    """
    发送短信序列化器
    """
    mobile = serializers.CharField(max_length=11, min_length=11, required=True, help_text="手机号")
    # sms_type = serializers.CharField(max_length=10, required=True, help_text="请求类型：login/register/restpass/rebind")

    def validated_mobile(self, mobile):
        # 手机号验证
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法", 4000)
        if self.context["sms_type"] == "register":
            # 是否已注册
            if Users.objects.filter(mobile=mobile).count():
                raise serializers.ValidationError("该手机号已注册", 4000)
        if self.context['sms_type'] == "restpass" or self.context['sms_type'] == "login":  # 重置密码/用户登录
            # 该手机号是否已注册
            if not Users.objects.filter(username=mobile, identity=2, is_active=True).count():
                raise serializers.ValidationError("没有找到该用户或已禁用", 4000)

        if self.context['sms_type'] == "wxbind":  # 微信绑定
            # 该手机号是否已注册
            if not Users.objects.filter(username=mobile, mobile=mobile, identity=2, is_active=True,
                                        oauthwxuser__isnull=True).count():
                raise serializers.ValidationError("没有找到该用户或该用户已绑定微信", 4000)

        if self.context['sms_type'] == "rebind":  # 换绑手机号，前提用户已经登录
            # 是否跟原来绑定过的号码一致
            queryset = Users.objects.filter(id=self.context['request'].user.id)
            if not queryset:
                raise serializers.ValidationError("该用户不存在", 4000)
            if queryset[0].mobile == mobile:
                raise serializers.ValidationError("请使用新的手机号绑定", 4000)
            if Users.objects.filter(mobile=mobile).count():
                raise serializers.ValidationError("该手机号已被其他用户绑定", 4000)

        return mobile


class MobilePasswordLoginSerializer(TokenObtainPairSerializer):
    """
    手机+密码登录的序列化器
        - 重写djangorestframework-simplejwt的序列化器
    """
    default_error_messages = {
        'no_active_account': _('该账号已被禁用,请联系管理员')
    }

    def validate(self, attrs):
        mobile = attrs['username']
        if not re.match(REGEX_MOBILE, mobile):
            result = {
                "code": 4000,
                "msg": '请输入正确的手机号',
                "data": None
            }
            return result
        password = attrs['password']
        user = Users.objects.filter(username=mobile, identity=2).first()
        if user and not user.is_active:
            result = {
                "code": 4000,
                "msg": "该账号已被禁用,请联系管理员",
                "data": None
            }
            return result
        if user and user.check_password(password):
            data = {}
            refresh = self.get_token(user)
            data['identity'] = ast_convert(user.identity)
            data['userId'] = user.uuid
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            result = {
                "code": 2000,
                "msg": "登录成功",
                "data": {
                    "page": 1,
                    "limit": 1,
                    "total": 1,
                    "data": data
                },
            }
        else:
            result = {
                "code": 4000,
                "msg": "账号/密码不正确",
                "data": None
            }
        return result


class MobileSmsLoginSerializer(TokenObtainPairSerializer):
    """
    手机+短信登录的序列化器:
    重写djangorestframework-simplejwt的序列化器
    """

    @classmethod
    def get_token(cls, user):
        refresh = super(MobileSmsLoginSerializer, cls).get_token(user)
        data = {
            'identity': ast_convert(user.identity),
            'userId': user.uuid,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data
