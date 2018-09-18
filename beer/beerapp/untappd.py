import requests
import json

from beerapp.credentials import *

auth_token = '&client_id={}&client_secret={}'.format(client_id, client_secret)
auth_token_q = '?client_id={}&client_secret={}'.format(client_id, client_secret)

# auth_token must be inserted at the end of any query string. API does not accept headers, requires both client_id and client_secret to function
# Example responses stored at bottom of code because they're huge



def getTapBeer(BID=False):
      if not BID: return None
      r = requests.get('https://api.untappd.com/v4/beer/info/{}{}'.format(str(BID), auth_token_q))
      return r.json()

def searchTapBeer(breweryName=False, beerName=False):
      if not beerName: return None;
      
      if breweryName and beerName: query = str(breweryName) + " " + str(beerName)
      else: query = beerName;
      
      r = requests.get('https://api.untappd.com/v4/search/beer?q={}{}'.format(query, auth_token))
      return r.json()

def searchTapBeerOnly(beerName=False):
      if not beerName: return None;
      query = str(beerName)
      r = requests.get('https://api.untappd.com/v4/search/beer?q={}{}'.format(query, auth_token))
      return r.json()





















# https://api.untappd.com/v4/search/brewery?q=Good+People
# {
#     "meta": {
#         "code": 200,
#         "response_time": {
#             "time": 0.127,
#             "measure": "seconds"
#         },
#         "init_time": {
#             "time": 0,
#             "measure": "seconds"
#         }
#     },
#     "notifications": [],
#     "response": {
#         "engine": "_algolia",
#         "page": 0,
#         "search_type": "wildcard",
#         "sort": "",
#         "term": "Good People",
#         "key": "Good People",
#         "found": 1,
#         "brewery": {
#             "count": 1,
#             "items": [
#                 {
#                     "brewery": {
#                         "brewery_id": 2811,
#                         "beer_count": 147,
#                         "brewery_name": "Good People Brewing Company",
#                         "brewery_slug": "good-people-brewing-company",
#                         "brewery_page_url": "/GPBrewing",
#                         "brewery_label": "https://untappd.akamaized.net/site/brewery_logos/brewery-2811_b7617.jpeg",
#                         "country_name": "United States",
#                         "location": {
#                             "brewery_city": "Birmingham",
#                             "brewery_state": "AL",
#                             "lat": 33.507,
#                             "lng": -86.8121
#                         }
#                     }
#                 }
#             ]
#         }
#     }
# }

