from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from beerapp.models import CustomUser


# custom user creation includes fav_beer and fav_brewery
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'fav_beer', 'fav_brewery', )



class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'fav_beer', 'fav_brewery', )