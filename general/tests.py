from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .serializers import UnifiedWeatherDataSerializer
from stations.models import Station
from weather_master_x.models import Coordinates, Location, Readings, WeatherMasterX
from bulgarian_meteo_pro.models import BulgarianMeteoProData
import datetime

class UnifiedWeatherDataSerializerTest(TestCase):
    def setUp(self):
        self.station = Station.objects.create(station_id="123", city="Test City")
        coordinates = Coordinates.objects.create(lat=42.6977, lon=23.3219)
        location = Location.objects.create(
            city_name="Test City",
            coordinates=coordinates
        )
        readings = Readings.objects.create(
            temp_fahrenheit=77.9,
            humidity_percent=80.0,
            pressure_hpa=29.92,
            uv_index=5,
            rain_mm=0.5
        )
        
        self.weather_data = WeatherMasterX.objects.create(
            station_identifier=self.station,
            recorded_at=datetime.datetime.now(),
            readings=readings,
            location=location
        )

    def test_serializer_data_format(self):
        serializer = UnifiedWeatherDataSerializer(instance=self.weather_data)
        data = serializer.data
        self.assertIn("station_id", data)
        self.assertIn("city", data)
        self.assertIn("temperature_celsius", data)
        self.assertEqual(data["station_id"], self.station.station_id)

class CityListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Station.objects.create(station_id="123", city="Test City")
        Station.objects.create(station_id="124", city="Another City")

    def test_city_list(self):
        url = reverse("city-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class CityWeatherDataAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.station = Station.objects.create(station_id="123", city="Test City")

    def test_city_weather_data_missing_city_name(self):
        response = self.client.get("/api/city-weather-data/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_city_weather_data_with_city_name(self):
        url = reverse("city-weather-data", args=["Test City"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class DailyAverageWeatherViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_daily_average_weather_invalid_date_range(self):
        url = reverse("daily-average-weather")
        response = self.client.get(url, {"from": "invalid-date", "to": "2023-01-01"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_daily_average_weather_valid_date_range(self):
        url = reverse("daily-average-weather")
        response = self.client.get(url, {"from": "01/01/2023", "to": "31/12/2023"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
