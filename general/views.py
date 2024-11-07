from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from general.utils import combine_weather_data, validate_date_range
from weather_master_x.models import WeatherMasterX
from bulgarian_meteo_pro.models import BulgarianMeteoProData
from .serializers import UnifiedWeatherDataSerializer
from stations.models import Station
from django.db.models import Avg, F, ExpressionWrapper, FloatField
from django.db.models.functions import TruncDate
from django.core.cache import cache

class CityListView(APIView):
    def get(self, request):
        cities = Station.objects.values_list('city', flat=True).distinct()
        return Response([{"name": city} for city in cities])

class CityWeatherDataAPIView(APIView):

    def get(self, request, city_name=None):
        if not city_name:
            return Response({"error": "city_name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Define a unique cache key for each city
        cache_key = f"city_weather_data_{city_name}"
        
        # Check if the data is already cached
        cached_data = cache.get(cache_key)
        breakpoint()
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        # Fetch stations by city and prefetch related data
        stations = Station.objects.filter(city=city_name).prefetch_related(
            'bulgarian_meteo_pro_data', 'weather_master_x'
        )
    
        # Collect data from related models
        combined_data = []
        for station in stations:
            # Serialize BulgarianMeteoProData records
            meteo_data = station.bulgarian_meteo_pro_data.all()
            meteo_serializer = UnifiedWeatherDataSerializer(meteo_data, many=True)
            combined_data.extend(meteo_serializer.data)

            # Serialize WeatherMasterX records
            master_data = station.weather_master_x.all()
            master_serializer = UnifiedWeatherDataSerializer(master_data, many=True)
            combined_data.extend(master_serializer.data)

        # Sort combined data by timestamp in descending order
        combined_data = sorted(combined_data, key=lambda x: x['timestamp'], reverse=True)
        # Cache the response data for 1 hour (3600 seconds)
        cache.set(cache_key, combined_data, timeout=3600)
        # Paginate combined data
        return Response(combined_data, status=status.HTTP_200_OK)

class DailyAverageWeatherView(APIView):

    def get(self, request):
        try:
            # Validate and parse from and to dates
            from_date, to_date = validate_date_range(
                from_date=request.query_params.get('from'),
                to_date=request.query_params.get('to')
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Create a cache key using the date range
        cache_key = f"daily_avg_weather_{from_date}_{to_date}"
        
        # Check if data is already cached for this date range
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        weather_master_data = WeatherMasterX.objects.filter(recorded_at__gte=from_date, recorded_at__lte=to_date)
        meteo_data = BulgarianMeteoProData.objects.filter(timestamp__gte=from_date, timestamp__lte=to_date)

        # Aggregate WeatherMasterX data by date
        weather_master_avg = (
            weather_master_data
            .annotate(date=TruncDate('recorded_at'))
            .annotate(temp_celsius=ExpressionWrapper(
                (F('readings__temp_fahrenheit') - 32) * 5.0 / 9.0, output_field=FloatField()
            ))
            .values('date')
            .annotate(
                avg_temp_celsius=Avg('temp_celsius'),  # Use the annotated Celsius temperature
                avg_humidity=Avg('readings__humidity_percent'),
                avg_pressure=Avg('readings__pressure_hpa'),
                avg_uv_index=Avg('readings__uv_index'),
                avg_rainfall=Avg('readings__rain_mm')
            )
        )

        # Aggregate BulgarianMeteoProData data by date
        bulgarian_meteo_pro_avg = (
            meteo_data
            .annotate(date=TruncDate('timestamp'))
            .values('date')
            .annotate(
                avg_temp_celsius=Avg('temperature_celsius'),
                avg_humidity=Avg('humidity_percent'),
                avg_wind_speed=Avg('wind_speed_kph')
            )
        )
        
        daily_avg_data = combine_weather_data(weather_master_avg, bulgarian_meteo_pro_avg)
         # Convert WeatherDataEntry objects to dictionaries
        serialized_data = [entry.__dict__ for entry in daily_avg_data]
        # Cache the response for this date range
        cache.set(cache_key, serialized_data, timeout=3600)
        return Response(serialized_data, status=status.HTTP_200_OK)