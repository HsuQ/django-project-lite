# -*- coding: utf-8 -*-
# @Time    : 2022/12/2 11:01
# @Author  : Hsurich
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from django.conf import settings


class SMS:
    def __init__(self, sign_name, template_code):
        self.signName = sign_name
        self.templateCode = template_code
        self.client = AcsClient(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET, 'cn-hangzhou')

    def send(self, phone_numbers, template_param):
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('RegionId', "cn-hangzhou")
        request.add_query_param('PhoneNumbers', phone_numbers)
        request.add_query_param('SignName', self.signName)
        request.add_query_param('TemplateCode', self.templateCode)
        request.add_query_param('TemplateParam', template_param)
        response = self.client.do_action_with_exception(request)
        return response


# 发送短信
sms = SMS("XXX", "SMS_XXXX")  # 验证码
# 验证码为：${code}，为避免账号泄露造成损失，请勿泄露验证码。如非本人操作，请忽略此短信。


