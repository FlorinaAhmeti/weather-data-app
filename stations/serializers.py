from rest_framework import serializers
from .models import Station
import uuid

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['station_id', 'city', 'status', 'api_key']
        read_only_fields = ['api_key', 'station_id'] 