# https://api.untappd.com/v4/beer/info/BID=16630
# {
#   "beer": {
#     "bid": 16630,
#     "beer_name": "Celebration Ale",
#     "beer_label": "https://d1c8v1qci5en44.cloudfront.net/site/beer_logos/beer-_16630_sm_96f50e03ae848a4a368a787b38f989.jpeg",
#     "beer_abv": 6.8,
#     "beer_ibu": 65,
#     "beer_description": "The long, cold nights of winter are a little brighter with Celebration Ale. Wonderfully robust and rich, Celebration Ale is dry-hopped for a lively, intense aroma. Brewed especially for the holidays, it is perfect for a festive gathering or for a quiet evening at home.",
#     "beer_style": "American IPA",
#     "is_in_production": 1,
#     "beer_slug": "sierra-nevada-brewing-co-celebration-ale",
#     "is_homebrew": 0,
#     "created_at": "Fri, 24 Dec 2010 10:10:42 +0000",
#     "rating_count": 35148,
#     "rating_score": 3.78495,
#     "stats": {
#       "total_count": 57453,
#       "monthly_count": 24387,
#       "total_user_count": 39594,
#       "user_count": 0
#     },
#     "brewery": {
#       "brewery_id": 1142,
#       "brewery_name": "Sierra Nevada Brewing Co.",
#       "brewery_label": "https://d1c8v1qci5en44.cloudfront.net/site/brewery_logos/brewery-1142_f241d.jpeg",
#       "country_name": "United States",
#       "contact": {
#         "twitter": "SierraNevada",
#         "facebook": "http://www.facebook.com/sierranevadabeer",
#         "url": "http://www.sierranevada.com/"
#       },
#       "location": {
#         "brewery_city": "Chico",
#         "brewery_state": "CA",
#         "lat": 39.7246,
#         "lng": -121.816
#       }
#     },
#     "auth_rating": 0,
#     "wish_list": false,
#     "media": {
#       "count": 1,
#       "items": {
#         "photo_id": 25856365,
#         "photo": {
#           "photo_img_sm": "https://d1c8v1qci5en44.cloudfront.net/photo/2014_12_14/b73895e69761fdb62a4a9e10294e9613_100x100.jpg",
#           "photo_img_md": "https://d1c8v1qci5en44.cloudfront.net/photo/2014_12_14/b73895e69761fdb62a4a9e10294e9613_320x320.jpg",
#           "photo_img_lg": "https://d1c8v1qci5en44.cloudfront.net/photo/2014_12_14/b73895e69761fdb62a4a9e10294e9613_640x640.jpg",
#           "photo_img_og": "https://d1c8v1qci5en44.cloudfront.net/photo/2014_12_14/b73895e69761fdb62a4a9e10294e9613_raw.jpg"
#         },
#         "created_at": "Sun, 14 Dec 2014 22:39:26 +0000",
#         "checkin_id": 137623689,
#         "beer": {
#           "bid": 16630,
#           "beer_name": "Celebration Ale",
#           "beer_label": "https://d1c8v1qci5en44.cloudfront.net/site/beer_logos/beer-_16630_sm_96f50e03ae848a4a368a787b38f989.jpeg",
#           "beer_abv": 6.8,
#           "beer_ibu": 65,
#           "beer_slug": "sierra-nevada-brewing-co-celebration-ale",
#           "beer_description": "The long, cold nights of winter are a little brighter with Celebration Ale. Wonderfully robust and rich, Celebration Ale is dry-hopped for a lively, intense aroma. Brewed especially for the holidays, it is perfect for a festive gathering or for a quiet evening at home.",
#           "is_in_production": 1,
#           "beer_style_id": 128,
#           "beer_style": "American IPA",
#           "auth_rating": 0,
#           "wish_list": false,
#           "beer_active": 1
#         },
#         "brewery": {
#           "brewery_id": 1142,
#           "brewery_name": "Sierra Nevada Brewing Co.",
#           "brewery_slug": "sierra-nevada-brewing-co",
#           "brewery_label": "https://d1c8v1qci5en44.cloudfront.net/site/brewery_logos/brewery-1142_f241d.jpeg",
#           "country_name": "United States",
#           "contact": {
#             "twitter": "SierraNevada",
#             "facebook": "http://www.facebook.com/sierranevadabeer",
#             "url": "http://www.sierranevada.com/"
#           },
#           "location": {
#             "brewery_city": "Chico",
#             "brewery_state": "CA",
#             "lat": 39.7246,
#             "lng": -121.816
#           },
#           "brewery_active": 1
#         },
#         "user": {
#           "uid": 1068060,
#           "user_name": "Sallyddrake",
#           "first_name": "Sally",
#           "last_name": "D",
#           "user_avatar": "https://gravatar.com/avatar/51d0f47cf4633afac7dda8990a67ab1b?size=100&d=htt…44.cloudfront.net%2Fsite%2Fassets%2Fimages%2Fdefault_avatar_v2.jpg%3Fv%3D1",
#           "relationship": "none",
#           "is_private": 0
#         },
#         "venue": [
#           {
#             "venue_id": 1922107,
#             "venue_name": "Lucky's Market",
#             "primary_category": "Shop & Service",
#             "parent_category_id": "4d4b7105d754a06378d81259",
#             "categories": {
#               "count": 1,
#               "items": [
#                 {
#                   "category_name": "Grocery or Supermarket",
#                   "category_id": "4bf58dd8d48988d118951735",
#                   "is_primary": true
#                 }
#               ]
#             },
#             "location": {
#               "venue_address": "Fountain Plaza",
#               "venue_city": "Ellisville",
#               "venue_state": "MO",
#               "lat": 38.6058,
#               "lng": -90.5834
#             },
#             "contact": {
#               "twitter": "",
#               "venue_url": ""
#             },
#             "private_venue": true,
#             "foursquare": {
#               "foursquare_id": "53d80e2b498eb7cff03ec47a",
#               "foursquare_url": "http://4sq.com/1rCS43U"
#             },
#             "venue_icon": {
#               "sm": "https://ss3.4sqi.net/img/categories_v2/shops/food_grocery_bg_64.png",
#               "md": "https://ss3.4sqi.net/img/categories_v2/shops/food_grocery_bg_88.png",
#               "lg": "https://ss3.4sqi.net/img/categories_v2/shops/food_grocery_bg_88.png"
#             }
#           }
#         ]
#       }
#     },
#     "similar": {
#       "count": 1,
#       "items": {
#         "rating_score": 4.16096,
#         "beer": {
#           "bid": 881386,
#           "beer_name": "Stone Enjoy By 12.26.14 IPA",
#           "beer_abv": 9.4,
#           "beer_ibu": 88,
#           "beer_style": "Imperial / Double IPA",
#           "beer_label": "https://d1c8v1qci5en44.cloudfront.net/site/beer_logos/beer-881386_1a85e_sm.jpeg",
#           "auth_rating": 0,
#           "wish_list": false
#         },
#         "brewery": {
#           "brewery_id": 1204,
#           "brewery_name": "Stone Brewing Co.",
#           "brewery_slug": "stone-brewing-co",
#           "brewery_label": "https://d1c8v1qci5en44.cloudfront.net/site/brewery_logos/brewery-stone.jpg",
#           "country_name": "United States",
#           "contact": {
#             "twitter": "StoneBrewingCo",
#             "facebook": "http://www.facebook.com/StoneBrewingCo",
#             "instagram": "StoneBrewingCo",
#             "url": "http://www.stonebrew.com/"
#           },
#           "location": {
#             "brewery_city": "Escondido",
#             "brewery_state": "CA",
#             "lat": 33.1157,
#             "lng": -117.12
#           },
#           "brewery_active": 1
#         },
#         "friends": {
#           "items": [],
#           "count": 0
#         }
#       }
#     },
#     "friends": {
#       "count": 0,
#       "items": []
#     },
#     "vintages": {
#       "count": 5,
#       "items": [
#         {
#           "beer": {
#             "bid": 6796,
#             "beer_label": "https://d1c8v1qci5en44.cloudfront.net/site/beer_logos/beer-_6796_sm_7a8d7db0099654386f616e26ccb043.jpeg",
#             "beer_slug": "sierra-nevada-brewing-co-celebration-ale-2010",
#             "beer_name": "Celebration Ale (2010)",
#             "is_vintage": 1,
#             "is_variant": 0
#           }
#         },
#         {
#           "beer": {
#             "bid": 10611,
#             "beer_label": "https://d1c8v1qci5en44.cloudfront.net/site/beer_logos/beer-_10611_sm_f9e846389a5b26bb4888557aa78a29.jpeg",
#             "beer_slug": "sierra-nevada-brewing-co-celebration-ale-2007",
#             "beer_name": "Celebration Ale (2007)",
#             "is_vintage": 1,
#             "is_variant": 0
#           }
#         },
#         {
#           "beer": {
#             "bid": 12371,
#             "beer_label": "https://d1c8v1qci5en44.cloudfront.net/site/beer_logos/beer-_12371_sm_389b71c2126a12d3e538ba9d0ef82e.jpeg",
#             "beer_slug": "sierra-nevada-brewing-co-celebration-ale-2009",
#             "beer_name": "Celebration Ale (2009)",
#             "is_vintage": 1,
#             "is_variant": 0
#           }
#         },
#         {
#           "beer": {
#             "bid": 15030,
#             "beer_label": "https://d1c8v1qci5en44.cloudfront.net/site/beer_logos/beer-_16630_sm_96f50e03ae848a4a368a787b38f989.jpeg",
#             "beer_slug": "sierra-nevada-brewing-co-celebration-ale-1997",
#             "beer_name": "Celebration Ale (1997)",
#             "is_vintage": 1,
#             "is_variant": 0
#           }
#         },
#         {
#           "beer": {
#             "bid": 19893,
#             "beer_label": "https://d1c8v1qci5en44.cloudfront.net/site/beer_logos/beer-_16630_sm_96f50e03ae848a4a368a787b38f989.jpeg",
#             "beer_slug": "sierra-nevada-brewing-co-celebration-ale-2006",
#             "beer_name": "Celebration Ale (2006)",
#             "is_vintage": 1,
#             "is_variant": 0
#           }
#         }
#       ]
#     }
#   }
# }