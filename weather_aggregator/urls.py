from django.contrib import admin
from django.urls import path, include
from stations import urls as stations_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('bulgarian_meteo_pro/', include('bulgarian_meteo_pro.urls')),
    path('api/', include(stations_urls)),
]
