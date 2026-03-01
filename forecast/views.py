from django.shortcuts import render
from django.http import JsonResponse
from forecast.forecastAPI.forecast_api import generate_forecast_data
from forecast.forecastAPI.input_validation import validate_country, \
                                validate_city, validate_days

DEFAULT_COUNTRY = "United Kingdom"
DEFAULT_CITY = "London"
DEFAULT_DAYS = "3"

def forecast(request):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET requests are allowed"}, status=405)

    country = request.GET.get("country", DEFAULT_COUNTRY)
    if not validate_country(country):
        return JsonResponse({"error": "Invalid country format"}, status=400)
    
    city = request.GET.get("city", DEFAULT_CITY)
    if not validate_city(city):
        return JsonResponse({"error": "Invalid city format"}, status=400)
    
    days = request.GET.get("days", DEFAULT_DAYS)
    if not validate_days(days):
        return JsonResponse({"error": "Invalid days format"}, status=400)

    forecast_data = generate_forecast_data(int(days), city, country)
    if forecast_data is None:
        return JsonResponse({"error": "Could not generate forecast data"}, status=500)
    return JsonResponse(forecast_data)

def index(request):
    return render(request, "html/index.html")
