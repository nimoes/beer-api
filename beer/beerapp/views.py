import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from beerapp.models import Beer, Brewery, Review
from beerapp.ratebeer import *

def index(request):
    return JsonResponse(getBeer(1))

@csrf_exempt
def brewery_list_view(request):
    pass
    """
    Brewery 'list' actions:

    Based on the request method, perform the following actions:

        * GET: Returns the `Brewery` object based on brewery_name


    Make sure you add at least these validations:
        * If the view receives another HTTP method out of the ones listed
          above, return a `400` response.

        * If submited payload is nos JSON valid, return a `400` response.
    """
    
@csrf_exempt
def beer_detail_view(request, beer_id):
    pass
    """
    Beer 'list' actions:

    Based on the request method, perform the following actions:

        * GET: Returns the `Beer` object based on beer_id

    Make sure you add at least these validations:
        * If the view receives another HTTP method out of the ones listed
          above, return a `400` response.

        * If submited payload is nos JSON valid, return a `400` response.
    """


@csrf_exempt
def user_detail_view(request, user_id):
    pass