from django.test import TestCase
from .models import WeatherMasterX, Coordinates, Location, Readings
from stations.models import Station
from .serializers import WeatherMasterXSerializer
from datetime import datetime, timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class WeatherMasterXModelTest(TestCase):
    def setUp(self):
        # Create related objects for WeatherMasterX
        self.coordinates = Coordinates.objects.create(lat=42.6973, lon=23.3419)
        self.location = Location.objects.create(city_name="Test City", coordinates=self.coordinates)
        self.readings = Readings.objects.create(
            temp_fahrenheit=77.0,
            humidity_percent=65.0,
            pressure_hpa=1015.0,
            uv_index=5,
            rain_mm=1.2
        )
        self.station = Station.objects.create(station_id="WX123", city="Test City")

        # Create WeatherMasterX instance
        self.weather_data = WeatherMasterX.objects.create(
            station_identifier=self.station,
            location=self.location,
            recorded_at=datetime.now(),
            readings=self.readings,
            operational_status="operational"
        )

    def test_string_representation(self):
        self.assertEqual(
            str(self.weather_data),
            f"Station ID: {self.station.station_id}, Status: {self.weather_data.operational_status}"
        )

    def test_temperature_conversion(self):
        # Convert 77°F to Celsius
        expected_celsius = round((77.0 - 32) * 5.0 / 9.0, 2)
        self.assertEqual(self.weather_data.temperature_celcius, expected_celsius)


