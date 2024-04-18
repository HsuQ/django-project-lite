import time

import jwt
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from weixin import WXAPPAPI

from apps.accounts.models import User

wx_api = WXAPPAPI(appid=settings.APPID, app_secret=settings.APP_SECRET)
tags = ['用户']


class TokenView(APIView):
    """登陆接口"""
    authentication_classes = []

    @swagger_auto_schema(
        operation_description="登录接口",
        # 返回的数据，对应的状态码可以指定一个自定义的序列化器指定返回结果
        tags=tags,
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, required=['code'],
                                    properties={'code': openapi.Schema(type=openapi.TYPE_STRING, title="微信code")}),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'role': openapi.Schema(type=openapi.TYPE_STRING, title="EMPLOYEE:业务管理员，STORE:加盟店，"
                                                                           "SERVICE_PROVIDER:服务商，VISITOR:游客"),
                    'audit_status': openapi.Schema(type=openapi.TYPE_STRING,
                                                   title="审核状态，-1:未申请 0：待审核，1：审核通过 2：审核未通过"),
                    'token': openapi.Schema(type=openapi.TYPE_STRING),
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
        },
        operation_summary='code获取token',
    )
    def post(self, request):
        code = request.data.get('code')
        # 使用 code 获取openid
        session_info = wx_api.exchange_code_for_session_key(code=code)
        openid = session_info.get('openid')
        # 判断是否存在用户
        user = User.objects.filter(openid=openid).first()
        if not user:
            # 不存在则创建用户
            user = User.objects.create(openid=openid, role=UserRoleChoice.VISITOR, audit_status=-1)
            Accounts.objects.create(user=user)
        # 生成 jwt
        payload = {
            "iat": int(time.time()),
            "exp": int(time.time()) + 86400,  # token 有效期1天
            "sub": str(user.id),
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        data = {
            'token': token,
            'role': user.role,
            'user_id': user.id,
            'audit_status': user.audit_status,
        }
        return Response(data, status=status.HTTP_200_OK)