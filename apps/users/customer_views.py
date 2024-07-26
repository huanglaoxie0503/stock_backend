#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-24
# @Desc : 前端用户登录、注册、修改密码
import json
import re
import uuid
from random import choice

from django_redis import get_redis_connection
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from config import REGEX_MOBILE, ALI_YUN_SMS_SIGN, ALI_YUM_SMS_TEMPLATE
from utils.aliyun_sms import send_sms
from utils.common import get_parameter_dic
from .serializers import MobilePasswordLoginSerializer, MobileSmsLoginSerializer, SmsSerializer
from utils.jsonResponse import SuccessResponse, ErrorResponse, DetailResponse

# Create your views here.
Users = get_user_model()


# Create your views here.
# ********************************** 前端客户微服务API用户接口************************************ #


class SendSmsCodeView(APIView):
    """
    post:
    【功能描述】发送手机验证码</br>
    【参数说明】使用"application/json"编码传输，参数如下：mobile 为手机号</br>
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = SmsSerializer

    @staticmethod
    def generate_code():
        """
        生成6位数字的验证码
        :return: 验证码字符串
        """
        seeds = "1234567890"
        random_str = []
        for i in range(6):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']
            if not re.match(REGEX_MOBILE, mobile):
                return ErrorResponse(error_message="请输入正确手机号")

            # 判断该手机号60s内是否已经发送过短信
            redis_conn = get_redis_connection('verify_codes')
            send_flag = redis_conn.get(f'send_flag_{mobile}')
            if send_flag:  # 如果取到了标记，说明该手机号60s内发送过短信验证码
                return ErrorResponse(error_message="请一分钟后再获取验证码")

            # 验证码过期时间
            code_expire = 120  # 120秒，默认2分钟
            # 生成验证码
            code = self.generate_code()

            __business_id = uuid.uuid1()
            params = f'{{"code":"{code}"}}'  # 模板参数
            sms_status = send_sms(__business_id, mobile, ALI_YUN_SMS_SIGN, ALI_YUM_SMS_TEMPLATE, params)
            sms_status_str = sms_status.decode()
            sms_status_json = json.loads(sms_status)
            if 'Code' in sms_status_str:  # 判断返回内容是否存在code的key，错误时不返回code
                if sms_status_json["Code"] == 'OK':
                    # 存储短信验证码到redis
                    redis_conn.setex(f'sms_{mobile}', code_expire, code)  # 默认300秒5分钟过期时间
                    # 存储一个标记，表示此手机号已发送过短信，标记有效期为60s
                    redis_conn.setex(f'send_flag_{mobile}', 60, 1)
                    mydata = {"mobile": mobile}
                    return DetailResponse(data=mydata, msg="发送成功")
                else:
                    return ErrorResponse(data=sms_status_json, error_message='发送失败')
            else:
                return ErrorResponse(data=sms_status_json, error_message='发送失败')
        return ErrorResponse(data=serializer.errors, error_message="参数验证失败")


class MobilePasswordLoginView(TokenObtainPairView):
    """
    post:
    【功能描述】前端-手机号码+密码登录</br>
    【参数说明】mobile为手机号</br>
    【参数说明】password为密码</br>
    """
    serializer_class = MobilePasswordLoginSerializer
    permission_classes = []


class UsernamePasswordLoginView(APIView):
    """
    post:
    【功能描述】前端-账号+密码登录</br>
    【参数说明】username为账号</br>
    【参数说明】password为密码</br>
    """

    @staticmethod
    def post(request):
        username = get_parameter_dic(request)['username']
        password = get_parameter_dic(request)['password']
        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, username):
            return ErrorResponse(error_message="请输入正确的手机号")
        user = Users.objects.filter(username=username).first()
        if user and not user.is_active:
            return ErrorResponse(error_message="该账号已被禁用,请联系管理员")
        if user and user.check_password(password):
            re_data = MobileSmsLoginSerializer.get_token(user)
            return DetailResponse(data=re_data, msg="登录成功")
        return ErrorResponse(error_message="账号/密码错误")


class MobileSmsLoginView(APIView):
    """
    post:
    【功能描述】前端-用户手机号+短信验证码登录</br>
    【参数说明】mobile为手机号</br>
    【参数说明】code为短信验证码</br>
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        mobile = get_parameter_dic(request)['mobile']
        code = get_parameter_dic(request)['code']
        # 验证手机号是否合法
        if not re.match(REGEX_MOBILE, mobile):
            return ErrorResponse(error_message="请输入正确手机号")
        # 判断短信验证码是否正确
        redis_conn = get_redis_connection('verify_codes')
        send_flag = redis_conn.get('sms_%s' % mobile)  # send_flag的值为bytes，需要转换成str ,send_flag.decode()
        if not send_flag:  # 如果取不到标记，则说明验证码过期
            return ErrorResponse(error_message="短信验证码已过期")
        else:
            if str(send_flag.decode()) != str(code):
                return ErrorResponse(error_message="验证码错误")
            # 开始登录
            user = Users.objects.filter(username=mobile).first()
            if not user:
                return ErrorResponse(error_message="用户不存在")
            if not user.is_active:
                return ErrorResponse(error_message="该账号已被禁用，请联系管理员")
            res_data = MobileSmsLoginSerializer.get_token(user)
            redis_conn.delete('sms_%s' % mobile)
            return SuccessResponse(data=res_data, message="登录成功")


