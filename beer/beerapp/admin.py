from django.contrib import admin

# Register your models here.
from beerapp.models import Beer, Brewery

admin.site.register(Beer)
admin.site.register(Brewery)