import os
import sys
import django
import datetime

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoWeatherForecast.settings")
django.setup()

from forecast.openWeather.api import get_weather_data
from forecast.openWeather.data_processing import calculate_daily_forecasts
from forecast.models import Country, City, Weather, InfoType, Background


def get_weather_icon(weather_type):
    """Get the weather icon for a given weather type.

    Args:
        weather_type (str): The type of weather to get the icon for.

    Returns:
        str: The URL of the weather icon, or None if not found.
    """
    weather_icon = Weather.objects.filter(name__iexact=weather_type).first()
    
    if weather_icon is None:
        print(f"Could not find icon for weather type: {weather_type}.")
        return None
    return weather_icon.icon


def generate_forecast_data(days, city_name, country_name):
    """Generate weather forecast API data for a specific city and country.

    Args:
        days (int): The number of days to forecast.
        city_name (str): The name of the city to forecast.
        country_name (str): The name of the country the city is in.

    Returns:
        str: A JSON string containing the forecast data.
    """
    country_code = Country().get_country_code(country_name)
    
    if country_code is None:
        print(f"Could not find country code for the country: {country_name}.")
        return
    city_coordinates = City().get_coordinates(city_name, country_code)
    
    if city_coordinates is None:
        print(f"Could not find coordinates for the city: {city_name}.")
        return

    weather_data = get_weather_data(city_coordinates[0], city_coordinates[1])
    daily_forecasts = calculate_daily_forecasts(weather_data, days)
    
    api_response_entries = []
    for forecast in daily_forecasts:
        entry = {
            "city": city_name,
            "country": country_code,
            "date": forecast["date"],
            "weather": {
                "type": forecast["weather_type"],
                "icon": get_weather_icon(forecast["weather_type"]),
                "background": Background().get_random_background(forecast["weather_type"]),
                "description": forecast["description"],
                "temp_min": forecast["temp_min"],
                "temp_max": forecast["temp_max"],
                "feels_like": forecast["feels_like"],
                "rain": forecast["rain"],
                "snow": forecast["snow"],
                "cloud_cover": forecast["cloud_cover"],
                "wind_speed": forecast["wind_speed"]
            }
        }
        
        api_response_entries.append(entry)

    api_response = {
    "dt": datetime.datetime.now().isoformat(),
    "weather_data": api_response_entries
    }

    return api_response
