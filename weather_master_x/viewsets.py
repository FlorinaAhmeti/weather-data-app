from rest_framework import mixins, viewsets
from weather_master_x.filters import WeatherMasterXFilter
from stations.authorization import StationAPIKeyAuthentication
from .models import WeatherMasterX
from .serializers import WeatherMasterXSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class WeatherMasterXViewset(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = WeatherMasterX.objects.all()
    serializer_class = WeatherMasterXSerializer
    authentication_classes = [StationAPIKeyAuthentication]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filter_class = WeatherMasterXFilter
    ordering_fields = ['timestamp', 'temperature_celsius', 'humidity_percent', 'wind_speed_kph']
    