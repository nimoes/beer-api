from django.db import models

# Create your models here.
class Beer(models.Model):
    name = models.CharField(max_length=50)
    brewery = models.CharField(max_length=50)
    alcohol = models.DecimalField(max_digits=4, decimal_places=2)
    ideal_temp = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.models.CharField(max_length=255, null=True, blank=True)
    # does the beer get distributed within the states or only locally
    # distribution = models.BooleanField()
    
    def __str__(self):
        return self.name


class Brewery(models.Model):
    id = models.IntegerField(null=True, blank=True)
    name = models.ForeignKey(Beer, on_delete=models.CASCADE)
    brewery_type = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    postal_code = models.IntegerField(max_length=5)
    country = models.CharField(max_length=20)
    longitude = models.DecimalField(max_digits=20)
    latitude = models.DecimalField(max_digits=20)
    phone = models.CharField(max_length=17)
    website_url = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
