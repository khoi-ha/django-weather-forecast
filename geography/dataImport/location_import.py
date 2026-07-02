import os
import sys
import requests
import gzip
import shutil
import json
import django
import logging
from django.db import connection, transaction

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoWeatherForecast.settings")
django.setup()

from forecast.models import Country

logger = logging.getLogger(__name__)

LOCATION_DATA_DIRNAME = os.path.join(os.path.dirname(__file__), "data")
CITY_LIST_FILENAME = "city.list.min.json"
CITY_LIST_GZ_FILENAME = "city.list.min.json.gz"
COUNTRY_CODES_URL = "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/refs/heads/master/json/countries.json"
OPENWEATHER_CITY_LIST_URL = "http://bulk.openweathermap.org/sample/city.list.min.json.gz"


def fetch_country_codes():
    """Fetch the list of country codes from the remote JSON file.

    Raises:
        Exception: If the request to fetch country codes fails.

    Returns:
        list: A list of country codes and names.
    """
    response = requests.get(COUNTRY_CODES_URL)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch country codes. Response code: {response.status_code}")
    

def import_country_codes():
    """Import country codes into the database.
    """
    country_codes = fetch_country_codes()
    for country in country_codes:
        try:
            Country.objects.get_or_create(code=country["iso2"], name=country["name"])
            logger.debug(f"Imported country: {country['name']}, {country['iso2']}")
        except Exception as e:
            logger.debug(f"Error importing country {country['name']}: {e}")


def unzip_city_list():
    """Unzip the city list from a .gz file.
    """
    with gzip.open(f"{LOCATION_DATA_DIRNAME}/{CITY_LIST_GZ_FILENAME}", "rb") as f_in:
        with open(f"{LOCATION_DATA_DIRNAME}/{CITY_LIST_FILENAME}", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
            f_out.close()
        f_in.close()


def fetch_city_list():
    """Fetch the city list from the OpenWeather API.

    Raises:
        Exception: If the request to fetch the city list fails.
    """
    if os.path.exists(f"{LOCATION_DATA_DIRNAME}/{CITY_LIST_FILENAME}"):
        logger.debug("City list already exists. Skipping download")
        return
    response = requests.get(OPENWEATHER_CITY_LIST_URL)
    if response.status_code == 200:
        with open(f"{LOCATION_DATA_DIRNAME}/{CITY_LIST_GZ_FILENAME}", "wb") as f:
            f.write(response.content)
            f.close()
    else:
        raise Exception(f"Failed to fetch city list. Response code: {response.status_code}")
    unzip_city_list()


CITY_TAB_NAME = "forecast_city"
@transaction.atomic
def import_city_list():
    """Import city list into the database.
    """
    fetch_city_list()

    # Load city list
    city_list = None
    with open(f"{LOCATION_DATA_DIRNAME}/{CITY_LIST_FILENAME}", "r", encoding="utf-8") as f:
        city_list = json.load(f)
        f.close()
    
    # Build country map    
    country_set = set([
        country.code for country in Country.objects.only("code")
    ])

    # Insert into the temp table
    with connection.cursor() as cursor:    
        cursor.execute(f"""CREATE TEMP TABLE tmp_city 
                            (LIKE {CITY_TAB_NAME} INCLUDING DEFAULTS)""")
        with cursor.copy(
            "COPY tmp_city (id, name, lat, lon, country_id, state) FROM STDIN"
        ) as copy:
            for city in city_list:
                country_code = city["country"]
                if country_code not in country_set:
                    continue
                copy.write_row((int(city["id"]), city["name"], city["coord"]["lat"],
                            city["coord"]["lon"], country_code,
                            city["state"]))
                if city["state"]:
                    logger.debug(f"Imported city: {city['name']}, {city['state']}, {country_code}")
                else:
                    logger.debug(f"Imported city: {city['name']}, {country_code}")
    
    # Inserting from temp table to real table            
    with connection.cursor() as cursor:
        cursor.execute(
            f""" 
            INSERT INTO {CITY_TAB_NAME} (id, name, lat, lon, country_id, state)
                SELECT id, name, lat, lon, country_id, state
                FROM tmp_city
                ON CONFLICT(id)
                DO NOTHING
            """
        )

if __name__ == "__main__":
    if not os.path.exists(LOCATION_DATA_DIRNAME):
        os.makedirs(LOCATION_DATA_DIRNAME)
    import_country_codes()
    import_city_list()