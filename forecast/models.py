from django.db import models

class Country(models.Model):
    """Model representing a country. The purpose is to map the country code to the country name."""
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=32, unique=True, default="")

    def get_country_code(self, country_name):
        """Get the country code for a given country name.

        Args:
            country_name (str): The name of the country to search for.

        Returns:
            str: The country code if found, otherwise None.
        """
        country = Country.objects.filter(name__iexact=country_name).first()
        if country:
            return country.code
        return None
    
    def get_country_name(self, country_code):
        """Get the country name for a given country code.

        Args:
            country_code (str): The code of the country to search for.

        Returns:
            str: The country name if found, otherwise None.
        """
        country = Country.objects.filter(code__iexact=country_code).first()
        if country:
            return country.name
        return None

class City(models.Model):
    """Model representing a city. The purpose is to store city names and their geographical coordinates."""
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, default="")
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)

    def get_coordinates(self, city, country_code):
        """Get the geographical coordinates of a city by its name.

        Args:
            keyword (str): The name of the city to search for.

        Returns:
            (float, float): The latitude and longitude of the city, or None if not found.
        """
        city = City.objects.filter(name__iexact=city, 
                                   country__code=country_code).first()
        if city:
            return (city.lat, city.lon)
        return None
    
    def find_matching_cities(self, keyword):
        """Find cities that match a given keyword.

        Args:
            keyword (str): The keyword to search for in city names.

        Returns:
            QuerySet: A queryset of matching cities.
        """
        return City.objects.filter(name__icontains=keyword)
        return City.objects.filter(name__icontains=keyword)

class Weather(models.Model):
    """Model representing a weather condition."""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80, unique=True, default="")
    icon = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)

class InfoType(models.Model):
    """Model representing an information type."""
    type = models.CharField(max_length=20, unique=True,primary_key=True)
    icon = models.CharField(max_length=200)

class Background(models.Model):
    """Model representing a background image for a specific weather condition."""
    weather_type = models.ForeignKey(Weather, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, unique=True, default="")
    link = models.CharField(max_length=200, unique=True)

    def get_random_background(self, weather_type):
        """Get a random background image link for a given weather type.

        Args:
            weather_type (str): The type of weather to get the background for.

        Returns:
            str: The URL of the background image, or None if not found.
        """
        background = Background.objects.filter(weather_type__name__iexact=weather_type).order_by("?").first()
        if background:
            return background.link
        return ""
    
    def __str__(self):        
        return f"{self.name}"

