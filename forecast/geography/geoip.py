from os import getenv
from django.http.request import HttpRequest
from ipware import get_client_ip 
from iplocate import IPLocateClient

IPLOCATE_KEY = getenv("IPLOCATE_API_KEY")
IPLOCATE_ENDPOINT = "https://iplocate.io/api/lookup/"

# Default location to use in case the GeoIP service fails
DEFAULT_LOCATION = ("United Kingdom", "London")


def get_ip(request:HttpRequest)->str:
    """
    Get the client's IP address from the request.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        str: The client's IP address or an empty string if not found.
    """
    client_ip, is_routable = get_client_ip(request)

    # Attempt to determine IP from request
    if not client_ip:
        print("Error: Failed to get client IP.")
        return ""
    else:
        # Check if obtained IP address is publicly routable
        if is_routable:
            return client_ip
        else:
            print(f"Error: IP address {client_ip} is not routable.")
            return ""


def approximate_location(ipv4:str)->tuple:
    """
    Get the approximate location (country, city) for a given IPv4 address.

    Args:
        ipv4 (str): The IPv4 address to look up.

    Returns:
        tuple: A tuple containing the country code and city name.
    """
    if not ipv4:
        return DEFAULT_LOCATION
    
    client = IPLocateClient(api_key=IPLOCATE_KEY)

    try:
        # Attempt IP lookup
        result = client.lookup(ipv4)
    except Exception as e:
        print(f"Error: Location lookup for address {ipv4} failed. See below for more details.")
        print(e)
        return DEFAULT_LOCATION
    
    if not (result.country or result.city):
        return DEFAULT_LOCATION

    return (result.country, result.city)


def locate_by_request(request:HttpRequest):
    return approximate_location(get_ip(request))


if __name__ == "__main__":
    
    from dotenv import load_dotenv
    from django.test import RequestFactory

    load_dotenv()

    # Test the GeoIP API
    TEST_IP_V4 = getenv("IPV4")
    if TEST_IP_V4:
        print(approximate_location(TEST_IP_V4))
    
    # Set up minimal Django app for testing
    from django.conf import settings
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            SECRET_KEY="dummy",
            ALLOWED_HOSTS=[],
            USE_TZ=True,
        )
    from django import setup
    setup()

    # Test approximating location from requests
    TEST_REMOTE = getenv("REMOTE")
    rf = RequestFactory()
    request = rf.get(
        "/",
        DEFAULT_CHARSET = "utf-8",
        REMOTE_ADDR="127.0.0.1",
        HTTP_X_FORWARDED_FOR=TEST_REMOTE
    )
    print(locate_by_request(request))
