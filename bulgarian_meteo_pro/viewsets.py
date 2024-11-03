from rest_framework import mixins, viewsets

from bulgarian_meteo_pro.filters import BulgarianMeteoProDataFilter
from .models import BulgarianMeteoProData
from .serializers import BulgarianMeteoProDataSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class BulgarianMeteoProDataViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = BulgarianMeteoProData.objects.all()
    serializer_class = BulgarianMeteoProDataSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filter_class = BulgarianMeteoProDataFilter
    ordering_fields = ['timestamp', 'temperature_celsius', 'humidity_percent', 'wind_speed_kph']
    
