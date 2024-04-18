"""
URL configuration for django-project-lite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from apps.accounts import urls as accounts_urls


# swagger API文档配置 https://github.com/axnsan12/drf-yasg
schema_view = get_schema_view(
    openapi.Info(
        title="DEMO-API",
        default_version='v1.0.0',
        description="API文档",
        terms_of_service="",
        contact=openapi.Contact(email="deemoxuchao@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
    permission_classes=[permissions.AllowAny]
)

base_api = settings.BASE_API

urlpatterns = [
    path(f'{base_api}swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(f'{base_api}swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(f'{base_api}redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path(f'{base_api}accounts/', include(accounts_urls)),
]
