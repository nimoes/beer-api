from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from beerapp.models import CustomUser, Like, Dislike


# custom user creation includes fav_beer and fav_brewery
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'fav_beer', 'fav_brewery', )


class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'fav_beer', 'fav_brewery', )


class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ('brewid', 'name', )


class DisikeForm(forms.ModelForm):
    class Meta:
        model = Dislike
        fields = ('brewid', 'name', )