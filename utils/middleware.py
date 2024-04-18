# -*- coding: utf-8 -*-
# @Time    : 2021/2/25 下午2:02
# @Author  : Hsurich
import json
import logging

from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response

from apps.system.models import LogInfor, SystemLog


class OperationLogMiddleware:
    """
    操作日志Log记录
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.operation_logger = logging.getLogger('operation')  # 记录非GET操作日志
        self.query_logger = logging.getLogger('query')  # 记录GET查询操作日志

    def __call__(self, request):
        try:
            request_body = json.loads(request.body)
        except Exception:
            request_body = dict()
        if request.method == "GET":
            request_body.update(dict(request.GET))
            logger = self.query_logger
        else:
            request_body.update(dict(request.POST))
            logger = self.operation_logger
        # 处理密码, log中密码已******替代真实密码
        for key in request_body:
            if 'password' in key:
                request_body[key] = '******'
        response = self.get_response(request)
        try:
            response_body = response.data
            # 处理token, log中token已******替代真实token值
            if response_body['data'].get('token'):
                response_body['data']['token'] = '******'
        except Exception:
            response_body = dict()
        log_info = f'[{request.user} [Request: {request.method} {request.path} {request_body}] ' \
                   f'[Response: {response.status_code} {response.reason_phrase} {response_body}]]'
        if response.status_code >= 500:
            logger.error(log_info)
            level=3
            operator_content = request_body.get('msg')
        elif response.status_code >= 400:
            logger.warning(log_info)
            level=2
            operator_content = request_body.get('msg')
        else:
            if response_body.get('code')==200:
                logger.info(log_info)
                level=0
                operator_content = response_body.get('data').get("operator_content")
                if not operator_content:
                    operator_content=response_body.get('msg')
            else:
                logger.info(log_info)
                level = 1
                operator_content = response_body.get('errors')
                if not operator_content:
                    operator_content = response_body.get('msg')

        logInfo = LogInfor.objects.filter(method=request.method,deleted=0)
        flag = False

        for m in logInfo:
            if m.route in request.path:
                flag=True
                types = m
        if flag:
            if "item" not in request.path:
                if request.user.id:
                    user_id=request.user.id
                else:
                    user_id=None
                client_ip = request.META.get("REMOTE_ADDR")
                if not operator_content:
                    if response.status_code >= 500:
                        operator_content="服务器错误"
                    else:
                        operator_content=""
                SystemLog.objects.create(
                    operator_id=user_id,
                    type=types,
                    operator_content=operator_content,
                    result=response_body.get("msg"),
                    content=request_body,
                    proxy=request.path,
                    method=request.method,
                    ip=client_ip,
                    level=level
                )
        return response


class ResponseMiddleware(MiddlewareMixin):
    """
    自定义响应数据格式
    """

    def process_request(self, request):
        pass

    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    def process_exception(self, request, exception):
        pass

    def process_response(self, request, response):
        if isinstance(response, Response) and response.get('content-type') == 'application/json':
            if response.status_code >= 400:
                msg = '请求失败'
                detail = response.data.get('detail')
                code = 1
                data = {}
            elif response.status_code == 200 or response.status_code == 201:
                msg = '成功'
                detail = ''
                code = 200
                data = response.data
            else:
                return response
            response.data = {'msg': msg, 'errors': detail, 'code': code, 'data': data}
            response.content = response.rendered_content
        return response


import logging

from django.db import DatabaseError
from django.http.response import JsonResponse
from django.http import HttpResponseServerError
from django.middleware.common import MiddlewareMixin

from .R import R
from .codeEnum import StatusCodeEnum
from .exception import BusinessException

logger = logging.getLogger('error')



class ExceptionMiddleware(MiddlewareMixin):
    """统一异常处理中间件"""

    def process_exception(self, request, exception):
        """
        统一异常处理
        :param request: 请求对象
        :param exception: 异常对象
        :return:
        """
        if isinstance(exception, BusinessException):
            # 业务异常处理
            data = R.set_result(exception.enum_cls).data()
            return JsonResponse(data)

        elif isinstance(exception, DatabaseError):
            # 数据库异常
            r = R.set_result(StatusCodeEnum.DB_ERR)
            logger.error(r.data(), exc_info=True)
            return HttpResponseServerError(StatusCodeEnum.SERVER_ERR.errmsg)

        elif isinstance(exception, Exception):
            # 服务器异常处理
            r = R.server_error()
            logger.error(r.data(), exc_info=True)

            return HttpResponseServerError(r.errmsg)

        return None

    def process_response(self, request, response):
        print("response.status_code", response.status_code)
        if response.status_code == 303:
            response.data={
                "result": True,
                "code": 200,
                "returnCode": "200",
                "message": "成功"
            }
            response.content = response.rendered_content
            response.status_code = 200
            return response

        if isinstance(response, Response) and response.get('content-type') == 'application/json':
            if response.status_code >= 400:
                if response.status_code ==400:

                    # 区分是不是用户未填写信息或者未登录
                    if "用户信息填写不完整或当前暂无该用户" != response.data.get('detail'):
                        response.status_code=200
                        msg = '请求失败'
                        print(response.data.get('detail'))
                        if'non_field_errors' in response.data.get('detail'):
                            detail = response.data.get('detail').get('non_field_errors')[0]

                        elif type(response.data.get('detail'))==str:
                            detail = response.data.get('detail')
                        else:
                            detail = str(response.data.get('detail')).split('string=')[1].split("'")[1]
                        code = 300
                        data = {}
                    else:
                        response.status_code = 200
                        msg = '请求失败'
                        print(response.data.get('detail'))
                        if 'non_field_errors' in response.data.get('detail'):
                            detail = response.data.get('detail').get('non_field_errors')[0]

                        elif type(response.data.get('detail')) == str:
                            detail = response.data.get('detail')
                        else:
                            detail = str(response.data.get('detail')).split('string=')[1].split("'")[1]
                        code = 100
                        data = {}

                elif response.status_code==404:

                    response.status_code = 200
                    msg = response.data.get("detail",'未找到指定接口')
                    detail = response.data.get("detail",'未找到指定接口')
                    code = 404
                    data = {}
                elif response.status_code == 500:
                    response.status_code = 200
                    msg = '请求失败'
                    detail = response.data.get('detail')
                    code = 300
                    data = {}
                elif response.status_code == 401:
                    response.status_code = 200
                    msg = '请求失败'
                    detail = response.data.get('detail')
                    code = 401
                    data = {}
                elif response.status_code == 403:
                    response.status_code = 200
                    msg = '请求失败'
                    detail = response.data.get('detail')
                    code = 403
                    data = {}
                else:
                    response.status_code = 200
                    msg = '登录失效'
                    detail = response.data.get('detail')
                    code = 400
                    data = {}
            elif response.status_code == 200 or response.status_code == 201:
                if 'detail' in response.data:
                    msg = response.data.get('detail',"请求成功")
                else:
                    msg = "请求成功"
                detail = ''
                code = 200
                data = response.data

            else:
                return response
            response.data = {'msg': msg, 'errors': detail, 'code': code, 'data': data}
            response.content = response.rendered_content
        return response
