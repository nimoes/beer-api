import json
from jsonmerge import merge
import re

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.views.generic.base import RedirectView

# for user signup
from beerapp.forms import CustomUserCreationForm, LikeForm, LikeBeerForm
from django.urls import reverse_lazy
from django.views import generic

# for api
from beerapp.credentials import map_api

# for likes
from beerapp.models import *

from beerapp.ratebeer import *
from beerapp.openbrewery import *
from beerapp.untappd import *

from django.utils.timezone import now

@csrf_exempt
def index(request):
    template = loader.get_template('index.html')
    return render(request, 'index.html')


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    

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
    
    if request.method == 'GET':
        print("this is a get request")
        q = request.GET.get('q')
        search_type = request.GET.get('search_type')
        try: 
            page = request.GET.get('p')
        except:
            page = ""
        
        if search_type == 'beer':
            if page:
                numAfter = int(page) * 10
                results = searchBeers(query=q, first=10, after=numAfter)
                pass
            else:
                results = searchBeers(query=q)
            # print(results)
        elif search_type == 'brewery':
            if page:
                numAfter = int(page) * 5
                results = brewerySearch(query=q, first=5, after=numAfter)
            else:
                results = brewerySearch(query=q)
            # print(results)
        else:
            results = topBeers(10)
    
        return render(request, 'search_results.html', context={
            'results': results,
            'search_type': search_type, 
        })


'''
This function allows users to add their favorite breweries and beers
to their respective profiles.
'''
@login_required
def adds_to_favorites(request):
    
    if request.method == 'POST':
        print('POST - ' + str(request.POST))
        
        likes = ""
        beer_likes = ""
        
        if 'brewid' in request.POST:
            like_form = LikeForm(request.POST)
            print(like_form)
            if (request.user is not None) and like_form.is_valid():
                print("\nCreating instance of like for user\n\nAdding brewery to your favorites...")
                instance = Like(
                    name=like_form.cleaned_data['name'], 
                    brewid=like_form.cleaned_data['brewid'], 
                    imageUrl=like_form.cleaned_data['imageUrl'], 
                    username=request.user
                    )
                # if the name of the brewery does not exist in list of Like objects
                if Like.objects.filter(name=like_form.cleaned_data['name']).count() == 0:
                    # assign and save instance
                    likes = Like.objects.filter(username=request.user)
                    print("\nSaving instance of like")
                    instance.save()
                else:
                    print("\nThis brewery already exists in your profile.")
                    
        elif 'beerid' in request.POST:
            beer_form = LikeBeerForm(request.POST)
            print(beer_form)
            if (request.user is not None) and beer_form.is_valid():
                print("\nCreating instance of like for user\n\nAdding beer to your favorites...")
                instance = LikeBeer(
                    beername = beer_form.cleaned_data['beername'], 
                    beerid = beer_form.cleaned_data['beerid'], 
                    beerimg = beer_form.cleaned_data['beerimg'],
                    username = request.user
                    )
                
                # if the name of the beer does not exist in list of Like objects
                if LikeBeer.objects.filter(beername=beer_form.cleaned_data['beername']).count() == 0:
                    # assign and save instance
                    beer_likes = LikeBeer.objects.filter(username=request.user)
                    print("\nSaving instance of like")
                    instance.save()
                else:
                    print("\nThis beer already exists in your profile.")

        return HttpResponseRedirect('/my_profile/')
    
    if request.method == 'GET':
        try:
            beer_likes = LikeBeer.objects.filter(username=request.user)
            likes = Like.objects.filter(username=request.user)

        except Exception as e:
            print(str(e))
            
        print("retrieving favorites for the user")
        # for like in likes:
        #     print(like.imageUrl)
        # for beerlike in beer_likes:
        #     print(beerlike.beerimg)

        return render(request, 'profile.html', context={
            'likes': likes,
            'beer_likes': beer_likes
        })


'''
This function is invoked when a user wants to remove his/her favorite beer or
brewery from his/her list of favorites. Only POST request is accepted.
'''
@login_required
def remove_item(request):
    if request.method == 'POST':
        beer_name = request.POST.get('beer_name')
        brewery_name = request.POST.get('brewery_name')
        if brewery_name:
            try:
                print(request.POST)
                print(brewery_name)
                brewery = Like.objects.filter(name=brewery_name)
            except Exception as e:
                print(str(e))
                return HttpResponseNotFound('\nthis brewery does not exist')
            brewery.delete()
            messages.success(request, 'Item has been successfully removed from your favorites.')
            return HttpResponseRedirect('/my_profile')
            
        elif beer_name:
            try:
                beer = LikeBeer.objects.filter(beername=beer_name)
            except Exception as e:
                return HttpResponseNotFound('\nthis beer does not exist')
            beer.delete()
            messages.success(request, 'Item has been successfully removed from your favorites.')
            return HttpResponseRedirect('/my_profile')
    else:
        return HttpResponse('invalid HTTP method')

