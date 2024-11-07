from django.urls import path
from .views import CityWeatherDataAPIView, DailyAverageWeatherView, CityListView

urlpatterns = [
    path('city-weather-data/<str:city_name>/', CityWeatherDataAPIView.as_view(), name='city-weather-data'),
    path('daily-average-weather/', DailyAverageWeatherView.as_view(), name='daily-average-weather'),
    path('cities/', CityListView.as_view(), name='city-list'),
]

