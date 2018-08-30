import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

# from api.models import Beer, Brewery

def index(request):
    return HttpResponse("Hello Caleb.")