from weather_master_x.models import WeatherMasterX
from bulgarian_meteo_pro.models import BulgarianMeteoProData
from rest_framework import serializers

class UnifiedWeatherDataSerializer(serializers.Serializer):
    station_id = serializers.CharField()
    city = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    timestamp = serializers.DateTimeField()
    temperature_celsius = serializers.FloatField()
    humidity_percent = serializers.FloatField()
    wind_speed_kph = serializers.FloatField(allow_null=True)
    pressure_hpa = serializers.FloatField(allow_null=True)
    uv_index = serializers.IntegerField(allow_null=True)
    rain_mm = serializers.FloatField(allow_null=True)
    station_status = serializers.CharField()

    def to_representation(self, instance):
        if isinstance(instance, BulgarianMeteoProData):
            return {
                "station_id": instance.station_id.station_id,
                "city": instance.city,
                "latitude": instance.latitude,
                "longitude": instance.longitude,
                "timestamp": instance.timestamp,
                "temperature_celsius": instance.temperature_celsius,
                "humidity_percent": instance.humidity_percent,
                "wind_speed_kph": instance.wind_speed_kph,
                "pressure_hpa": None,
                "uv_index": None,
                "rain_mm": None,
                "station_status": instance.station_status
            }
        elif isinstance(instance, WeatherMasterX):
            return {
                "station_id": instance.station_identifier.station_id,
                "city": instance.location.city_name,
                "latitude": instance.location.coordinates.lat,
                "longitude": instance.location.coordinates.lon,
                "timestamp": instance.recorded_at,
                "temperature_celsius": instance.temperature_celcius,
                "humidity_percent": instance.readings.humidity_percent,
                "wind_speed_kph": None,
                "pressure_hpa": instance.readings.pressure_hpa,
                "uv_index": instance.readings.uv_index,
                "rain_mm": instance.readings.rain_mm,
                "station_status": instance.operational_status
            }
