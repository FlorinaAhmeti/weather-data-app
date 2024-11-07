from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import BulgarianMeteoProData, Status
from .serializers import BulgarianMeteoProDataSerializer
from stations.models import Station
import datetime

class BulgarianMeteoProDataModelTest(TestCase):
    def setUp(self):
        self.station = Station.objects.create(station_id="BG123", city="Sofia")
        self.weather_data = BulgarianMeteoProData.objects.create(
            station_id=self.station,
            city="Sofia",
            latitude=42.6977,
            longitude=23.3219,
            timestamp=datetime.now(),
            temperature_celsius=20.5,
            humidity_percent=60.0,
            wind_speed_kph=15.0,
            station_status=Status.ACTIVE
        )

    def test_str_method(self):
        self.assertIn("Station BG123 in Sofia", str(self.weather_data))

class BulgarianMeteoProDataSerializerTest(TestCase):
    def setUp(self):
        self.station = Station.objects.create(station_id="BG123", city="Sofia")
        self.weather_data = BulgarianMeteoProData.objects.create(
            station_id=self.station,
            city="Sofia",
            latitude=42.6977,
            longitude=23.3219,
            timestamp=datetime.now(),
            temperature_celsius=20.5,
            humidity_percent=60.0,
            wind_speed_kph=15.0,
            station_status=Status.ACTIVE
        )
        self.serializer = BulgarianMeteoProDataSerializer(instance=self.weather_data)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {"created_at", "updated_at", "id", "station_id", "city", "latitude", "longitude", "timestamp", 
                                            "temperature_celsius", "humidity_percent", "wind_speed_kph", 
                                            "station_status"})

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import BulgarianMeteoProData
from stations.models import Station
from datetime import datetime, timedelta
from .filters import BulgarianMeteoProDataFilter

class BulgarianMeteoProDataViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create a station to associate with BulgarianMeteoProData
        self.station = Station.objects.create(station_id="BG123", city="Sofia")

        # Create sample data entries
        self.weather_data1 = BulgarianMeteoProData.objects.create(
            station_id=self.station,
            city="Sofia",
            latitude=42.6977,
            longitude=23.3219,
            timestamp=datetime.now(),
            temperature_celsius=25.5,
            humidity_percent=65.0,
            wind_speed_kph=10.0,
            station_status="active"
        )
        self.weather_data2 = BulgarianMeteoProData.objects.create(
            station_id=self.station,
            city="Plovdiv",
            latitude=42.1354,
            longitude=24.7453,
            timestamp=datetime.now() - timedelta(days=1),
            temperature_celsius=20.0,
            humidity_percent=70.0,
            wind_speed_kph=12.0,
            station_status="inactive"
        )

    def test_filter_by_city(self):
        url = reverse("bulgarian-metoe-pro-list")
        response = self.client.get(url, {"city": "Sofia"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]["city"], "Sofia")

    def test_filter_by_timestamp_range(self):
        url = reverse("bulgarian-metoe-pro-list")
        from_timestamp = (datetime.now() - timedelta(days=2)).isoformat()
        to_timestamp = datetime.now().isoformat()
        response = self.client.get(url, {"from_timestamp": from_timestamp, "to_timestamp": to_timestamp})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_by_temperature(self):
        url = reverse("bulgarian-metoe-pro-list")
        response = self.client.get(url, {"temperature_celsius": 20.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]["temperature_celsius"], "20.00")

    def test_filter_by_humidity(self):
        url = reverse("bulgarian-metoe-pro-list")
        response = self.client.get(url, {"humidity_percent": 65.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]["humidity_percent"], "65.00")

    def test_filter_by_station_status(self):
        url = reverse("bulgarian-metoe-pro-list")
        response = self.client.get(url, {"station_status": "inactive"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]["station_status"], "inactive")

    def test_ordering_by_timestamp(self):
        url = reverse("bulgarian-metoe-pro-list")
        response = self.client.get(url, {"ordering": "timestamp"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(
            response.data['results'][0]["timestamp"],
            response.data['results'][1]["timestamp"]
        )

    def test_ordering_by_temperature(self):
        
        url = reverse("bulgarian-metoe-pro-list")
        response = self.client.get(url, {"ordering": "temperature_celsius"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(
            response.data['results'][0]["temperature_celsius"],
            response.data['results'][1]["temperature_celsius"]
        )

    def test_authentication_required_for_post_method(self):
        self.client.credentials(HTTP_API_KEY="")
        url = reverse("bulgarian-metoe-pro-list")
        data = {
            "station_id": self.station.station_id,
            "city": "Varna",
            "latitude": 43.2141,
            "longitude": 27.9147,
            "timestamp": datetime.now().isoformat(),
            "temperature_celsius": 15.5,
            "humidity_percent": 55.0,
            "wind_speed_kph": 5.0,
            "station_status": "active"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_create_weather_data(self):
        auth_headers = {'HTTP_AUTHORIZATION': f'Bearer {self.station.api_key}'}
        url = reverse("bulgarian-metoe-pro-list")
        data = {
            "station_id": self.station.station_id,
            "city": "Varna",
            "latitude": 43.2141,
            "longitude": 27.9147,
            "timestamp": datetime.now().isoformat(),
            "temperature_celsius": 15.5,
            "humidity_percent": 55.0,
            "wind_speed_kph": 5.0,
            "station_status": "active"
        }
        response = self.client.post(url, data, format="json", **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["city"], "Varna")
