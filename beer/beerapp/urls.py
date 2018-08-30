# for api url structure

from django.contrib import admin
from django.urls import path, include

from api import views

urlpatterns = [
    path('beer/<int:beer_id>/', views.beer_detail_view),
    path('brewery/')
    # path('people-detail/', views.single_people),
    # path('people-list/', views.list_people),

    # # actual views
    # path('people/<int:people_id>/', views.people_detail_view),
    # path('people/', views.people_list_view),
]