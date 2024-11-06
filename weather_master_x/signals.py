from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import WeatherMasterX
from django.db import transaction
from .models import StatusChoices

@receiver(pre_save, sender=WeatherMasterX)
def update_station_model(sender, instance, **kwargs):
    with transaction.atomic():
        station = instance.station_identifier

        update_needed = False
        fields_to_update = []

        if instance.operational_status == StatusChoices.MAINTENANCE and station.api_key is not None:
            station.api_key = None
            station.status = False
            fields_to_update.append('api_key', 'status')
            update_needed = True
        
        if station.city != instance.location.city_name:
            station.city = instance.location.city_name
            fields_to_update.append('city')
            update_needed = True
        if station.latitude != instance.location.coordinates.lat:
            station.latitude = instance.location.coordinates.lat
            fields_to_update.append('latitude')
            update_needed = True
        if station.longitude != instance.location.coordinates.lon:
            station.longitude = instance.location.coordinates.lat
            fields_to_update.append('longitude')
            update_needed = True

        if update_needed:
            station.save(update_fields=fields_to_update)