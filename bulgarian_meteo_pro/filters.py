from django_filters import FilterSet, AllValuesFilter, DateTimeFilter, NumberFilter
from bulgarian_meteo_pro.models import BulgarianMeteoProData

class BulgarianMeteoProDataFilter(FilterSet):
    city = AllValuesFilter(field_name='city')
    from_timestamp = DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    to_timestamp = DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    temperature_celsius = NumberFilter(field_name='temperature_celsius')
    humidity_percent = NumberFilter(field_name='humidity_percent')
    wind_speed_kph = NumberFilter(field_name='wind_speed_kph')
    station_status = AllValuesFilter(field_name='station_status')
    
    class Meta:
        model = BulgarianMeteoProData
        fields = [
            'city', 
            'temperature_celsius', 
            'humidity_percent', 
            'wind_speed_kph',
            'station_status'
            ]