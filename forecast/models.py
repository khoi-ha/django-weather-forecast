from django.db import models

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

