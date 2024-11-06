from django.db import models
from general.models import AbstractTrackedModel
import uuid

class Station(AbstractTrackedModel):
    station_id = models.CharField(max_length=50, primary_key=True)
    city = models.CharField(max_length=100)
    status = models.BooleanField(default=True) # True for active, False for inactive
    api_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True)
    