from django.db import models
from datetime import datetime
# Create your models here.

class AbstractTrackedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
    def on_save(self):
        self.updated_at = datetime.now()
        if not self.created_at:
            self.created_at = datetime.now()
        super().save()