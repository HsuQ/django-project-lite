# -*- coding: utf-8 -*-
# @Time    : 2021/1/12 10:44
# @Author  : Hsurich
# @Email   : hsurich78@163.com
# @File    : auth.py
# @Software: PyCharm

import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', '').split()

        if not auth or auth[0].lower() != self.keyword.lower():
            raise exceptions.AuthenticationFailed('未填写token！')
            # return None

        if len(auth) == 1:
            msg = 'Token 头无效，没有提供 Token'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Token 头无效，Token 字符串中不应包含空格'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['sub'])
            if user.available == 0:
                raise exceptions.PermissionDenied('您的账号已被禁用')
            user.is_authenticated = True  # 为配合 django 的权限检查
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token 已过期')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('用户不存在或已删除')
        except jwt.InvalidSignatureError:
            raise exceptions.AuthenticationFailed('认证失败')

        return user, token

    def authenticate_header(self, request):
        return self.keyword
