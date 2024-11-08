from rest_framework import serializers
from .models import WeatherMasterX, Location, Coordinates, Readings

class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = ['lat', 'lon']

class LocationSerializer(serializers.ModelSerializer):
    coordinates = CoordinatesSerializer()

    class Meta:
        model = Location
        fields = ['city_name', 'coordinates']
        
class ReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Readings
        fields = ['temp_fahrenheit', 'humidity_percent', 'pressure_hpa', 'uv_index', 'rain_mm']

class WeatherMasterXSerializer(serializers.ModelSerializer):
    location = LocationSerializer() 
    readings = ReadingsSerializer()

    class Meta:
        model = WeatherMasterX
        fields = [
            'station_identifier', 'location', 'readings', 'recorded_at', 'operational_status'
        ]

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        coordinates_data = location_data.pop('coordinates')
        
        readings_data = validated_data.pop('readings')

        coordinates = Coordinates.objects.create(**coordinates_data)
        location = Location.objects.create(coordinates=coordinates, **location_data)
        readings = Readings.objects.create(**readings_data)
        weather_data = WeatherMasterX.objects.create(location=location, readings=readings, **validated_data)
        return weather_data

    def update(self, instance, validated_data):
        location_data = validated_data.pop('location', None)
        readings_data = validated_data.pop('readings', None)

        if location_data and 'coordinates' in location_data:
            coordinates_data = location_data.pop('coordinates')
            Coordinates.objects.filter(id=instance.location.coordinates.id).update(**coordinates_data)

        if location_data:
            Location.objects.filter(id=instance.location.id).update(**location_data)

        if readings_data:
            Readings.objects.filter(id=instance.readings.id).update(**{k: v for k, v in readings_data.items() if v is not None})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
