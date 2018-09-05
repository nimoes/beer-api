from django import forms

from .models import Beer, Brewery

class BeerForm(forms.ModelForm):
    class Meta:
        model = Beer
        fields = ('brewer',)

class BreweryForm(forms.ModelForm):
    class Meta:
        model = Brewery
        fields = ('brewery_name', 'streetAddress', 'city', 'state', 'postal_code', 'country',)