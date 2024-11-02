from django.db import models
from general.models import AbstractTrackedModel
import uuid
# Create your models here.

class StatusChoices(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'

class Station(AbstractTrackedModel):
    station_id = models.CharField(max_length=50, primary_key=True)
    city = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
    )
    api_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True)
    