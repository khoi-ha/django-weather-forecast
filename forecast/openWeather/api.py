from os import getenv

import sys
sys.path.append("..")

from openWeather.request_format import send_get_request

OPENWEATHER_API_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"

# Loads the OpenWeather API key from environment variables
OPENWEATHER_API_KEY = getenv("OPENWEATHER_API_KEY")


def get_weather_data(lat:float, lon:float):
    """Gets weather data from the OpenWeather free API

    Args:
        lat (float): Latitude of the location to get weather data of 
        lon (float): Longtitude of the location to get weather data of

    Returns:
        The contents of the response from the API
    """
    response = send_get_request(
        OPENWEATHER_API_ENDPOINT, 
        {},
        lat=lat,
        lon=lon,
        appid=OPENWEATHER_API_KEY
    )
    
    if not response:
        return {}
    
    return response.json()
