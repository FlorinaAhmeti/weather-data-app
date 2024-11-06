from django.db import models

from stations.models import Station

class StatusChoices(models.TextChoices):
    OPERATIONAL = 'operational', 'Operational'
    MAINTENANCE = 'maintenance', 'Maintenance'

class Coordinates(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return f"Lat: {self.lat}, Lon: {self.lon}"


class Location(models.Model):
    city_name = models.CharField(max_length=100, help_text="City where the station is located")
    coordinates = models.OneToOneField(Coordinates, on_delete=models.CASCADE, help_text="Coordinates of the location")

    def __str__(self):
        return f"{self.city_name}"


class Readings(models.Model):
    temp_fahrenheit = models.FloatField(help_text="Temperature in Fahrenheit")
    humidity_percent = models.FloatField(help_text="Humidity as a percentage")
    pressure_hpa = models.FloatField(help_text="Atmospheric pressure in hPa")
    uv_index = models.IntegerField(help_text="UV index")
    rain_mm = models.FloatField(help_text="Rainfall in millimeters")

    def __str__(self):
        return f"Temp: {self.temp_fahrenheit}F, Humidity: {self.humidity_percent}%"


class WeatherMasterX(models.Model):
    station_identifier = models.ForeignKey(Station, on_delete=models.CASCADE, to_field="station_id", related_name="weather_master_x")
    location = models.OneToOneField(Location, on_delete=models.CASCADE, help_text="Location of the station")
    recorded_at = models.DateTimeField(help_text="Timestamp of the data in ISO 8601 format")
    readings = models.OneToOneField(Readings, on_delete=models.CASCADE, help_text="Readings of various parameters at the station")
    operational_status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.OPERATIONAL, help_text="Operational status of the station")

    def __str__(self):
        return f"Station ID: {self.station_identifier}, Status: {self.operational_status}"
