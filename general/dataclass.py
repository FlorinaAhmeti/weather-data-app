from dataclasses import dataclass
from typing import Optional
from datetime import date
@dataclass
class AvgWeatherDataEntry:
    date: date
    avg_temp_celsius: Optional[float] = None
    avg_humidity: Optional[float] = None
    avg_pressure: Optional[float] = None
    avg_uv_index: Optional[int] = None
    avg_rainfall: Optional[float] = None
    avg_wind_speed: Optional[float] = None