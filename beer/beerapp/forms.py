from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from beerapp.models import CustomUser, Like, LikeBeer


# custom user creation includes fav_beer and fav_brewery
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'fav_beer', 'fav_brewery', )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'fav_beer', 'fav_brewery', )


# for liked breweries
class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ('brewid', 'name', 'imageUrl')
        

# for liked beers
class LikeBeerForm(forms.ModelForm):
    class Meta:
        model = LikeBeer
        fields = ('beerid', 'beername', 'beerimg', )