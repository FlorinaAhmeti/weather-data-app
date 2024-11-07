import random
import uuid
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from stations.models import Station
from bulgarian_meteo_pro.models import BulgarianMeteoProData
from weather_master_x.models import WeatherMasterX, Coordinates, Location, Readings

class Command(BaseCommand):
    help = "Seed initial data for Stations, BulgarianMeteoProData, and WeatherMasterX models"

    def handle(self, *args, **kwargs):
        # Step 1: Define three Bulgarian cities for consistent city names across datasets
        cities = ["Sofia", "Plovdiv", "Varna"]

        # Step 2: Create stations for BulgarianMeteoProData and WeatherMasterX with shared cities
        self.stdout.write("Creating stations...")

        bmp_stations = []
        wmx_stations = []

        # Create 3 stations for BulgarianMeteoProData with defined city names
        for i, city in enumerate(cities):
            bmp_station = Station.objects.create(
                station_id=f"BMP_Station_{i+1}",
                city=city,
                api_key=uuid.uuid4(),
                status=True
            )
            bmp_stations.append(bmp_station)
            self.stdout.write(self.style.SUCCESS(f"Created BMP station for {city}: {bmp_station.station_id}"))

        # Create 3 stations for WeatherMasterX with the same city names
        for i, city in enumerate(cities):
            wmx_station = Station.objects.create(
                station_id=f"WMX_Station_{i+1}",
                city=city,
                api_key=uuid.uuid4(),
                status=True
            )
            wmx_stations.append(wmx_station)
            self.stdout.write(self.style.SUCCESS(f"Created WMX station for {city}: {wmx_station.station_id}"))

        # Step 3: Generate 100 random timestamps over the last month
        self.stdout.write("Generating random timestamps over the last month...")
        timestamps = []
        for _ in range(100):
            random_days_ago = random.randint(0, 30)  # Choose a day within the last month
            random_hour = random.randint(0, 23)
            random_minute = random.randint(0, 59)
            random_timestamp = datetime.now() - timedelta(days=random_days_ago, hours=random_hour, minutes=random_minute)
            timestamps.append(random_timestamp)

        # Step 4: Seed BulgarianMeteoProData with generated timestamps
        self.stdout.write("Seeding BulgarianMeteoProData records...")
        for timestamp in timestamps:
            station = random.choice(bmp_stations)
            BulgarianMeteoProData.objects.create(
                station_id=station,
                city=station.city,
                latitude=round(random.uniform(42.0, 44.0), 4),
                longitude=round(random.uniform(23.0, 27.0), 4),
                timestamp=timestamp,
                temperature_celsius=round(random.uniform(-5, 35), 1),
                humidity_percent=round(random.uniform(30, 90), 1),
                wind_speed_kph=round(random.uniform(0, 50), 1),
                station_status="active"
            )
        self.stdout.write(self.style.SUCCESS("Finished seeding BulgarianMeteoProData records."))

        # Step 5: Seed WeatherMasterX with generated timestamps
        self.stdout.write("Seeding WeatherMasterX records...")
        for timestamp in timestamps:
            station = random.choice(wmx_stations)

            # Create Coordinates
            coordinates = Coordinates.objects.create(
                lat=round(random.uniform(42.0, 44.0), 4),
                lon=round(random.uniform(23.0, 27.0), 4)
            )

            # Create Location
            location = Location.objects.create(
                city_name=station.city,
                coordinates=coordinates
            )

            # Create Readings
            readings = Readings.objects.create(
                temp_fahrenheit=round(random.uniform(30, 100), 1),
                humidity_percent=round(random.uniform(30, 90), 1),
                pressure_hpa=round(random.uniform(900, 1100), 1),
                uv_index=random.randint(0, 11),
                rain_mm=round(random.uniform(0, 10), 1)
            )

            # Create WeatherMasterX entry
            WeatherMasterX.objects.create(
                station_identifier=station,
                location=location,
                recorded_at=timestamp,
                readings=readings,
                operational_status="operational"
            )
        self.stdout.write(self.style.SUCCESS("Finished seeding WeatherMasterX records."))
