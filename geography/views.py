from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from geography.suggestions.suggestions_api import generate_city_suggestions

# Limit the number of city suggestions to prevent overwhelming
# the user and to reduce database load
MAX_SUGGESTIONS = 20

def get_city_suggestions(request: HttpRequest):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET requests are allowed"}, status=405)

    keyword = request.GET.get("keyword", "")
    if not keyword:
        return JsonResponse({"error": "Query parameter is required"}, status=400)

    suggestions = generate_city_suggestions(keyword, MAX_SUGGESTIONS)
    return JsonResponse({"suggestions": suggestions})