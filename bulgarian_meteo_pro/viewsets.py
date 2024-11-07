from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from stations.authorization import StationAPIKeyAuthentication
from .models import BulgarianMeteoProData
from .serializers import BulgarianMeteoProDataSerializer
from bulgarian_meteo_pro.filters import BulgarianMeteoProDataFilter


class BulgarianMeteoProDataViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = BulgarianMeteoProData.objects.all()
    serializer_class = BulgarianMeteoProDataSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filter_class = BulgarianMeteoProDataFilter
    ordering_fields = ['timestamp', 'temperature_celsius', 'humidity_percent', 'wind_speed_kph']
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Manually apply StationAPIKeyAuthentication for create only
        auth = StationAPIKeyAuthentication()
        auth_result = auth.authenticate(request)
        
        if auth_result is None:
            raise AuthenticationFailed('Authentication required to create data.')

        return super().create(request, *args, **kwargs)
