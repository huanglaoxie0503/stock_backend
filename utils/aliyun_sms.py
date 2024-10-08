#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Date  : 2024-07-12
# @Desc :阿里云短信发送接口
import uuid

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from config import ALI_YUN_SMS_ACCESS_KEY_ID, ALI_YUN_SMS_ACCESS_KEY_SECRET


client = AcsClient(ALI_YUN_SMS_ACCESS_KEY_ID, ALI_YUN_SMS_ACCESS_KEY_SECRET, 'cn-hangzhou')


# 短信发送接口，外部调用即可
def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    # RegionId，默认即可
    request.add_query_param('RegionId', "cn-hangzhou")

    # 发送到的手机号码
    request.add_query_param('PhoneNumbers', phone_numbers)

    # 短信签名
    request.add_query_param('SignName', sign_name)

    # 申请的短信模板编码,必填
    request.add_query_param('TemplateCode', template_code)

    # 短信模板变量参数，及不同的短信区别在哪里，比如验证码短信这里就应传入验证码的json文本
    if template_param is not None:
        request.add_query_param('TemplateParam', template_param)

    # 设置业务请求流水号，用来区分请求，必填。
    request.add_query_param('OutId', business_id)

    # 调用接口发送
    response = client.do_action_with_exception(request)

    return response


# 测试代码
if __name__ == '__main__':
    __business_id = uuid.uuid1()
    # 一个验证码发送的例子
    params = "{\"code\":\"666888\"}"  # 模板参数
    print(str(send_sms(__business_id, "15361276730", "涨停宝", "SMS_302035344", params), encoding='utf-8'))
