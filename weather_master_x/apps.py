from django.apps import AppConfig


class WeatherMasterXConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather_master_x'
    
    def ready(self):
        import weather_master_x.signals
