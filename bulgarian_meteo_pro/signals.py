from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import BulgarianMeteoProData
from django.db import transaction

@receiver(pre_save, sender=BulgarianMeteoProData)
def update_station_model(sender, instance, **kwargs):
    with transaction.atomic():
        station = instance.station_id

        update_needed = False
        fields_to_update = []

        # Update api_key if the station becomes inactive
        if instance.station_status == 'inactive' and station.api_key is not None:
            station.api_key = None
            fields_to_update.append('api_key')
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