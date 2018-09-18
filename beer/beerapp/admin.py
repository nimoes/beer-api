from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .forms import CustomUserCreationForm, CustomUserChangeForm
from beerapp.models import CustomUser, Like, Dislike

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['email', 'username', 'fav_beer', 'fav_brewery']
    model = CustomUser

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Like)
admin.site.register(Dislike)