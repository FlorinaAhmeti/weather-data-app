from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import BulgarianMeteoProData
from django.db import transaction

@receiver(pre_save, sender=BulgarianMeteoProData)
def update_station_model(sender, instance, **kwargs):
    with transaction.atomic():
        station = instance.station_id
        station_status = { True: "inactive", False: "inactive"}
        update_needed = False
        fields_to_update = []
        if instance.station_status != station_status.get(station.status):
            station.status = not station.status
            fields_to_update.append('status')
            update_needed = True

        if station.city != instance.city:
            station.city = instance.city
            fields_to_update.append('city')
            update_needed = True

        if update_needed:
            station.save(update_fields=fields_to_update)