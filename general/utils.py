from datetime import datetime
from typing import Optional, Dict, List
from general.dataclass import WeatherDataEntry
from django.core.cache import cache


def validate_date_range(from_date: Optional[str] = None, to_date: Optional[str] = None) -> tuple[Optional[datetime], Optional[datetime]]:
    """
    Validates and converts from_date and to_date strings in DD/MM/YYYY format to datetime objects.
    If to_date is not provided, defaults to today's date.

    Args:
        from_date (str): The starting date in 'DD/MM/YYYY' format.
        to_date (str): The ending date in 'DD/MM/YYYY' format.

    Returns:
        dict: A dictionary with 'from' and 'to' keys containing datetime objects or None if dates are not provided.
    
    Raises:
        ValueError: If the date format is invalid or if from_date is after to_date.
    """
    # Parse from_date
    if from_date:
        try:
            from_date_parsed = datetime.strptime(from_date, "%d/%m/%Y").replace(hour=0, minute=0, second=0)
        except ValueError:
            raise ValueError("Invalid 'from' date format. Use 'DD/MM/YYYY'.")

    # Parse to_date or default to today's date
    if to_date:
        try:
            to_date_parsed = datetime.strptime(to_date, "%d/%m/%Y").replace(hour=23, minute=59, second=59)
        except ValueError:
            raise ValueError("Invalid 'to' date format. Use 'DD/MM/YYYY'.")
    else:
        # Default to today's date at the end of the day
        to_date_parsed = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)

    if from_date_parsed > to_date_parsed:
        raise ValueError("The 'from' date must be earlier than or equal to the 'to' date.")

    return (from_date_parsed, to_date_parsed)

def create_weather_entry(entry: Dict, source: str) -> WeatherDataEntry:
    """Creates a WeatherDataEntry from an entry based on the data source."""
    if source == "weather_master":
        return WeatherDataEntry(
            date=entry['date'],
            avg_temp_celsius=entry.get('avg_temp_celsius'),
            avg_humidity=entry.get('avg_humidity'),
            avg_pressure=entry.get('avg_pressure'),
            avg_uv_index=entry.get('avg_uv_index'),
            avg_rainfall=entry.get('avg_rainfall'),
            avg_wind_speed=None  # No wind speed data in WeatherMasterX
        )
    elif source == "meteo":
        return WeatherDataEntry(
            date=entry['date'],
            avg_temp_celsius=entry.get('avg_temp_celsius'),
            avg_humidity=entry.get('avg_humidity'),
            avg_pressure=None,  # No pressure data in BulgarianMeteoProData
            avg_uv_index=None,  # No UV index data in BulgarianMeteoProData
            avg_rainfall=None,  # No rainfall data in BulgarianMeteoProData
            avg_wind_speed=entry.get('avg_wind_speed')
        )
            
def update_weather_entry(existing_entry: WeatherDataEntry, new_entry: WeatherDataEntry) -> None:
    """Updates an existing WeatherDataEntry with values from a new entry, averaging where applicable."""
    if new_entry.avg_temp_celsius is not None:
        existing_entry.avg_temp_celsius = (
            (existing_entry.avg_temp_celsius + new_entry.avg_temp_celsius) / 2
            if existing_entry.avg_temp_celsius is not None else new_entry.avg_temp_celsius
        )
    if new_entry.avg_humidity is not None:
        existing_entry.avg_humidity = (
            (existing_entry.avg_humidity + new_entry.avg_humidity) / 2
            if existing_entry.avg_humidity is not None else new_entry.avg_humidity
        )
    if new_entry.avg_wind_speed is not None:
        existing_entry.avg_wind_speed = new_entry.avg_wind_speed

def combine_weather_data(master_data_x: List[Dict], bulgarian_metro_pro: List[Dict]) -> List[WeatherDataEntry]:
    """
    Combines data from WeatherMasterX and BulgarianMeteoProData into WeatherDataEntry dataclass instances.

    Args:
        master_data_x (List[Dict]): Aggregated data from WeatherMasterX.
        bulgarian_metro_pro (List[Dict]): Aggregated data from BulgarianMeteoProData.

    Returns:
        List[WeatherDataEntry]: A list of WeatherDataEntry instances with combined data.
    """
    combined_data = {}

    # Process WeatherMasterX data
    for entry in master_data_x:
        date = entry['date']
        if date in combined_data:
            # Update the existing entry with new values
            update_weather_entry(combined_data[date], create_weather_entry(entry, source="weather_master"))
        else:
            # Create a new entry if not already in combined_data
            combined_data[date] = create_weather_entry(entry, source="weather_master")

    # Process BulgarianMeteoProData data, updating or adding entries as needed
    for entry in bulgarian_metro_pro:
        date = entry['date']
        if date in combined_data:
            # Update the existing entry with new values
            update_weather_entry(combined_data[date], create_weather_entry(entry, source="meteo"))
        else:
            # Create a new entry if not already in combined_data
            combined_data[date] = create_weather_entry(entry, source="meteo")

    # Convert combined data to a sorted list
    return sorted(combined_data.values(), key=lambda x: x.date)

def clear_city_cache(city_name):
    cache_key = f"city_weather_data_{city_name}"
    cache.delete(cache_key)
    
def clear_daily_avg_weather_cache(from_date, to_date):
    cache_key = f"daily_avg_weather_{from_date}_{to_date}"
    cache.delete(cache_key)