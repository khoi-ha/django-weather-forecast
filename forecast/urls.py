from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r"forecast/api", view=views.forecast, name="forecast"),
]