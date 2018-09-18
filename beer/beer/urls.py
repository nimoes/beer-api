"""beer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
# from django.contrib.auth import views as auth_views

from beerapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('search_results', views.search_view, name='search_results'),
    path('test_api/', include('beerapp.urls'), name='results'),
    path('beer', views.beer_detail_view, name="beer_detail_view"),
    path('brewery', views.brewery_detail_view, name="brewery_detail_view"),
    
    
    # includes users account settings
    path('users/', include('django.contrib.auth.urls')),
    # for user signups
    path('users/', include('beerapp.urls')),
    
    # user's likes and dislikes
    path('my_profile/', views.user_favorites_view, name='my_profile'),
]