@csrf_exempt
def brewery_list_view(request, brewery_name='Good People'):
    """

    """
    if request.method == 'GET':
        results =  brewerySearch(brewery_name)
    else:
        brewery_form = Brewery_Form()
    
    return render(request, 'brewery_details_view.html', context={
        'results': results
    })
    
@csrf_exempt
def beer_detail_view(request, beer_id=1):
    """

    """
    beer_id = request.GET.get('id')
    if request.method == 'GET':
        results = getBeer(beer_id)
        # print(results)
        if (results['data']['beer']['brewer']['name'] != "") and (results['data']['beer']['name'] != ""):
            rateBeer = results['data']['beer']
            untappd = searchTapBeer(rateBeer['brewer']['name'], rateBeer['name'])
            if untappd['response']:
                # print(untappd['response'])
                # print(len(untappd['response']['beers']['items']))
                
                # if the search is too restrictive with brewer and beer
                if len(untappd['response']['beers']['items']) < 1:
                    untappd = searchTapBeerOnly(rateBeer['name'])
                    match = ""
                
                for untappdBeer in untappd['response']['beers']['items']:
                    print("untappdBrewery " + str(untappdBeer['brewery']['brewery_name']))
                    print("untappdBeer " + str(untappdBeer['beer']['beer_name']))
                    # print("untappdState " + str(untappdBeer['brewery']['location']['brewery_state']))
                    print("untappdStyle " + str(untappdBeer['beer']['beer_style']))
                    print("untappdABV " + str(untappdBeer['beer']['beer_abv']))
                    
                    print("rbBrewery " + str(rateBeer['brewer']['name']))
                    print("rbBeer " + str(rateBeer['name']))
                    # print("rbState " + str(rateBeer['brewer']['state']['name']))
                    print("rbStyle " + str(rateBeer['style']['name']))
                    print("rbABV " + str(rateBeer['abv']))
                    
                    uBrewery = untappdBeer['brewery']['brewery_name']
                    uBeer = untappdBeer['beer']['beer_name']
                    uState = untappdBeer['brewery']['location']['brewery_state']
                    uStyle = untappdBeer['beer']['beer_style']
                    uABV = untappdBeer['beer']['beer_abv']
                    
                    rbBrewery = rateBeer['brewer']['name']
                    rbBeer = rateBeer['name']
                    if rateBeer['brewer']['state'] is not None:
                        rbState = rateBeer['brewer']['state']['name']
                    else:
                        rbState = ""
                    rbStyle = rateBeer['style']['name']
                    rbABV = rateBeer['abv']
                    
                    # Logic beer match
                    count = 0
                    total = 0
                    if (rbState and uState):
                        total+=1
                        # Meshing types
                        if len(uState) <= 2: uState = us_state_abbrev.get(uState, None)
                        
                        # Match check
                        if (rbState == uState): count+=1
                        
                    if (rbBrewery and uBrewery):
                        total+=1
                        # Meshing types
                        if "Company" in rbBrewery: rbBrewery.replace("Company", "Co")
                        if "Company" in uBrewery: rbBrewery.replace("Company", "Co")
                        
                        # Match check
                        if (rbBrewery in uBrewery or uBrewery in rbBrewery): count+=1
                        
                    if (rbBeer and uBeer):
                        total+=1
                        # Meshing types
            
                        # Match check
                        if (rbBeer in uBeer or uBeer in rbBeer): count+=1
                        
                    if (uStyle and rbStyle):
                        total+=1
                        # Meshing types
                        rbStyle = re.sub('[^A-Za-z0-9]+', '', rbStyle)
                        uStyle = re.sub('[^A-Za-z0-9]+', '', uStyle)
                        
                        # Match check
                        if (rbStyle in uStyle or uStyle in rbStyle): count+=1
                        
                    if (rbABV and uABV):
                        total+=1
                        # Meshing Types
                        rbABV = '%.2f' % rbABV
                        uABV = '%.2f' % uABV
                        
                        #Match check
                        if abs(float(rbABV) - float(uABV)) <= 1.1: count+=1
                    
                    # Count up matches, divide by total
                    percent = count/total
                    if (percent) == 1: 
                        # all matching criteria
                        print ('definitely a match: ' + str(percent))
                        match = untappdBeer
                        break
                    elif (percent) >= 0.75:
                        # probably good enough
                        print ('most likely a match: ' + str(percent))
                        match = untappdBeer
                        break
                    elif (percent) >= 0.6:
                        # let it go again and see if it finds a better match
                        print ('probably a match: ' + str(percent))
                        match = untappdBeer
                    elif (percent) >= 0.5:
                        # probably not a match, but possible if total=2
                        print ('low confidence match: ' + str(percent))
                        match = untappdBeer
                    else:
                        print ('not a match' + str(percent))
            else:
                match = ""
    else:
        return JsonResponse({
            "success": False,
            "msg": "A bad request"
        }, status=400)
    
        
    if match:
        print (results)
        return render(request, 'beer_details_view.html', context={
            'results': results,
            'match': match,
            'google_api': map_api
            
        })
    else:
        return render(request, 'beer_details_view.html', context={
            'results': results,
            'google_api': map_api
        })
    
