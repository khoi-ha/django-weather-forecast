from django.urls import path

from . import views

urlpatterns = [
    path("geography/api/city_suggestions", view=views.get_city_suggestions, name="city_suggestions_api"),
]