class WeatherMasterXSerializerTest(TestCase):
    def setUp(self):
        # Create related objects for WeatherMasterX
        self.coordinates = Coordinates.objects.create(lat=42.6937, lon=23.3219)
        self.location = Location.objects.create(city_name="Test City", coordinates=self.coordinates)
        self.readings = Readings.objects.create(
            temp_fahrenheit=77.0,
            humidity_percent=65.0,
            pressure_hpa=1015.0,
            uv_index=5,
            rain_mm=1.2
        )
        self.station = Station.objects.create(station_id="WX123", city="Test City")

        # WeatherMasterX data for serializer
        self.weather_data = WeatherMasterX.objects.create(
            station_identifier=self.station,
            location=self.location,
            recorded_at=datetime.now(),
            readings=self.readings,
            operational_status="operational"
        )
        self.serializer = WeatherMasterXSerializer(instance=self.weather_data)

    def test_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            {"station_identifier", "location", "recorded_at", "readings", "operational_status"}
        )

    def test_serializer_field_values(self):
        data = self.serializer.data
        self.assertEqual(data["station_identifier"], self.station.station_id)
        self.assertEqual(data["location"]["city_name"], "Test City")
        self.assertEqual(data["readings"]["temp_fahrenheit"], 77.0)
        self.assertEqual(data["readings"]["humidity_percent"], 65.0)
        self.assertEqual(data["readings"]["pressure_hpa"], 1015.0)

    def test_serializer_create(self):
        # Sample input data for serializer
        input_data = {
            "station_identifier": self.station.station_id,
            "location": {
                "city_name": "Varna",
                "coordinates": {
                    "lat": 43.2141,
                    "lon": 27.9147
                }
            },
            "recorded_at": datetime.now().isoformat(),
            "readings": {
                "temp_fahrenheit": 60.0,
                "humidity_percent": 55.0,
                "pressure_hpa": 1008.0,
                "uv_index": 3,
                "rain_mm": 0.5
            },
            "operational_status": "operational"
        }

        serializer = WeatherMasterXSerializer(data=input_data)
        self.assertTrue(serializer.is_valid())
        weather_instance = serializer.save()

        # Assert the values were correctly saved
        self.assertEqual(weather_instance.location.city_name, "Varna")
        self.assertEqual(weather_instance.readings.temp_fahrenheit, 60.0)
        self.assertEqual(weather_instance.operational_status, "operational")

    def test_serializer_update(self):
        # New data to update operational status
        update_data = {"operational_status": "maintenance"}
        serializer = WeatherMasterXSerializer(instance=self.weather_data, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_instance = serializer.save()

        self.assertEqual(updated_instance.operational_status, "maintenance")

class WeatherMasterXViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a station to associate with WeatherMasterX
        self.station = Station.objects.create(station_id="WX123", city="Sofia")

        # Create coordinates, location, and readings
        self.coordinates = Coordinates.objects.create(lat=42.6977, lon=23.3319)
        self.location1 = Location.objects.create(city_name="Sofia", coordinates=Coordinates.objects.create(lat=42.6977, lon=23.3319))
        self.location2 = Location.objects.create(city_name="Sofia", coordinates=Coordinates.objects.create(lat=42.6987, lon=23.3329))

        # Create readings for WeatherMasterX instances
        self.readings1 = Readings.objects.create(
            temp_fahrenheit=77.0,
            humidity_percent=65.0,
            pressure_hpa=1015.0,
            uv_index=5,
            rain_mm=1.2
        )
        self.readings2 = Readings.objects.create(
            temp_fahrenheit=68.0,
            humidity_percent=70.0,
            pressure_hpa=1012.0,
            uv_index=4,
            rain_mm=0.8
        )


        # Create sample WeatherMasterX data entries
        self.weather_data1 = WeatherMasterX.objects.create(
            station_identifier=self.station,
            location=self.location1,
            recorded_at=datetime.now(),
            readings=self.readings1,
            operational_status="operational"
        )
        self.weather_data2 = WeatherMasterX.objects.create(
            station_identifier=self.station,
            location=self.location2,
            recorded_at=datetime.now() - timedelta(days=1),
            readings=self.readings2,
            operational_status="maintenance"
        )

    def test_filter_by_city(self):
        url = reverse("weather-master-x-list")
        response = self.client.get(url, {"city": "Sofia"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]["location"]["city_name"], "Sofia")

    def test_filter_by_recorded_at_range(self):
        url = reverse("weather-master-x-list")
        from_recorded_at = (datetime.now() - timedelta(days=2)).isoformat()
        to_recorded_at = datetime.now().isoformat()
        response = self.client.get(url, {"from_recorded_at": from_recorded_at, "to_recorded_at": to_recorded_at})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_by_temperature_fahrenheit(self):
        url = reverse("weather-master-x-list")
        response = self.client.get(url, {"temp_fahrenheit": 68.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['readings']["temp_fahrenheit"], 68.0)

    def test_filter_by_uv_index(self):
        url = reverse("weather-master-x-list")
        response = self.client.get(url, {"uv_index": 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['readings']["uv_index"], 5)

    def test_ordering_by_recorded_at(self):
        url = reverse("weather-master-x-list")
        response = self.client.get(url, {"ordering": "recorded_at"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(
            response.data['results'][1]["recorded_at"],
            response.data['results'][0]["recorded_at"]
        )

    def test_ordering_by_temperature_celsius(self):
        url = reverse("weather-master-x-list")
        response = self.client.get(url, {"ordering": "temp_fahrenheit"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(
            response.data['results'][1]['readings']["temp_fahrenheit"],
            response.data['results'][0]['readings']["temp_fahrenheit"]
        )

    def test_create_weather_master_x(self):
        auth_headers = {'HTTP_AUTHORIZATION': f'Bearer {self.station.api_key}'}
        url = reverse("weather-master-x-list")
        data = {
            "station_identifier": self.station.station_id,
            "location": {
                "city_name": "Plovdiv",
                "coordinates": {
                    "lat": 42.1354,
                    "lon": 24.7453
                    }
            },
            "recorded_at": "2024-09-24T10:20:45Z",
            "readings": {
                "temp_fahrenheit": 73.4,
                "humidity_percent": 58.0,
                "pressure_hpa": 1012.3,
                "uv_index": 5,
                "rain_mm": 0.0
            },
            "operational_status": "operational"
        }
        response = self.client.post(url, data, format="json", **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["location"]["city_name"], "Plovdiv")
        
    def test_authentication_required_for_post_method(self):
        self.client.credentials(HTTP_API_KEY="")
        url = reverse("weather-master-x-list")
        data = {
            "station_identifier": self.station.station_id,
            "location": {
                "city_name": "Varna",
                "coordinates": {
                    "lat": 43.2141,
                    "lon": 27.9147
                }
            },
            "recorded_at": datetime.now().isoformat(),
            "readings": {
                "temp_fahrenheit": 15.5,
                "humidity_percent": 55.0,
                "pressure_hpa": 1015.0,
                "uv_index": 5,
                "rain_mm": 1.2
            },
            "operational_status": "active"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)