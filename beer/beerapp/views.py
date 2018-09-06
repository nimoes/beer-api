import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseForbidden
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from beerapp.models import Beer, Brewery
from beerapp.ratebeer import *

@csrf_exempt
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

@csrf_exempt
def search_view(request, search='Good People'):
    """
    Grabs user's input from homepage search bar and provides results
    
    """
    q = request.GET.get('q')
    results = brewerySearch(query=q)
    if results == None:
        results = searchBeers(query=q)
    return render(request, 'search_results.html', context={
        'results': results
    })

@csrf_exempt
def brewery_list_view(request, brewery_name='Good People'):
    """
    Brewery 'list' actions:

    Based on the request method, perform the following actions:
        * GET: Returns the `Brewery` object based on brewery_name

    Make sure you add at least these validations:
        * If the view receives another HTTP method out of the ones listed
          above, return a `400` response.

        * If submited payload is nos JSON valid, return a `400` response.
    """
    if request.method == 'GET':
        return JsonResponse(brewerySearch(brewery_name))
    else:
        brewery_form = Brewery_Form()
    
    return render(request, 'brewery_page.html', {'brewery_form': brewery_form})
    
@csrf_exempt
def beer_detail_view(request, beer_id):
    """
    Beer 'list' actions:

    Based on the request method, perform the following actions:

        * GET: Returns the `Beer` object based on beer_id

    Make sure you add at least these validations:
        * If the view receives another HTTP method out of the ones listed
          above, return a `400` response.

        * If submited payload is nos JSON valid, return a `400` response.
    """
    if request.method == 'GET':
        return JsonResponse(getBeer(beer_id))
    else:
        return JsonResponse({
            "success": False,
            "msg": "A bad request"
        }, status=400)


# @csrf_exempt
# def user_detail_view(request, user_id):
#     pass


@csrf_exempt
def test(request, test):
    if request.method == 'GET':
        return JsonResponse('test')
    else:
        return JsonResponse({"success": False,"msg": "A bad request"}, status=400)