from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .serializers import UnifiedWeatherDataSerializer
from stations.models import Station
from weather_master_x.models import Coordinates, Location, Readings, WeatherMasterX
from bulgarian_meteo_pro.models import BulgarianMeteoProData, Status
from datetime import datetime

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
        
        self.weather_data_master_x = WeatherMasterX.objects.create(
            station_identifier=self.station,
            recorded_at=datetime.now(),
            readings=readings,
            location=location
        )
        
        self.weather_data_bulgarion_pro = BulgarianMeteoProData.objects.create(
            station_id=self.station,
            city="Test City",
            latitude=42.6977,
            longitude=23.3219,
            timestamp=datetime.now(),
            temperature_celsius=20.5,
            humidity_percent=60.0,
            wind_speed_kph=15.0,
            station_status=Status.ACTIVE
        )

    def test_serializer_data_format_for_weather_master_x(self):
        serializer = UnifiedWeatherDataSerializer(instance=self.weather_data_master_x)
        data = serializer.data
        self.assertEqual(data["station_id"], self.station.station_id)
        self.assertEqual(data["city"], self.station.city)
        self.assertEqual(data["temperature_celsius"], self.weather_data_master_x.temperature_celcius)
        self.assertEqual(data["wind_speed_kph"], None)
        self.assertEqual(data["station_id"], self.station.station_id)
    
    def test_serializer_data_format_for_bulgarian_meteo_pro(self):
        serializer = UnifiedWeatherDataSerializer(instance=self.weather_data_bulgarion_pro)
        data = serializer.data
        self.assertEqual(data["station_id"], self.station.station_id)
        self.assertEqual(data["city"], self.station.city)
        self.assertEqual(data["temperature_celsius"], self.weather_data_bulgarion_pro.temperature_celsius)
        self.assertEqual(data["wind_speed_kph"], self.weather_data_bulgarion_pro.wind_speed_kph)
        self.assertEqual(data["rain_mm"], None)
        self.assertEqual(data["pressure_hpa"], None)
        self.assertEqual(data["uv_index"], None)
        

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
