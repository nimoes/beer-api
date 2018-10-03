# for api url structure

from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    # # ratebeer api
    # path('beer/<int:beer_id>/', views.beer_detail_view, name='beer_detail_view'),
    # # openbrewery api / ratebeer api
    # path('brewery/<slug:brewery_name>/', views.brewery_list_view, name='brewery_list_view')
]

"""
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views

from cryptocoins import views """