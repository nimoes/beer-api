import requests
import json

# example response from the server about a brewery
#   {
#     id: 299,
#     name: "Almanac Beer Company",
#     brewery_type: "micro",
#     street: "651B W Tower Ave",
#     city: "Alameda",
#     state: "California",
#     postal_code: "94501-5047",
#     country: "United States",
#     longitude: "-122.306283180899",
#     latitude: "37.7834497667258",
#     phone: "4159326531",
#     website_url: "http://almanacbeer.com",
#     updated_at: "2018-08-23T23:24:11.758Z"
#   }



# searchBrewery
# Query (string)    takes any parameter and searches all the paramters
def searchBrewery(query=False):
    if not query: return None
    r = requests.get('https://api.openbrewerydb.org/breweries/search?query={}'.format(query))
    return r.json()



# searchAutoComplete
# Query (string)    takes any parameter and searches all the paramters 
def searchAutoComplete(query=False):
    if not query: return None
    r = requests.get('https://api.openbrewerydb.org/breweries/autocomplete?query={}'.format(query))
    return r.json()
      
      
# getBrewery
# ID (int)          takes ID as a parameter, returns a brewery object
def getBrewery(ID=False):
    if not ID: return None
    r = requests.get("https://api.openbrewerydb.org/breweries/" + str(ID))
    return r.json()



# getBreweriesByState
# State (string)    takes a state as a parameter, looks like the full state name
def getBreweriesByState(state=False):
    if not state: return None
    r = requests.get('https://api.openbrewerydb.org/breweries?by_state={}&sort=type,-name'.format(state))
    return r.json()



# getBreweryByName
# Name (string)     takes name as a paramter, returns matching breweries
# Page (int)        takes an integer as a parameter, default to 1
# Per_Page (int)    takes an integer as a parameter, default to 20
def getBreweryByName(name, page=1, per_page=20):
    if not name: return None
    name=str(name); page=str(page); per_page=str(per_page)
    r = requests.get('https://api.openbrewerydb.org/breweries?by_name={}&page={}&per_page={}'.format(name, page, per_page));
    return r.json()