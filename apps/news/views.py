from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.pagination import CustomPagination
from .models import ClsNews
from .serializers import ClsNewsSerializer
from utils.viewset import CustomModelViewSet


# Create your views here.


class ClsNewsViewSet(CustomModelViewSet):
    # 查询
    queryset = ClsNews.objects.all()
    # 序列化
    serializer_class = ClsNewsSerializer
    create_serializer_class = ClsNewsSerializer
    update_serializer_class = ClsNewsSerializer
    # 过滤
    # filterset_class = TradingVolumeFilter
    # 分页功能
    pagination_class = CustomPagination
    # 需要用户认证
    permission_classes = [IsAuthenticated]
    # 使用 JWT 进行认证
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['c_time']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-c_time')