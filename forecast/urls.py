from django.urls import path

from . import views

urlpatterns = [
    path("",view=views.index, name="forecast_ui"),
    path("forecast/api", view=views.forecast, name="forecast_api"),
    path("geography/api/city_suggestions", view=views.get_city_suggestions, name="city_suggestions_api"),
]