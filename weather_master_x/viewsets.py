from rest_framework import mixins, viewsets
from weather_master_x.filters import WeatherMasterXFilter
from stations.authorization import StationAPIKeyAuthentication
from .models import WeatherMasterX
from .serializers import WeatherMasterXSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny


class WeatherMasterXViewset(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = WeatherMasterX.objects.all()
    serializer_class = WeatherMasterXSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filter_class = WeatherMasterXFilter
    ordering_fields = ['timestamp', 'temperature_celsius', 'humidity_percent', 'wind_speed_kph']
    permission_classes = [AllowAny]
    
    
    def create(self, request, *args, **kwargs):
        # Manually apply StationAPIKeyAuthentication for create only
        auth = StationAPIKeyAuthentication()
        auth_result = auth.authenticate(request)
        
        if auth_result is None:
            raise AuthenticationFailed('Authentication required to create data.')

        return super().create(request, *args, **kwargs)