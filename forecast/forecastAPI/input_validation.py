import re

COUNTRY_RE = re.compile(r"^[A-Za-z\ ]{2,50}$")
CITY_RE = re.compile(r"^[A-Za-z\s-]{1,100}$")
MAX_DAYS = 4


def validate_country(country:str)->bool:
    """Validate the country parameter's format.

    Args:
        country (str): The country name to validate.

    Returns:
        bool: True if the country is valid, False otherwise.
    """
    return COUNTRY_RE.match(country) is not None


def validate_city(city:str)->bool:
    """Validate the city parameter's format.

    Args:
        city (str): The city name to validate.

    Returns:
        bool: True if the city is valid, False otherwise.
    """
    return CITY_RE.match(city) is not None


def validate_days(days:str)->bool:
    """Validate the days parameter.

    Args:
        days (str): The number of days to validate.

    Returns:
        bool: True if the days are valid, False otherwise.
    """
    return days.isdigit() and (1 <= int(days) <= MAX_DAYS)
