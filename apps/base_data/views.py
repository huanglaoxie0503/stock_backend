from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.pagination import CustomPagination
from utils.viewset import CustomModelViewSet
from .models import (
    TradingVolume,
    StockLimitUpDetail,
    StockLimitDownDetail, StockLimitBlast
)
from .serializers import (
    TradingVolumeSerializer,
    StockLimitUpDetailSerializer,
    StockLimitDownDetailSerializer,
    StockLimitBlastSerializer
)
from .filters import (
    TradingVolumeFilter,
    StockLimitBlastFilter,
    StockLimitUpDetailFilter,
    StockLimitDownDetailFilter
)


# Create your views here.


class TradingVolumeViewSet(CustomModelViewSet):
    # 查询
    queryset = TradingVolume.objects.all()
    # 序列化
    serializer_class = TradingVolumeSerializer
    create_serializer_class = TradingVolumeSerializer
    update_serializer_class = TradingVolumeSerializer
    # 过滤
    filterset_class = TradingVolumeFilter
    # 分页功能
    pagination_class = CustomPagination
    # 需要用户认证
    permission_classes = [IsAuthenticated]
    # 使用 JWT 进行认证
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['trade_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-trade_date')


class StockLimitUpDetailViewSet(CustomModelViewSet):
    # 查询
    queryset = StockLimitUpDetail.objects.all()
    #
    serializer_class = StockLimitUpDetailSerializer
    create_serializer_class = StockLimitUpDetailSerializer
    update_serializer_class = StockLimitUpDetailSerializer
    # 过滤
    filterset_class = StockLimitUpDetailFilter
    # 需要用户认证
    permission_classes = [IsAuthenticated]
    # 使用 JWT 进行认证
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['trade_date']


class StockLimitDownDetailViewSet(CustomModelViewSet):
    # 查询
    queryset = StockLimitDownDetail.objects.all()
    #
    serializer_class = StockLimitDownDetailSerializer
    create_serializer_class = StockLimitDownDetailSerializer
    update_serializer_class = StockLimitDownDetailSerializer
    # 过滤
    filterset_class = StockLimitDownDetailFilter
    # 需要用户认证
    permission_classes = [IsAuthenticated]
    # 使用 JWT 进行认证
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]


class StockLimitBlastViewSet(CustomModelViewSet):
    # 查询
    queryset = StockLimitBlast.objects.all()
    # 序列化
    serializer_class = StockLimitBlastSerializer
    create_serializer_class = StockLimitBlastSerializer
    update_serializer_class = StockLimitBlastSerializer
    # 过滤
    filterset_class = StockLimitBlastFilter
    # 需要用户认证
    permission_classes = [IsAuthenticated]
    # 使用 JWT 进行认证
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
