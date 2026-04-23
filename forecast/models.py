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

    def get_random_backgrounds(self, weather_type, days):
        """Get a random background image link for a given weather type.
    
        Args:
            weather_type (str): The type of weather to get the background for.
            days (int): The number of days to get backgrounds for.

        Returns:
            list: A list of background image URLs, or an empty list if not found.
        """

        link_objs = list(Background.objects
                         .filter(weather_type__name__iexact=weather_type)
                         .values_list("link").order_by('?')[:days])
        links = [k[0] for k in link_objs if k]

        # Repeat means how many time to repeat the link list in the final list
        repeats = days // len(links)
        # Padding means the number of items that are taken from the start of the
        # link list and added to the back of the padded list for it reach the 
        # required number of days
        padding = days % len(links)
        padded_links = links*repeats
        padded_links.extend(links[:padding])

        return padded_links

    def __str__(self):
        return f"{self.name}"

