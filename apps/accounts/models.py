from datetime import datetime, timedelta

from django.db import models
from utils.models import BaseModel


class User(BaseModel):
    openid = models.CharField(max_length=28, unique=True)
    unionid = models.CharField('unionId', max_length=64, null=False, default='', db_index=True)
    nickname = models.CharField('昵称', max_length=32)

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname
