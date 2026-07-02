from django.urls import path

from . import views

urlpatterns = [
    path("",view=views.index, name="forecast_ui"),
    path("forecast/api", view=views.forecast, name="forecast_api"),
]