@csrf_exempt
def brewery_detail_view(request, brewery_id=1):
    """
    
    """
    brewery_id = request.GET.get('id')
    brewery_name = request.GET.get('name')
    if request.method == 'GET':
        
        match = False
        if  brewery_name and brewery_id: 
            results = merge(brewerySearch(str(brewery_name)) , beersByBrewer(int(brewery_id)) )
            # results = ""
        elif brewery_name and not brewery_id:
            results =  brewerySearch(str(brewery_name))
        else:
            results =  beersByBrewer(int(brewery_id))
            
        if  brewery_name:
            brewery_details = searchBrewery(brewery_name)
            for l in brewery_details:
                # Logic match step
                if (l['name'] in results['data']['brewerSearch']['items'][0]['name']) or (results['data']['brewerSearch']['items'][0]['name'] in l['name']):
                    match = l
                else:
                    match = False
        
    else:
        return JsonResponse({
            "success": False,
            "msg": "A bad request"
        }, status=400)

    if match == False:
        print ("returning just results")
        return render(request, 'brewery_details_view.html', context={
            'results': results,
            'google_api': map_api,
        })
    else:
        print ("returning results and brewery_details")
        return render(request, 'brewery_details_view.html', context={
            'results': results,
            'match': match,
            'google_api': map_api,
        })

us_state_abbrev = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
    'PR': 'Puerto Rico'
}

