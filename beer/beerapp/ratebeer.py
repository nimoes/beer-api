import requests
import json

from beerapp.credentials import *

from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseForbidden

headers = {}
headers["Content-Type"] = "application/json"
headers["accept"] = "application/json"
headers["x-api-key"] = api_key

SINGLE_BEER = """
      id, 
      name,
      description,
      brewer {id, name, description, type, streetAddress, city, state {name}, zip, phone, imageUrl, score, isRetired},
      contractBrewer {name, description, type, streetAddress, city, state {name}, zip, phone, imageUrl, score, isRetired},
      abv,
      ibu,
      calories,
      labels,
      seasonal,
      style {name, description, glasses{name, description} },
      styleScore,
      overallScore,
      averageRating,
      realAverage,
      ratingCount,
      imageUrl,
      availability {bottle, tap, distribution},
      purchase {store {name, url} , productId, productUrl, bottleSize, price},
      confidence
"""

BEER_LIST = """
items {
      id, 
      name,
      description,
      brewer {id, name, description, type, streetAddress, city, state {name}, zip, phone, imageUrl, score, isRetired},
      contractBrewer {name, description, type, streetAddress, city, state {name}, zip, phone, imageUrl, score, isRetired},
      abv,
      ibu,
      calories,
      labels,
      seasonal,
      style {name, description, glasses{name, description} },
      styleScore,
      overallScore,
      averageRating,
      realAverage,
      ratingCount,
      imageUrl,
      availability {bottle, tap, distribution},
      purchase {store {name, url} , productId, productUrl, bottleSize, price},
      confidence
    } 
"""
BREWERY_LIST = """
items{
      id,
      name, 
      description, 
      type, 
      streetAddress, 
      city, 
      state {name}, 
      zip, 
      phone, 
      imageUrl, 
      score, 
      isRetired
    }
"""

REVIEW_LIST = """
items{
      id,
      comment,
      score,
      scores {appearance, aroma, flavor, mouthfeel, overall},
      beer {id, name},
      createdAt,
      updatedAt
    }
"""



# getBeer
# id: ID! = ! denotes required field, takes only an ID and returns a single beer
def getBeer(ID=False):
      if not ID:
            return JsonResponse({
                  "success": False,
                  "msg": "A bad request"
            }, status=400)
      else:
            if ID > 500000: ID = 500000
            ID = str(ID)
            get_beer = 'query{beer (id: ' + ID + ') {' + SINGLE_BEER + '} }'
      r = requests.post("https://api.r8.beer/v1/api/graphql/", json={"query":get_beer,"variables":"{}"}, headers=headers)
      return r.json()



# topBeers
# first: int = total number of beers to pull (top 10 default)
# after: id = pulls the top beers following the id of a specific beer
# Two recurring calls would probably take the last beer ID as an after, 
# with first remaining the same to pull 2 pages of top beers and not show repeats
def topBeers(first=10, after=False):
      if first:
            first = str(first);
            if first > 100: first = 100
            
      if after:
            top_beers = 'query {topBeers (first: ' + first + ', after: ' + after + ') {' + BEER_LIST + '} }'
      else:
            top_beers = 'query {topBeers (first: ' + first + ') {' + BEER_LIST + '} }'
      r = requests.post("https://api.r8.beer/v1/api/graphql/", json={"query":top_beers,"variables":"{}"}, headers=headers)
      return r.json()



# searchBeers
# Takes up to 3 parameters (query, first, after)
# query: String = name of BEER to search for
# first: Int = total number of beers to pull (top 10 default)
# after: ID = pulls the top beers following the id of a specific beer
def searchBeers(query="good people", first=10, after=False):
    if first > 100: first = 100
    first = str(first)
    if after:
        after = str(after)
        beer_search = 'query {beerSearch (query: "' + query + '", first: ' + first + ', after: ' + after + ') {' + BEER_LIST + ', totalCount } }'
    else:
      beer_search = 'query {beerSearch (query: "' + query + '", first: ' + first + ') {' + BEER_LIST + ', totalCount } }'
    r = requests.post("https://api.r8.beer/v1/api/graphql/", json={"query":beer_search,"variables":"{}"}, headers=headers)
    return r.json()



# beersByBrewer
# brewerId: ID! = ! denotes required field, requires ID of brewery to get beers by brewer
# first: Int = total number of breweries to pull (top 5 default)
# after: ID = pulls the top breweries following the id of a speciifc brewery
def beersByBrewer(brewerId=False, first=5, after=False):
      if first:
            first = str(first);
            if first > 25: first = 25
      
      if not brewerId:
            return JsonResponse({
                  "success": False,
                  "msg": "A bad request"
            }, status=400)
      if after:
            after = str(after)
            beers_by_brewer = 'query {beersByBrewer (brewerId: ' + brewerId + ', first: ' + first + ', after: ' + after + ') {' + BEER_LIST + '} }'
      else:
            beers_by_brewer = 'query {beersByBrewer (brewerId: ' + brewerId + ', first: ' + first + ') {' + BEER_LIST + '} }'
      r = requests.post("https://api.r8.beer/v1/api/graphql/", json={"query":beers_by_brewer,"variables":"{}"}, headers=headers)
      return r.json()



# brewerySearch
# query: String = name of BREWERY to search for
# order: SearchOrder = MATCH, RATING_COUNT, AVERAGE_RATING, OVERALL_SCORE (not strings in the query itself, these are variables)
# first: Int = total number of breweries to pull (top 5 default)
# after: ID = pulls the top breweries following the id of a specific brewery
def brewerySearch(query, order="MATCH", first=5, after=False):
      if not query:
            return JsonResponse({
                  "success": False,
                  "msg": "A bad request"
            }, status=400)
      if first:
            if first > 100: first = 100 
            first = str(first)
      if after:
            after = str(after)
            brewery_search = 'query {brewerSearch (query: "' + query + '", order: '+ order +', first: '+ first +', after: ' + after + ') {' + BREWERY_LIST + '} }'
      else:
            brewery_search = 'query {brewerSearch (query: "' + query + '", order: '+ order +', first: '+ first +') {' + BREWERY_LIST + '} }'
      r = requests.post("https://api.r8.beer/v1/api/graphql/", json={"query":brewery_search,"variables":"{}"}, headers=headers)
      return r.json()


# beerReviews
# beerId: ID! = ! denotes requires field, requires ID of brewery to get beers by brewer
# first: Int = total number of BEERS to pull (top 10 default)
# after: ID = pulls the top breweries following the id of a speciifc brewery
def beerReviews(beerId=False, first=5, after=False):
      if not beerId:
            return None
      if first:
            first = str(first);
            if first > 25: 
                first = 25
            
      if after:
            after = str(after)
            beer_reviews = 'query {beerReviews (beerId: ' + beerId + ', first: ' + first + ', afer: ' + after + '){' + REVIEW_LIST + '} }'
      else:
            beer_reviews = 'query {beerReviews (beerId: ' + beerId + ', first: ' + first + '){' + REVIEW_LIST + '} }'
      r = requests.post("https://api.r8.beer/v1/api/graphql/", json={"query":beer_reviews,"variables":"{}"}, headers=headers)
      return r.json()
