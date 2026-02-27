from django.db import models

class Country(models.Model):
    """Model representing a country. The purpose is to map the country code to the country name."""
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=32, unique=True)

class City(models.Model):
    """Model representing a city. The purpose is to store city names and their geographical coordinates."""
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    lat = models.FloatField()
    lon = models.FloatField()

    def get_coordinates(self, keyword):
        """Get the geographical coordinates of a city by its name.

        Args:
            keyword (str): The name of the city to search for.

        Returns:
            (float, float): The latitude and longitude of the city, or None if not found.
        """
        city = City.objects.filter(name__icontains=keyword).first()
        if city:
            return (city.lat, city.lon)
        return None

class Weather(models.Model):
    """Model representing a weather condition."""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80, unique=True)
    icon = models.CharField(max_length=200, unique=True)

class InfoType(models.Model):
    """Model representing an information type."""
    type = models.CharField(max_length=20, unique=True)
    icon = models.CharField(max_length=200, unique=True)

class Background(models.Model):
    """Model representing a background image for a specific weather condition."""
    weather_type = models.ForeignKey(Weather, on_delete=models.CASCADE)
    link = models.CharField(max_length=200, unique=True)
