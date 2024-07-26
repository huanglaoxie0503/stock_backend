"""
URL configuration for stock_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
import xadmin
from django.urls import re_path as url
from django.urls import path, include
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from stock_backend.settings import MEDIA_ROOT

# Swagger配置
schema_view = get_schema_view(
    openapi.Info(
        title="涨停宝 API",
        default_version='v1',
        description="描述: API文档",
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    # ********************************** 管理后台系统接口************************************ #
    url(r'^xadmin/', xadmin.site.urls),
    url('^api-auth/', include('rest_framework.urls')),
    url(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),
    # drf自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),
    # jwt的认证接口
    url('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # ********************************** 文档相关路径************************************ #
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # ********************************** 管理后台其他自定义接口************************************ #
    path('v1/api/', include('apps.users.urls'), name='users'),
    path('v1/api/', include('apps.base_data.urls'), name='base_data'),

]
