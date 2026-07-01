import os
import sys
import django
from django.db import IntegrityError
import json
import logging

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoWeatherForecast.settings")
django.setup()

from forecast.models import Weather, InfoType

logger = logging.getLogger(__name__)

DEFAULT_DATA_DIR = "forecast/openWeather/default_data"
DEFAULT_WEATHER_TYPES_FILE = os.path.join(DEFAULT_DATA_DIR, "weather_conditions.json")
DEFAULT_INFO_TYPES_FILE = os.path.join(DEFAULT_DATA_DIR, "info_types.json")

def import_weather_types():
    """Import weather types from a JSON file into the database."""

    if not os.path.exists(DEFAULT_WEATHER_TYPES_FILE):
        logger.debug("Default weather types JSON file not found. Skipping import.")
        return

    with open(DEFAULT_WEATHER_TYPES_FILE, "r") as f:

        try:
            weather_types = json.load(f)
        except json.JSONDecodeError:
            logger.debug("Error decoding JSON from weather types file. Skipping import.")
            return

        for index, weather in enumerate(weather_types):
            try:
                Weather.objects.get_or_create(
                    id=index,
                    name=weather["weather_type"],
                    icon=weather["icon"]
                )
            except IntegrityError:
                logger.debug(f"Weather type '{weather['weather_type']}' already exists. Skipping.")
        f.close()

def import_info_types():
    """Import information types from a JSON file into the database."""
    if not os.path.exists(os.path.join(DEFAULT_DATA_DIR, "info_types.json")):
        logger.debug("Default information types JSON file not found. Skipping import.")
        return

    with open(os.path.join(DEFAULT_DATA_DIR, "info_types.json"), "r") as f:

        try:
            info_types = json.load(f)
        except json.JSONDecodeError:
            logger.debug("Error decoding JSON from information types file. Skipping import.")
            return

        for info in info_types:
            try:
                InfoType.objects.get_or_create(
                    type=info["type"],
                    icon=info["icon"]
                )
            except IntegrityError:
                logger.debug(f"Info type '{info['type']}' already exists. Skipping.")

if __name__ == "__main__":
    import_weather_types()
    import_info_types()
    logger.debug("Default data import completed.")