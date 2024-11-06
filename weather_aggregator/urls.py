from django.contrib import admin
from django.urls import path, include
from stations import urls as stations_urls
from bulgarian_meteo_pro import urls as bulgarian_meteo_pro_urls
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from weather_master_x import urls as weather_master_x_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(stations_urls)),
    path('api/', include(bulgarian_meteo_pro_urls)),
    path('api/', include(weather_master_x_urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # OpenAPI schema
    path('api/docs/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # ReDoc documentation

]
