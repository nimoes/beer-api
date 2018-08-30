from django.db import models



# Create your models here.
class Beer(models.Model):
    ID = models.IntegerField()
    name = models.CharField(max_length=50)
    brewer = models.CharField(max_length=50)
    alcohol = models.DecimalField(max_digits=4, decimal_places=2)
    hops = models.CharField(max_length=255)
    ideal_temp = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.CharField(max_length=255, null=True, blank=True)
    # does the beer get distributed within the states or only locally
    # distribution = models.BooleanField()
    
    def __str__(self):
        return "Beer: {} ({}%)".format(self.name, self.alcohol)


class Review(models.Model):
    # using ratebeer api
    '''
          id,
      comment,
      score,
      scores {appearance, aroma, flavor, mouthfeel, overall},
      beer {id, name},
      createdAt,
      updatedAt
    '''
    review_id = models.IntegerField(primary_key=True, blank=True)
    comment = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    # scores
    # beer


class Brewery(models.Model):
    # using openbrewerydb api
    id = models.IntegerField(primary_key=True, blank=True)
    brewery_name = models.ForeignKey(Beer, on_delete=models.CASCADE)
    brewery_type = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=14)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=20)
    longitude = models.DecimalField(max_digits=16, decimal_places=13)
    latitude = models.DecimalField(max_digits=16, decimal_places=13)
    phone = models.CharField(max_length=17)
    website_url = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Brewery: {}".format(self.brewery_name)

