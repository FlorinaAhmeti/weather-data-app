from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Station
from .serializers import StationSerializer
import uuid

class StationModelTest(TestCase):
    def setUp(self):
        self.station = Station.objects.create(
            station_id="12345",
            city="Test City",
            status=True
        )

    def test_station_creation(self):
        self.assertEqual(self.station.city, "Test City")
        self.assertIsNotNone(self.station.api_key)

    def test_status_toggle(self):
        self.station.status = False
        self.station.save()
        self.assertIsNotNone(self.station.api_key)

        self.station.status = True
        self.station.save()
        self.assertIsNotNone(self.station.api_key)

class StationSerializerTest(TestCase):
    def setUp(self):
        self.station_data = {
            "station_id": "12345",
            "city": "Test City",
            "status": True
        }
        self.station = Station.objects.create(**self.station_data)

    def test_serializer_fields(self):
        serializer = StationSerializer(instance=self.station)
        data = serializer.data
        self.assertEqual(set(data.keys()), {"station_id", "city", "status", "api_key"})

    def test_serializer_update_status(self):
        serializer = StationSerializer(instance=self.station, data={"status": False}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.station.refresh_from_db()
        self.assertIsNotNone(self.station.api_key)

class StationViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.station = Station.objects.create(
            station_id="12345",
            city="Test City",
            status=True
        )
        self.url = reverse("station-detail", args=[self.station.station_id])

    def test_get_station(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["station_id"], str(self.station.station_id))

    def test_update_status_to_inactive(self):
        url = reverse("station-update-status", args=[self.station.station_id])
        response = self.client.patch(url, {"status": False}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.station.refresh_from_db()
        self.assertFalse(self.station.status)
        self.assertIsNotNone(self.station.api_key)

    def test_update_status_to_active(self):
        self.station.status = False
        self.station.api_key = uuid.uuid4()
        self.station.save()

        url = reverse("station-update-status", args=[self.station.station_id])
        response = self.client.patch(url, {"status": True}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.station.refresh_from_db()
        self.assertTrue(self.station.status)
        self.assertIsNotNone(self.station.api_key)
