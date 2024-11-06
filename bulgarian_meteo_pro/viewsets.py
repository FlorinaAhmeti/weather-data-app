from rest_framework import mixins, viewsets, status
from bulgarian_meteo_pro.filters import BulgarianMeteoProDataFilter
from stations.authorization import StationAPIKeyAuthentication
from .models import BulgarianMeteoProData
from .serializers import BulgarianMeteoProDataSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

class BulgarianMeteoProDataViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = BulgarianMeteoProData.objects.all()
    serializer_class = BulgarianMeteoProDataSerializer
    authentication_classes = [StationAPIKeyAuthentication]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filter_class = BulgarianMeteoProDataFilter
    ordering_fields = ['timestamp', 'temperature_celsius', 'humidity_percent', 'wind_speed_kph']
    

class BulgarianMeteoProDataViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = BulgarianMeteoProData.objects.all()
    serializer_class = BulgarianMeteoProDataSerializer
    authentication_classes = [StationAPIKeyAuthentication]

    def create(self, request, *args, **kwargs):
        station = request.user

        if request.data.get('station_status') == 'inactive' and station.station_status == 'inactive':
            station.station_status = 'active'
            station.save()

            return Response({
                "message": "Station status updated to active, but no data was recorded."
            }, status=status.HTTP_200_OK)

        return super().create(request, *args, **kwargs)