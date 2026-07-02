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

class City(models.Model):
    """Model representing a city. The purpose is to store city names and their geographical coordinates."""
    name = models.CharField(max_length=80, default="")
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.CharField(max_length=80, default="")
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
    
    def find_matching_cities(self, keyword, suggestion_limit=20):
        """Find cities that match a given keyword.

        Args:
            keyword (str): The keyword to search for in city names.

        Returns:
            QuerySet: A queryset of matching cities.
        """
        return City.objects \
                   .filter(name__istartswith=keyword) \
                   .values_list('name', 'country__name', 'state')[:suggestion_limit]