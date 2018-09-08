import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseForbidden
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required

from beerapp.models import Beer, Brewery
from beerapp.ratebeer import *


@csrf_exempt
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


@csrf_exempt
def search_view(request, search='Good People'):
    """
    This function grabs user's input from homepage search bar and provides 
    results.
    Input name, `search_type`, is used to determine whether the users
    want to tailor their search to 1) beer or 2) brewery. 
    Input name, `q`, is used to grab users' input and perform 
    an appropriate function which then sends an API request to grab the
    results.
    Results will be rendered to `/search_results` where users can further
    interact with the website
    
    """
    q = request.GET.get('q')
    search_type = request.GET.get('search_type')
    
    if search_type == 'beer':
        results = searchBeers(query=q)
    elif search_type == 'brewery':
        results = brewerySearch(query=q)
    else:
        results = topBeers(10)

    return render(request, 'search_results.html', context={
        'results': results,
        'search_type': search_type
    })


@csrf_exempt
def brewery_list_view(request, brewery_name='Good People'):
    """

    """
    if request.method == 'GET':
        return JsonResponse(brewerySearch(brewery_name))
    else:
        brewery_form = Brewery_Form()
    
    return render(request, 'brewery_page.html', {'brewery_form': brewery_form})
    
@csrf_exempt
def beer_detail_view(request, beer_id):
    """

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