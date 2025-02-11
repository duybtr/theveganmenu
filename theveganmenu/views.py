from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Restaurant
from django.db import connection
import requests
from django.http import HttpResponse


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'

def get_restaurants(request):
    
    context = {}

    user_lng = float(request.POST['userLng'])
    user_lat = float(request.POST['userLat'])

    # Need to replace hardcoded latitude and longitude
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT name, address, link , acos(sin(radians({user_lat})) * sin(radians(32.9192404)) + cos(radians({user_lat})) * cos(radians(32.9192404)) * cos(radians({user_lng}) - radians(longitude))) * 6371 * 0.621371 AS distance FROM theveganmenu_restaurant ORDER BY distance LIMIT 3") 
        rows = cursor.fetchall()
    addresses = [r[1] for r in rows]
    # headers = {'Content-Type': 'application/json',
    #             'Authorization': 'Bearer ya29.a0AXeO80R8P7v7On3RcdDOiuwHhAfIUkXYtiS-yUYlHAo7kWAO4PYyJBoTL4JEzkcpnqLyHqGPEzzvjVPmyWu4ROoDkXIIjFywd7g_wBQ7QFO2jdEL4AWtkDQR0u5x6Ud525hTk754E2N2ksTG6qFOtyqUUKIUXzr7Fg003lQHOAaCgYKARsSARASFQHGX2MiLm-iepB0mSXIiPvz-dW5mw0177',
    #             'X-Goog-User-Project': 'veganapp-446321',
    #             'X-Goog-FieldMask': 'places.displayName,places.formattedAddress'
    #           }

    
    # restaurants_data = {
    #             "includedTypes": ["restaurant"],
    #             "maxResultCount": 10,
    #             "locationRestriction": {
    #                 "circle": {
    #                 "center": {
    #                     "latitude": userLat,
    #                     "longitude": userLng},
    #                 "radius": 500.0
    #                 }
    #             }
    #         }
    # restaurants_response = requests.post("https://places.googleapis.com/v1/places:searchNearby", headers=headers,  json=restaurants_data)
    # restaurants = Restaurant.objects.all()
    
    # Change the parameter 'units' to 'IMPERIAL'
    payload = {'destinations': '|'.join(addresses) ,'origins':f'{user_lat},{user_lng}','key':'AIzaSyCM1pTtJL8eBKe6iun6VU-L5GWQ3VxB5qQ'}
    distances_response = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json', params=payload)
    


    # destination addresses index: distances_response.json()['destination_addresses']
    # results: distances_response.json()['rows'][0]['elements']
    import pdb; pdb.set_trace()
    num_destinations = len(distances_response.json()['destination_addresses'])
    results = [ {'restaurant_name': distances_response.json()['destination_addresses'][i], 
                 'distance': distances_response.json()['rows'][0]['elements'][i]['distance']['text']  }  
                    for i in range(num_destinations)]
    context['results'] = results
    
    print(distances_response.text)
    return HttpResponse()


    