class ForgetPasswdResetView(APIView):
    """
    post:
    【功能描述】前端-重置用户密码</br>
    【参数说明】mobile为手机号</br>
    【参数说明】code为短信验证码</br>
    【参数说明】password为密码</br>
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):

        mobile = get_parameter_dic(request)['mobile']
        code = get_parameter_dic(request)['code']
        password = get_parameter_dic(request)['password']
        if len(password) < 6:
            return ErrorResponse(error_message="密码长度至少6位")

        # 验证手机号是否合法
        if not re.match(REGEX_MOBILE, mobile):
            return ErrorResponse(error_message="请输入正确手机号")
        # 判断短信验证码是否正确
        redis_conn = get_redis_connection('verify_codes')
        send_flag = redis_conn.get('sms_%s' % mobile)  # send_flag的值为bytes，需要转换成str ,,send_flag.decode()
        if not send_flag:  # 如果取不到标记，则说明验证码过期
            return ErrorResponse(error_message="短信验证码已过期")
        else:
            if str(send_flag.decode()) != str(code):
                return ErrorResponse(error_message="验证码错误")
            # 开始更换密码
            user = Users.objects.filter(username=mobile, identity=2).first()
            if not user:
                return ErrorResponse(error_message="用户不存在")
            if not user.is_active:
                return ErrorResponse(error_message="该账号已被禁用，请联系管理员")
            # 重置密码
            user.password = make_password(password)
            user.save()
            redis_conn.delete('sms_%s' % mobile)
            return SuccessResponse(message="success")


class MobileRegisterView(APIView):
    """
    post:
    【功能描述】前端-用户注册</br>
    【参数说明】mobile为手机号</br>
    【参数说明】code为短信验证码</br>
    【参数说明】password为密码</br>
    【参数说明】password2为确认输入的密码</br>
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        mobile = get_parameter_dic(request)['mobile']
        code = get_parameter_dic(request)['code']
        password = get_parameter_dic(request)['password']
        password2 = get_parameter_dic(request)['password2']
        if mobile is None or code is None or password is None or password2 is None:
            return ErrorResponse(error_message="提交的参数不能为空")

        # 判断密码是否合法
        if len(password) < 6:
            return ErrorResponse(error_message="密码长度至少6位")

        if not re.match(r'^[a-zA_Z0-9]{6,20}$', password):
            return ErrorResponse(error_message="密码格式不正确(大小写字母、数字组合)")

        if password != password2:
            return ErrorResponse(error_message="两次密码输入不一致")

        # 验证手机号是否合法
        if not re.match(REGEX_MOBILE, mobile):
            return ErrorResponse(error_message="请输入正确手机号")

        # 判断短信验证码是否正确
        if not re.match(r'^\d{6}$', code):
            return ErrorResponse(error_message="验证码格式错误")
        redis_conn = get_redis_connection('verify_codes')
        send_flag = redis_conn.get('sms_%s' % mobile)  # send_flag的值为bytes，需要转换成str ,,send_flag.decode()
        if not send_flag:  # 如果取不到标记，则说明验证码过期
            return ErrorResponse(error_message="短信验证码已过期")
        else:
            if str(send_flag.decode()) != str(code):
                return ErrorResponse(error_message="验证码错误")
            # 开始注册
            Users.objects.create(username=mobile, password=make_password(password), mobile=mobile, is_staff=False, identity=2)
            redis_conn.delete('sms_%s' % mobile)
            return DetailResponse(data=mobile, msg="注册成功")