beerSearchResponse = """
{
  "data": {
    "beerSearch": {
      "items": [
        {
          "id": "92158",
          "name": "Good People IPA",
          "description": "Copper in color with herbal and earthy hops being most prevalent. Light caramel flavors balance out this unique ale. Hop lovers will enjoy this unfiltered, dry-hopped IPA.",
          "brewer": {
            "id": "9621",
            "name": "Good People Brewing Company",
            "description": "",
            "type": "Microbrewery",
            "streetAddress": "1035 20th St S, Ste B",
            "city": "Birmingham",
            "state": {
              "name": "Alabama"
            },
            "zip": "35205",
            "phone": "588 - 8002",
            "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_150,c_limit,d_brewerdefault_hk6nu1.png,f_auto/brew_9621.jpg",
            "score": 118759,
            "isRetired": false
          },
          "contractBrewer": null,
          "abv": 6,
          "ibu": 64,
          "calories": 180,
          "labels": [],
          "seasonal": "UNKNOWN",
          "style": {
            "name": "IPA",
            "description": "India Pale Ale, the modern version of which has largely been formed in the US, has an intense hop flavor, a golden to copper color, and a medium malty body. The aroma is moderate to very strong. IPAs work especially well at cutting the heat of chili, vindaloo or Sichuan cuisine.  In England, IPA is often just another name for bitter although some micros are doing their own versions of an American IPA as well.",
            "glasses": [
              {
                "name": "Shaker",
                "description": "The American microbrewer’s standard. A gently sloped 16 oz. glass made for session-type beers. Ambers, English & American pales, and sometimes darker session ales are typically served in these glasses, which are better known for their durability, than for any particularly beneficial properties. It is for that reason that some beer geeks have developed a hatred of the shaker."
              },
              {
                "name": "Tulip",
                "description": "The most varied glass in the world of beer. This style of glass has been around a while but only recently has found in a home in the eyes of beer-lovers the world over. It is the ultimate beer-tasting utility glass. The bulbous bottom makes for great drinking, the flared mouth allows for wonderful head formation and aroma release, and while it is short enough to handle the biggest beer styles, it is tall enough to service IPAs and other complex session beers. The Duvel glass is a well-known variant of the tulip style, and the Ratebeer tasting glass is an almost perfect example."
              }
            ]
          },
          "styleScore": 60.762874117113576,
          "overallScore": 79.80014457959733,
          "averageRating": 3.424186944961548,
          "realAverage": null,
          "ratingCount": 179,
          "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_120,c_limit,d_beer_icon_default.png,f_auto/beer_92158.jpg",
          "availability": {
            "bottle": "unknown",
            "tap": "unknown",
            "distribution": "regional"
          },
          "purchase": null,
          "confidence": null
        },
        {
          "id": "89046",
          "name": "Good People American Brown Ale",
          "description": "This deep colored American Brown Ale is often requested and one of our personal favorites.  Many a weekend was spent perfecting this one.  Brewed with 2 - row pale and 5 specialty malts, its malty in both flavor and smell.  A heap of Cascade and Willamette add to balance this easy drinking ale.  Hole up, have a few, and tell us what you think.  We’re bettings it’s the best American Brown Ale you’ll ever have.",
          "brewer": {
            "id": "9621",
            "name": "Good People Brewing Company",
            "description": "",
            "type": "Microbrewery",
            "streetAddress": "1035 20th St S, Ste B",
            "city": "Birmingham",
            "state": {
              "name": "Alabama"
            },
            "zip": "35205",
            "phone": "588 - 8002",
            "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_150,c_limit,d_brewerdefault_hk6nu1.png,f_auto/brew_9621.jpg",
            "score": 118759,
            "isRetired": false
          },
          "contractBrewer": null,
          "abv": 5.800000190734863,
          "ibu": 36,
          "calories": 174,
          "labels": [],
          "seasonal": "UNKNOWN",
          "style": {
            "name": "Brown Ale",
            "description": "Color ranges from reddish-brown to dark brown. Beers termed brown ale include sweet low alcohol beers such as Manns Original Brown Ale medium strength amber beers of moderate bitterness such as Newcastle Brown Ale and malty but hoppy beers such as Sierra Nevada Brown Ale.",
            "glasses": [
              {
                "name": "Dimpled mug",
                "description": "A classic in North America, the dimpled mug is a large mug, with dimples, and a handle. It is convex, with the mouth larger than the base. The glass is thick, so bar owners love it. While the dimples make appreciating the appearance of the beer more difficult, the wide mouth releases the aroma just nicely. So while these mugs are most commonly used for raunchy lagers, I would recommend them more for aromatic brown ales (especially the hazy ones), bocks and other dark lagers."
              },
              {
                "name": "Shaker",
                "description": "The American microbrewer’s standard. A gently sloped 16 oz. glass made for session-type beers. Ambers, English & American pales, and sometimes darker session ales are typically served in these glasses, which are better known for their durability, than for any particularly beneficial properties. It is for that reason that some beer geeks have developed a hatred of the shaker."
              }
            ]
          },
          "styleScore": 61.188633081910595,
          "overallScore": 51.02976088700743,
          "averageRating": 3.223119020462036,
          "realAverage": null,
          "ratingCount": 146,
          "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_120,c_limit,d_beer_icon_default.png,f_auto/beer_89046.jpg",
          "availability": {
            "bottle": "available",
            "tap": "unknown",
            "distribution": "local"
          },
          "purchase": null,
          "confidence": null
        },
        {
          "id": "95959",
          "name": "Good People Coffee Oatmeal Stout",
          "description": "Big coffee flavors dominate early only to be wiped out by an enormous about of Willamette hop flavors. One of GPBC’s most requested beers. Complex and full of flavor yet amazingly sessionable. Brewed with coffee from Primavera Coffee Roasters here in Birmingham, AL.",
          "brewer": {
            "id": "9621",
            "name": "Good People Brewing Company",
            "description": "",
            "type": "Microbrewery",
            "streetAddress": "1035 20th St S, Ste B",
            "city": "Birmingham",
            "state": {
              "name": "Alabama"
            },
            "zip": "35205",
            "phone": "588 - 8002",
            "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_150,c_limit,d_brewerdefault_hk6nu1.png,f_auto/brew_9621.jpg",
            "score": 118759,
            "isRetired": false
          },
          "contractBrewer": null,
          "abv": 6,
          "ibu": 54,
          "calories": 180,
          "labels": [],
          "seasonal": "UNKNOWN",
          "style": {
            "name": "Stout - Sweet",
            "description": "Dark brown to black in colour. Sweet stouts come in two main varieties - milk stout and oatmeal stout. Milk stouts are made with the addition of lactose, and are sweet and generally low in alcohol. Oatmeal lends a smooth fullness of body to stouts. All of the sweet stouts are noted for their restrained roastiness in comparison with other stouts, and their low hop levels.",
            "glasses": [
              {
                "name": "English pint",
                "description": "These have a similar purpose to the shaker in that they are made for session ales, in this case bitters, milds, porters and stouts. There are a couple of key differences. First, they pour a proper pint (and usually have a line indicating where that is on the glass, just to make sure you don’t get ripped off). Second, they have a bit more flourish than the bland shaker. There are basically two variations. The first has a gentle curve covering the upper 2/3 of the glass - Guinness uses these. The second has a straight slope for the bottom two-thirds, and then a bump near the top, flattening out at the mouth of the glass."
              },
              {
                "name": "Shaker",
                "description": "The American microbrewer’s standard. A gently sloped 16 oz. glass made for session-type beers. Ambers, English & American pales, and sometimes darker session ales are typically served in these glasses, which are better known for their durability, than for any particularly beneficial properties. It is for that reason that some beer geeks have developed a hatred of the shaker."
              }
            ]
          },
          "styleScore": 88.05583865627241,
          "overallScore": 91.13980915403856,
          "averageRating": 3.566673994064331,
          "realAverage": null,
          "ratingCount": 123,
          "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_120,c_limit,d_beer_icon_default.png,f_auto/beer_95959.jpg",
          "availability": {
            "bottle": "unknown",
            "tap": "unknown",
            "distribution": "local"
          },
          "purchase": null,
          "confidence": null
        },
        {
          "id": "105873",
          "name": "Good People Snake Handler",
          "description": "A big, joyous celebration of all things hoppy (5 different varities). Large flavors and aroma of pine, citrus, flowers, spice, pineapple, and grassiness complimented with a touch of biscuit and caramel backbone. Our most requested beer.",
          "brewer": {
            "id": "9621",
            "name": "Good People Brewing Company",
            "description": "",
            "type": "Microbrewery",
            "streetAddress": "1035 20th St S, Ste B",
            "city": "Birmingham",
            "state": {
              "name": "Alabama"
            },
            "zip": "35205",
            "phone": "588 - 8002",
            "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_150,c_limit,d_brewerdefault_hk6nu1.png,f_auto/brew_9621.jpg",
            "score": 118759,
            "isRetired": false
          },
          "contractBrewer": null,
          "abv": 9.300000190734863,
          "ibu": 103,
          "calories": 279,
          "labels": [],
          "seasonal": "UNKNOWN",
          "style": {
            "name": "IPA - Imperial / Double",
            "description": "Imperial IPA %28also called Double or Triple IPA%29 is a strong%2C often sweet%2C intensely hoppy version of the traditional India Pale Ale. Bitterness units range tend to be 100 IBUs and above. The ABV level for DIPAs generally begins at 7.5%25 but is more commonly in the 8.0%25+ range.  The flavour profile is intense all around.  Unlike barley wines%2C the balance is heavily towards the hops%2C with crystal and other malts providing support.",
            "glasses": [
              {
                "name": "Shaker",
                "description": "The American microbrewer’s standard. A gently sloped 16 oz. glass made for session-type beers. Ambers, English & American pales, and sometimes darker session ales are typically served in these glasses, which are better known for their durability, than for any particularly beneficial properties. It is for that reason that some beer geeks have developed a hatred of the shaker."
              },
              {
                "name": "Snifter",
                "description": "Whether a pure brandy snifter or a variant, these are used most commonly for barley wines, eisbocks and imperial stouts. They are stemmed and footed, bulbous at the bottom and narrowing all the way to the top. Because barley wines often have little head formation, the narrow mouth is fine as far as that goes, but still inhibits aroma a little bit, the tradeoff being the appearance of elegance. Many snifter variants made for beers have wider-than-average mouths for this reason."
              }
            ]
          },
          "styleScore": 84.62846069474301,
          "overallScore": 96.0206867534079,
          "averageRating": 3.688452959060669,
          "realAverage": null,
          "ratingCount": 117,
          "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_120,c_limit,d_beer_icon_default.png,f_auto/beer_105873.jpg",
          "availability": {
            "bottle": "available",
            "tap": "unknown",
            "distribution": "regional"
          },
          "purchase": null,
          "confidence": null
        },
        {
          "id": "89047",
          "name": "Good People Pale Ale",
          "description": "This classic American Pale Ale is is floral to the nose and flavorful to the mouth.  2 - row, 5 specialty malts, and just the slap right amount of Cascade hops makes our pale ale just a shade short of perfect.  Grab some and tell us what you think.  Surely to be one of your new favorites.",
          "brewer": {
            "id": "9621",
            "name": "Good People Brewing Company",
            "description": "",
            "type": "Microbrewery",
            "streetAddress": "1035 20th St S, Ste B",
            "city": "Birmingham",
            "state": {
              "name": "Alabama"
            },
            "zip": "35205",
            "phone": "588 - 8002",
            "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_150,c_limit,d_brewerdefault_hk6nu1.png,f_auto/brew_9621.jpg",
            "score": 118759,
            "isRetired": false
          },
          "contractBrewer": null,
          "abv": 5.599999904632568,
          "ibu": 36,
          "calories": 168,
          "labels": [],
          "seasonal": "UNKNOWN",
          "style": {
            "name": "Pale Ale - American",
            "description": "American Pale Ales are light in color, ranging from golden to a light copper color. The style of this beer is typically defined by a balance between pale malts and hop presence - although without the hop intensity or alcohol strength of an IPA. American Pale Ales generally range in strength from c. 4.5% to 6.5% &#40although there are examples outside of this range&#41.\r\n\r\nThis is a perfect beer for big fare like grilled burgers or combination pizzas, as well as lighter fare like sushi and green salads.",
            "glasses": [
              {
                "name": "Lager glass",
                "description": "Short glasses, holding no more than 12 oz of beer. They are slightly wider at the mouth than at the foot, with gradual, evenly sloping sides. This unpretentious glass is a great basic drinking vessel, well-suited to pale lagers such as American standards, dortmunders, and helles. Lighter Vienna, American darks, cream ales and mainstream golden ales are also fine in this blue collar glass."
              },
              {
                "name": "Shaker",
                "description": "The American microbrewer’s standard. A gently sloped 16 oz. glass made for session-type beers. Ambers, English & American pales, and sometimes darker session ales are typically served in these glasses, which are better known for their durability, than for any particularly beneficial properties. It is for that reason that some beer geeks have developed a hatred of the shaker."
              },
              {
                "name": "Tulip",
                "description": "The most varied glass in the world of beer. This style of glass has been around a while but only recently has found in a home in the eyes of beer-lovers the world over. It is the ultimate beer-tasting utility glass. The bulbous bottom makes for great drinking, the flared mouth allows for wonderful head formation and aroma release, and while it is short enough to handle the biggest beer styles, it is tall enough to service IPAs and other complex session beers. The Duvel glass is a well-known variant of the tulip style, and the Ratebeer tasting glass is an almost perfect example."
              }
            ]
          },
          "styleScore": 49.84136329770405,
          "overallScore": 56.59243329296733,
          "averageRating": 3.25998592376709,
          "realAverage": null,
          "ratingCount": 94,
          "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_120,c_limit,d_beer_icon_default.png,f_auto/beer_89047.jpg",
          "availability": {
            "bottle": "available",
            "tap": "unknown",
            "distribution": "local"
          },
          "purchase": null,
          "confidence": null
        },
        {
          "id": "89357",
          "name": "Good Old Potosi",
          "description": "A golden ale with a delicate malt flavor and sweet finish.  Light in body, full in flavor.",
          "brewer": {
            "id": "9444",
            "name": "Potosi Brewing Company",
            "description": "Potosi Brewery , Wisconsin Craft Beer, All Profits to Charity",
            "type": "Brew Pub/Brewery",
            "streetAddress": "209 South Main Street",
            "city": "Potosi",
            "state": {
              "name": "Wisconsin"
            },
            "zip": "53820",
            "phone": "763-4002",
            "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_150,c_limit,d_brewerdefault_hk6nu1.png,f_auto/brew_9444.jpg",
            "score": 126605,
            "isRetired": false
          },
          "contractBrewer": null,
          "abv": 4.5,
          "ibu": 15,
          "calories": 135,
          "labels": [],
          "seasonal": "UNKNOWN",
          "style": {
            "name": "Golden Ale / Blond Ale",
            "description": "There are a few different types of blond ale. The first is the traditional \"Canadian Ale\", an adjunct-laden, macrobrewed, top-fermented equivalent of the American Standard. The second is common in US brewpubs - a light starter ale, with marginally more hop and body than a macrobrew, fewer adjuncts, but still not a flavourful beer by any means. The British interpretation is easily the boldest, hoppiest blond ale rendition. Some of these can almost be considered American Pales they are so hopped up - very crisp, refreshing, with relatively low alcohol compared with their North American counterparts.",
            "glasses": [
              {
                "name": "English pint",
                "description": "These have a similar purpose to the shaker in that they are made for session ales, in this case bitters, milds, porters and stouts. There are a couple of key differences. First, they pour a proper pint (and usually have a line indicating where that is on the glass, just to make sure you don’t get ripped off). Second, they have a bit more flourish than the bland shaker. There are basically two variations. The first has a gentle curve covering the upper 2/3 of the glass - Guinness uses these. The second has a straight slope for the bottom two-thirds, and then a bump near the top, flattening out at the mouth of the glass."
              },
              {
                "name": "Shaker",
                "description": "The American microbrewer’s standard. A gently sloped 16 oz. glass made for session-type beers. Ambers, English & American pales, and sometimes darker session ales are typically served in these glasses, which are better known for their durability, than for any particularly beneficial properties. It is for that reason that some beer geeks have developed a hatred of the shaker."
              }
            ]
          },
          "styleScore": 13.85451713636592,
          "overallScore": 14.546426168509916,
          "averageRating": 2.6600770950317383,
          "realAverage": null,
          "ratingCount": 56,
          "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_120,c_limit,d_beer_icon_default.png,f_auto/beer_89357.jpg",
          "availability": {
            "bottle": "unknown",
            "tap": "unknown",
            "distribution": "unknown"
          },
          "purchase": null,
          "confidence": null
        },
        {
          "id": "175714",
          "name": "Good People Bearded Lady",
          "description": "The Bearded Lady is a bit of a departure from the Good People norm. While most of our beers are robust, bold, and hoppy, the Bearded Lady is smooth and drinkable. Never fear, it still has the quality craftsmanship you expect from Good People. \r\n\r\nOur take on the Wheat Beer, a perennial favorite, we hope to have made a beer that is both flavorful and refreshing. The light body is complemented with just a hint of hops and just a twinge of tartness that give the Bearded Lady a subtle citrus flavor that leaves you wanting more.\r\n\r\nWhile we were not trying to reinvent the wheel or change the history of beer, we wanted to make a beer that was refreshing and highly drinkable for the warm Alabama summer, yet not sacrifice the integrity of anything with the Good People label. This is a beer we would be proud to hoist over our lawnmowers and say, “Today grass…you are mine!” \r\n\r\nWith the Bearded Lady, we hope we have done just that. We hope you think so too.",
          "brewer": {
            "id": "9621",
            "name": "Good People Brewing Company",
            "description": "",
            "type": "Microbrewery",
            "streetAddress": "1035 20th St S, Ste B",
            "city": "Birmingham",
            "state": {
              "name": "Alabama"
            },
            "zip": "35205",
            "phone": "588 - 8002",
            "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_150,c_limit,d_brewerdefault_hk6nu1.png,f_auto/brew_9621.jpg",
            "score": 118759,
            "isRetired": false
          },
          "contractBrewer": null,
          "abv": 4.5,
          "ibu": 17,
          "calories": 135,
          "labels": [],
          "seasonal": "UNKNOWN",
          "style": {
            "name": "Wheat Ale",
            "description": "Golden to light amber in color, the body is light to medium. The wheat lends a crispness to the brew, often with some acidity. Some hop flavour may be present, but bitterness is low. Not as estery as German or Belgian-style wheats.",
            "glasses": [
              {
                "name": "Shaker",
                "description": "The American microbrewer’s standard. A gently sloped 16 oz. glass made for session-type beers. Ambers, English & American pales, and sometimes darker session ales are typically served in these glasses, which are better known for their durability, than for any particularly beneficial properties. It is for that reason that some beer geeks have developed a hatred of the shaker."
              },
              {
                "name": "Weizen",
                "description": "The classic German wheat beer glass is tall, narrow and flared at the top. This design accentuates both the hazy appearance of a classic hefeweizen, but also allows for abundant head formation. They typically hold 1/2L of beer. The one drawback to these glasses is that with so much glass exposed to the atmosphere, the beer warms more quickly than one might like on a hot summer’s day."
              }
            ]
          },
          "styleScore": 61.046848951026575,
          "overallScore": 42.73651757430236,
          "averageRating": 3.103095054626465,
          "realAverage": null,
          "ratingCount": 39,
          "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_120,c_limit,d_beer_icon_default.png,f_auto/beer_175714.jpg",
          "availability": {
            "bottle": "unknown",
            "tap": "unknown",
            "distribution": "local"
          },
          "purchase": null,
          "confidence": null
        },
        {
          "id": "107439",
          "name": "Good People Fatso Imperial Stout",
          "description": "First debuted at the 2009 Magic City Brewfest as the first Imperial Stout legally brewed in Alabama. This bottle conditioned version was brewed especially for the County Line Series.  A huge, viscous, full-bodied, dark as night, imperial stout yet somehow amazingly drinkable. Big aromas and flavors, including cherries and raspberries, roasted malts, dark chocolate, and spiced rum.  It’s recommeded to serve in the low to mid 50s as the flavors really explode when allowed to come up in temperature.  ABV 8.5%, 72 bottles.",
          "brewer": {
            "id": "9621",
            "name": "Good People Brewing Company",
            "description": "",
            "type": "Microbrewery",
            "streetAddress": "1035 20th St S, Ste B",
            "city": "Birmingham",
            "state": {
              "name": "Alabama"
            },
            "zip": "35205",
            "phone": "588 - 8002",
            "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_150,c_limit,d_brewerdefault_hk6nu1.png,f_auto/brew_9621.jpg",
            "score": 118759,
            "isRetired": false
          },
          "contractBrewer": null,
          "abv": 8.5,
          "ibu": null,
          "calories": 255,
          "labels": [],
          "seasonal": "UNKNOWN",
          "style": {
            "name": "Stout - Imperial",
            "description": "Imperial stouts are usually extremely dark brown to black in color with flavors that are intensely malty, deeply roasted and sometimes with accents of dark fruit &#40raisin, fig&#41 and chocolate. The bitterness is typically low to moderate. Imperial stouts are strong and generally exceed 8% ABV.",
            "glasses": [
              {
                "name": "Snifter",
                "description": "Whether a pure brandy snifter or a variant, these are used most commonly for barley wines, eisbocks and imperial stouts. They are stemmed and footed, bulbous at the bottom and narrowing all the way to the top. Because barley wines often have little head formation, the narrow mouth is fine as far as that goes, but still inhibits aroma a little bit, the tradeoff being the appearance of elegance. Many snifter variants made for beers have wider-than-average mouths for this reason."
              }
            ]
          },
          "styleScore": 46.07836824639502,
          "overallScore": 94.03394711485916,
          "averageRating": 3.6186330318450928,
          "realAverage": null,
          "ratingCount": 38,
          "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_120,c_limit,d_beer_icon_default.png,f_auto/beer_107439.jpg",
          "availability": {
            "bottle": "unknown",
            "tap": "unknown",
            "distribution": "unknown"
          },
          "purchase": null,
          "confidence": null
        },
        {
          "id": "105874",
          "name": "Good People Mumbai Rye IPA",
          "description": "",
          "brewer": {
            "id": "9621",
            "name": "Good People Brewing Company",
            "description": "",
            "type": "Microbrewery",
            "streetAddress": "1035 20th St S, Ste B",
            "city": "Birmingham",
            "state": {
              "name": "Alabama"
            },
            "zip": "35205",
            "phone": "588 - 8002",
            "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_150,c_limit,d_brewerdefault_hk6nu1.png,f_auto/brew_9621.jpg",
            "score": 118759,
            "isRetired": false
          },
          "contractBrewer": null,
          "abv": 6.5,
          "ibu": null,
          "calories": 195,
          "labels": [],
          "seasonal": "UNKNOWN",
          "style": {
            "name": "IPA",
            "description": "India Pale Ale, the modern version of which has largely been formed in the US, has an intense hop flavor, a golden to copper color, and a medium malty body. The aroma is moderate to very strong. IPAs work especially well at cutting the heat of chili, vindaloo or Sichuan cuisine.  In England, IPA is often just another name for bitter although some micros are doing their own versions of an American IPA as well.",
            "glasses": [
              {
                "name": "Shaker",
                "description": "The American microbrewer’s standard. A gently sloped 16 oz. glass made for session-type beers. Ambers, English & American pales, and sometimes darker session ales are typically served in these glasses, which are better known for their durability, than for any particularly beneficial properties. It is for that reason that some beer geeks have developed a hatred of the shaker."
              },
              {
                "name": "Tulip",
                "description": "The most varied glass in the world of beer. This style of glass has been around a while but only recently has found in a home in the eyes of beer-lovers the world over. It is the ultimate beer-tasting utility glass. The bulbous bottom makes for great drinking, the flared mouth allows for wonderful head formation and aroma release, and while it is short enough to handle the biggest beer styles, it is tall enough to service IPAs and other complex session beers. The Duvel glass is a well-known variant of the tulip style, and the Ratebeer tasting glass is an almost perfect example."
              }
            ]
          },
          "styleScore": 49.94712357968785,
          "overallScore": 74.54553938255813,
          "averageRating": 3.3791871070861816,
          "realAverage": null,
          "ratingCount": 29,
          "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_120,c_limit,d_beer_icon_default.png,f_auto/beer_105874.jpg",
          "availability": {
            "bottle": "unknown",
            "tap": "unknown",
            "distribution": "regional"
          },
          "purchase": null,
          "confidence": null
        },
        {
          "id": "388592",
          "name": "Good Guys Pilot IPA",
          "description": "",
          "brewer": {
            "id": "22688",
            "name": "Good Guys Brew",
            "description": "",
            "type": "Client Brewer",
            "streetAddress": "Matmejeriet 2",
            "city": "Karlstad",
            "state": null,
            "zip": "65343",
            "phone": "",
            "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_150,c_limit,d_brewerdefault_hk6nu1.png,f_auto/brew_22688.jpg",
            "score": 121083,
            "isRetired": false
          },
          "contractBrewer": null,
          "abv": 7,
          "ibu": null,
          "calories": 210,
          "labels": [],
          "seasonal": "UNKNOWN",
          "style": {
            "name": "IPA",
            "description": "India Pale Ale, the modern version of which has largely been formed in the US, has an intense hop flavor, a golden to copper color, and a medium malty body. The aroma is moderate to very strong. IPAs work especially well at cutting the heat of chili, vindaloo or Sichuan cuisine.  In England, IPA is often just another name for bitter although some micros are doing their own versions of an American IPA as well.",
            "glasses": [
              {
                "name": "Shaker",
                "description": "The American microbrewer’s standard. A gently sloped 16 oz. glass made for session-type beers. Ambers, English & American pales, and sometimes darker session ales are typically served in these glasses, which are better known for their durability, than for any particularly beneficial properties. It is for that reason that some beer geeks have developed a hatred of the shaker."
              },
              {
                "name": "Tulip",
                "description": "The most varied glass in the world of beer. This style of glass has been around a while but only recently has found in a home in the eyes of beer-lovers the world over. It is the ultimate beer-tasting utility glass. The bulbous bottom makes for great drinking, the flared mouth allows for wonderful head formation and aroma release, and while it is short enough to handle the biggest beer styles, it is tall enough to service IPAs and other complex session beers. The Duvel glass is a well-known variant of the tulip style, and the Ratebeer tasting glass is an almost perfect example."
              }
            ]
          },
          "styleScore": 69.77884931601315,
          "overallScore": 83.87100206982265,
          "averageRating": 3.463676929473877,
          "realAverage": null,
          "ratingCount": 28,
          "imageUrl": "https://res.cloudinary.com/ratebeer/image/upload/w_120,c_limit,d_beer_icon_default.png,f_auto/beer_388592.jpg",
          "availability": {
            "bottle": "unknown",
            "tap": "unknown",
            "distribution": "unknown"
          },
          "purchase": null,
          "confidence": null
        }
      ]
    }
  }
}
"""