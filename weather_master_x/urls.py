from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WeatherMasterXViewset

router = DefaultRouter()
router.register(r'weather-master-data', WeatherMasterXViewset)

urlpatterns = [
    path('', include(router.urls)),
]