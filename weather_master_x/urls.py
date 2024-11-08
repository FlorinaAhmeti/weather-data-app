from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import WeatherMasterXViewset

router = DefaultRouter()
router.register(r'weather-master-x', WeatherMasterXViewset, basename='weather-master-x')

urlpatterns = [
    path('', include(router.urls)),
]