from django.db import models
from django.db import models
from general.models import AbstractTrackedModel
from stations.models import Station

class BulgarianMeteoProData(AbstractTrackedModel):
    station_id = models.ForeignKey(Station, on_delete=models.DO_NOTHING)
    city = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()  # ISO 8601 format
    temperature_celsius = models.DecimalField(max_digits=5, decimal_places=2)
    humidity_percent = models.DecimalField(max_digits=5, decimal_places=2)
    wind_speed_kph = models.DecimalField(max_digits=5, decimal_places=2)
    station_status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ])

    class Meta:
        indexes = [
            models.Index(fields=['city', 'timestamp']),
        ]
        ordering = ['timestamp']  # Return data in chronological order

    def __str__(self):
        return f"Station {self.station_id} in {self.city} recorded at {self.timestamp}"
