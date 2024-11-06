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

        if instance.station_status == StatusChoices.MAINTENANCE and station.api_key is not None:
            station.api_key = None
            station.status = False
            fields_to_update.append('api_key', 'status')
            update_needed = True
        
        if station.city != instance.city:
            station.city = instance.city
            fields_to_update.append('city')
            update_needed = True
        if station.latitude != instance.latitude:
            station.latitude = instance.latitude
            fields_to_update.append('latitude')
            update_needed = True
        if station.longitude != instance.longitude:
            station.longitude = instance.longitude
            fields_to_update.append('longitude')
            update_needed = True

        if update_needed:
            station.save(update_fields=fields_to_update)