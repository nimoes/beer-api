from django.contrib import admin

# Register your models here.
from beerapp.models import Beer, Brewery, Review

admin.site.register(Beer)
admin.site.register(Brewery)
admin.site.register(Review)