from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import TradingVolume
from .serializers import TradingVolumeSerializer, TradingVolumeCreateUpdateSerializer
from.filters import TradingVolumeFilter
from utils.viewset import CustomModelViewSet

# Create your views here.


class TradingVolumeViewSet(CustomModelViewSet):
    queryset = TradingVolume.objects.all()
    serializer_class = TradingVolumeSerializer
    create_serializer_class = TradingVolumeCreateUpdateSerializer
    update_serializer_class = TradingVolumeCreateUpdateSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TradingVolumeFilter
    filterset_fields = ['trade_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-trade_date')
