from django_filters import FilterSet, AllValuesFilter, DateTimeFilter, NumberFilter
from .models import WeatherMasterX

class WeatherMasterXFilter(FilterSet):
    city = AllValuesFilter(field_name='location__city_name')
    from_recorded_at = DateTimeFilter(field_name='recorded_at', lookup_expr='gte')
    to_recorded_at = DateTimeFilter(field_name='recorded_at', lookup_expr='lte')
    temp_fahrenheit = NumberFilter(field_name='readings__temp_fahrenheit')
    humidity_percent = NumberFilter(field_name='readings__humidity_percent')
    pressure_hpa = NumberFilter(field_name='readings__pressure_hpa')
    uv_index = NumberFilter(field_name='readings__uv_index')
    rain_mm = NumberFilter(field_name='readings__rain_mm')
    operational_status = AllValuesFilter(field_name='operational_status')
    
    class Meta:
        model = WeatherMasterX
        fields = [
            'city',
            'temp_fahrenheit',
            'humidity_percent',
            'pressure_hpa',
            'uv_index',
            'rain_mm',
            'operational_status',
        ]
