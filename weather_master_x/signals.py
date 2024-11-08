from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import WeatherMasterX
from django.db import transaction
from .models import StatusChoices

@receiver(pre_save, sender=WeatherMasterX)
def update_station_model(sender, instance, **kwargs):
    with transaction.atomic():
        station = instance.station_identifier
        station_status = { True: "operational", False: "maintenance"}

        update_needed = False
        fields_to_update = []

        if instance.operational_status != station_status.get(station.status):
            station.status = not station.status
            fields_to_update.append('status')
            update_needed = True
        
        if station.city != instance.location.city_name:
            station.city = instance.location.city_name
            fields_to_update.append('city')
            update_needed = True
 

        if update_needed:
            station.save(update_fields=fields_to_update)