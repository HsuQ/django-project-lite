# -*- coding: utf-8 -*-
# @Time    : 2022/11/22 14:44
# @Author  : Hsurich
import datetime

from django.db.models import Sum, Q
from rest_framework import serializers

from apps.accounts.models import User


class UserTokenSerializers(serializers.ModelSerializer):

    class Meta:
        model = User

