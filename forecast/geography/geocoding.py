import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoWeatherForecast.settings")
django.setup()

from forecast.models import City

def get_city_coordinates(city_name):
    """Get the geographical coordinates of a city by its name.

    Args:
        city_name (str): The name of the city to search for.

    Returns:
        (float, float): The latitude and longitude of the city, or None if not found.
    """
    city = City()
    coordinates = City.get_coordinates(city, city_name)
    if coordinates:
        return coordinates
    print(f"City '{city_name}' not found in database.")
    return None