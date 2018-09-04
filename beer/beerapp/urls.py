# for api url structure

from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # ratebeer api
    path('beer/<int:beer_id>/', views.beer_detail_view, name='beer_detail_view'),
    # openbrewery api / ratebeer api
    path('brewery/<slug:brewery_name>/', views.brewery_list_view, name='brewery_list_view')
    
    # test
    #path('beer/test/', views.test, name='test'),
    #path('<int:question_id>/', views.detail, name='detail'),
]