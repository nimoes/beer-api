# for custom user creation
from django.db import models
from django.contrib.auth.models import AbstractUser

# from django.utils.timezone import now
# from decimal import Decimal


# User model inherited from AbstractUser class
class CustomUser(AbstractUser):
    fav_beer = models.CharField(max_length=255)
    fav_brewery = models.CharField(max_length=255)


# '''
# {"data": 
# 	{"brewerSearch": 
# 		{"items": 
# 			[{
# 			"description": "", 
# 			"phone": "999-2192", 
# 			"zip": "20170", 
# 			"city": "Herndon", 
# 			"name": "Aslin Beer Company", 
# 			"type": "Microbrewery", 
# 			"streetAddress": "257 Sunset Park Dr.", 
# 			"id": "24435", 
# 			"state": {
# 				"name": "Virginia"
# 				}, 
# 			"imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_150,c_limit,d_brewerdefault_hk6nu1.png,f_auto/brew_24435.jpg", 
# 			"isRetired": false, 
# 			"score": 117693
# 			}, 
# 			{
# 			"description": "", 
# 			"phone": "902-1805", 
# 			"zip": "98225", 
# 			"city": "Bellingham", 
# 			"name": "Aslan Brewing Company", 
# 			"type": "Brew Pub/Brewery", 
# 			"streetAddress": "1330 N Forest Street", 
# 			"id": "19337", 
# 			"state": {
# 				"name": "Washington"
# 				}, 
# 			"imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_150,c_limit,d_brewerdefault_hk6nu1.png,f_auto/brew_19337.jpg", 
# 			"isRetired": false, 
# 			"score": 60322
# 			}]
# 		}
# 	}
# }
# '''
# class Brewery(models.Model):
#     '''
#         Uses ratebeer's api to instantiate appropriate fields
#     '''
#     brewer_api_id = models.IntegerField(primary_key=True, blank=True, default=0)
#     # brewery_name = models.SlugField(unique=True)
#     brewery_name = models.CharField(max_length=255)
#     brewery_type = models.CharField(max_length=255)
#     streetAddress = models.CharField(max_length=255)
#     city = models.CharField(max_length=50)
#     state = models.CharField(max_length=14)
#     postal_code = models.CharField(max_length=10)
#     country = models.CharField(max_length=20)
#     longitude = models.DecimalField(max_digits=16, decimal_places=13, default=Decimal('000.0000000000000'))
#     latitude = models.DecimalField(max_digits=16, decimal_places=13, default=Decimal('000.0000000000000'))
#     phone = models.CharField(max_length=17)
#     website_url = models.URLField(max_length=200)
#     updated_at = models.DateTimeField(auto_now_add=True)
#     # for search box
#     # slug = models.SlugField(max_length=200)
    
#     def __str__(self):
#         return "Brewery: {}".format(self.brewery_name)


# '''
# Sample Beer API output (ratebeer)
# {"data": 
# 	{"beer": 
# 		{"description": "Filtered and pasteurised. Available in nitro cans and nitro kegs.\nProduction moved to the former Murphys brewery on closure of the Beamish & Crawford brewery in 2009.", "averageRating": 3.364453077316284, 
# 		"realAverage": 3.3660523891448975, 
# 		"contractBrewer": null, 
# 		"brewer": 
# 			{
# 			"description": null, 
# 			"phone": "353.21.450.3371", 
# 			"zip": "\nFounded 1856", 
# 			"city": "Cork", 
# 			"name": "Heineken Ireland", 
# 			"type": "Commercial Brewery", 
# 			"streetAddress": "58 Leitrim Street", 
# 			"id": "184", 
# 			"state": 
# 				{"name": ""}, 
# 			"imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_150,c_limit,d_brewerdefault_hk6nu1.png,f_auto/brew_184.jpg", 
# 			"isRetired": false, 
# 			"score": 116804
# 			}, 
# 		"name": "Beamish Irish Stout", 
# 		"labels": [], 
# 		"styleScore": 79.80014457959733, 
# 		"ibu": null, 
# 		"id": "1", 
# 		"seasonal": "UNKNOWN", 
# 		"overallScore": 71.06762745306455, 
# 		"style": 
# 			{
# 			"description": "The &quotIrish-style&quot stout is typically a low-gravity stout with bitterness ranging between 30-45 IBUs. Roastiness is present, but restrained, and there should not be hops in either the flavour or aroma. A little bit of acidity can be present. Often, this type of stout is serving via nitrogen, with all the effects that has on a beer - low carbonation, extra-thick head, lifeless palate and muted flavour and aroma.", "name": "Dry Stout", "glasses": 
# 				[{
# 				"description": "These have a similar purpose to the shaker in that they are made for session ales, in this case bitters, milds, porters and stouts. There are a couple of key differences. First, they pour a proper pint (and usually have a line indicating where that is on the glass, just to make sure you don\u2019t get ripped off). Second, they have a bit more flourish than the bland shaker. There are basically two variations. The first has a gentle curve covering the upper 2/3 of the glass - Guinness uses these. The second has a straight slope for the bottom two-thirds, and then a bump near the top, flattening out at the mouth of the glass.", 
# 				"name": "English pint"
# 				}, 
# 				{
# 				"description": "The American microbrewer\u2019s standard. A gently sloped 16 oz. glass made for session-type beers. Ambers, English & American pales, and sometimes darker session ales are typically served in these glasses, which are better known for their durability, than for any particularly beneficial properties. It is for that reason that some beer geeks have developed a hatred of the shaker.", 
# 				"name": "Shaker"
# 				}
# 				]
# 			}, 
# 		"confidence": null, 
# 		"ratingCount": 1031, 
# 		"calories": 123, 
# 		"abv": 4.099999904632568, 
# 		"imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_120,c_limit,d_beer_icon_default.png,f_auto/beer_1.jpg", "purchase": null, 
# 		"availability": 
# 			{
# 			"bottle": "unknown", 
# 			"tap": "unknown", 
# 			"distribution": "unknown"
# 			}
# 		}
# 	}
# }
# '''

# class Beer(models.Model):
#     beer_api_id = models.IntegerField(default=0)
#     description = models.TextField()
#     avg_score = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('000.00'))
#     name = models.CharField(max_length=255)
#     brewer = models.ForeignKey(Brewery, on_delete=models.CASCADE)
#     # brewer_api_id = 
#     ibu = models.DecimalField(max_digits=4, decimal_places=1, default=Decimal('000.0'))
#     abv = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('00.00'))
#     calories = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('000.00'))
#     # hops = models.CharField(max_length=255)
#     # ideal_temp = models.DecimalField(max_digits=4, decimal_places=2)
#     # does the beer get distributed within the states or only locally
#     # distribution = models.BooleanField()
    
#     def __str__(self):
#         return "Beer: {} ({}%)".format(self.name, self.abv)
