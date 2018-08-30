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
      
      
      
# getBrewery
# ID (int)          takes ID as a parameter, returns a brewery object
def getBrewery(ID=False):
    if not ID: return None
    r = requests.get("https://api.openbrewerydb.org/breweries/" + str(ID))
    return r.json()
    
    

# getBreweryByName
# Name (string)     takes name as a paramter, returns matching breweries
# Page (int)        takes an integer as a parameter, default to 1
# Per_Page (int)    takes an integer as a parameter, default to 20