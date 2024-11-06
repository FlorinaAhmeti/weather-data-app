from rest_framework import serializers
from .models import Station
import uuid

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['station_id', 'city', 'status', 'api_key']
        read_only_fields = ['api_key'] 

    def update(self, instance, validated_data):
        status = validated_data.get("status", instance.status)
        
        if status:
            instance.api_key = None
        elif status and instance.status == False:
            instance.api_key = uuid.uuid4()

        instance.status = status
        instance.city = validated_data.get("city", instance.city)
        
        instance.save()
        return instance
