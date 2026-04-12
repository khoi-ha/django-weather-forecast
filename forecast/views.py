from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from forecast.forecastAPI.forecast_api import generate_forecast_data
from forecast.forecastAPI.input_validation import validate_country, \
                                validate_city, validate_days
from forecast.geography.geoip import locate_by_request
from forecast.geography.location_api import generate_city_suggestions

DEFAULT_DAYS = "3"

# Limit the number of city suggestions to prevent overwhelming
# the user and to reduce database load
MAX_SUGGESTIONS = 20

def forecast(request: HttpRequest):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET requests are allowed"}, status=405)

    country = request.GET.get("country", "")
    if not validate_country(country):
        return JsonResponse({"error": "Invalid country format"}, status=400)

    state = request.GET.get("state", "")
    if state and not validate_country(state):
        return JsonResponse({"error": "Invalid state format"}, status=400)

    city = request.GET.get("city", "")
    if not validate_city(city):
        return JsonResponse({"error": "Invalid city format"}, status=400)
    
    days = request.GET.get("days", DEFAULT_DAYS)
    if not validate_days(days):
        return JsonResponse({"error": "Invalid days format"}, status=400)
    
    # Log the user's location to personalize the experience
    if not (country and city):
        country, city = locate_by_request(request)
    forecast_data = generate_forecast_data(int(days), city, country)
    if forecast_data is None:
        return JsonResponse({"error": "Could not generate forecast data"}, status=500)
    return JsonResponse(forecast_data)

def get_city_suggestions(request: HttpRequest):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET requests are allowed"}, status=405)

    keyword = request.GET.get("keyword", "")
    if not keyword:
        return JsonResponse({"error": "Query parameter is required"}, status=400)

    suggestions = generate_city_suggestions(keyword, MAX_SUGGESTIONS)
    return JsonResponse({"suggestions": suggestions})


def index(request: HttpRequest):
    return render(request, "html/index.html")
