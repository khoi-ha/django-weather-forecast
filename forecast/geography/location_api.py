import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoWeatherForecast.settings")
django.setup()


from forecast.models import Country, City

def generate_city_suggestions(keyword):
    """Generate city suggestions based on a keyword.

    Args:
        keyword (str): The keyword to search for in city names.

    Returns:
        list: A list of city suggestions that match the keyword.
    """
    if not keyword:
        return []
    
    # Search for cities that contain the keyword (case-insensitive)
    matching_cities = City().find_matching_cities(keyword)
    
    # Create a list of suggestions in the format "City, Country"
    suggestions = []
    for city in matching_cities:
        country_name = city.country.name
        if not country_name:
            country_name = "Unknown Country"
        if city.state:
            suggestions.append(f"{city.name}, {city.state}, {country_name}")
        else:
            suggestions.append(f"{city.name}, {country_name}")

    return {"count": len(suggestions), "suggestions": suggestions}