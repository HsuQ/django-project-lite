# -*- coding: utf-8 -*-
# @Time    : 2023/10/7 18:00
# @Author  : Hsurich


from django.urls import path, include

from rest_framework.routers import DefaultRouter
from apps.accounts.views import (TokenView)

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenView.as_view()),
]
