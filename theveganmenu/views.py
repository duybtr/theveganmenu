from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Restaurant, MenuItem
from django.db import connection
from django.db.models import Q
import requests
from django.http import HttpResponse
from theveganmenu.common.utils import access_secret_version
from theveganmenu.management.commands.populate_long_lat import get_long_lat


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'

def get_restaurants(request):
    
    context = {}

    user_lng = float(request.POST['userLng'])
    user_lat = float(request.POST['userLat'])

    # Need to replace hardcoded latitude and longitude
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id, name, address, link , acos(sin(radians({user_lat})) * sin(radians(32.9192404)) + cos(radians({user_lat})) * cos(radians(32.9192404)) * cos(radians({user_lng}) - radians(longitude))) * 6371 * 0.621371 AS distance FROM theveganmenu_restaurant ORDER BY distance LIMIT 3") 
        rows = cursor.fetchall()
    restaurant_ids = [r[0] for r in rows]
    restaurants = [{'id' : rows[i][0],
                 'name' : rows[i][1],
                 'address': rows[i][2], 
                 'link': rows[i][3],
                 'distance': rows[i][4]}  
                    for i in range(len(rows))]
    context['restaurants'] = restaurants
    
    return render(request, 'theveganmenu/partial/restaurant_list.html', context)

def get_menu_dict(menu_list):
    menu_dict = {}
    for f in menu_list:
        if not f.restaurant.id in menu_dict.keys():
            menu_dict[f.restaurant.id] = []
        menu_dict[f.restaurant.id].append(f)
    return menu_dict

def get_food_menu(request, restaurant_pk):
    q = Q()
    q = q & Q(restaurant_id = restaurant_pk)
    q = q & Q(item_type = 'food')
    food_items = MenuItem.objects.filter(q)
    context = {'menu_items': food_items}
    print(context)
    return render(request, 'theveganmenu/partial/menu.html', context)

def get_dessert_menu(request, restaurant_pk):
    q = Q()
    q = q & Q(restaurant_id = restaurant_pk)
    q = q & Q(item_type = 'dessert')
    dessert_items = MenuItem.objects.filter(q)
    context = {'menu_items': dessert_items}
    print(context)
    return render(request, 'theveganmenu/partial/menu.html', context)

def get_beverage_menu(request, restaurant_pk):
    q = Q()
    q = q & Q(restaurant_id = restaurant_pk)
    q = q & Q(item_type = 'beverage')
    beverage_items = MenuItem.objects.filter(q)
    context = {'menu_items': beverage_items}
    print(context)
    return render(request, 'theveganmenu/partial/menu.html', context)

def get_menu(request):
    q = Q()
    # Get the list of 20 closest restaurants
    # Retrieve the menu items, filtered by the restaurant ids above. Divide them into 3 separate lists (food, dessert, beverage)
    context = {}

    user_lng = float(request.POST['userLng'])
    user_lat = float(request.POST['userLat'])
    address = None
    if 'address' in request.POST.keys():
        address = request.POST['address']
    if not address is None and len(address) > 0:
        user_lng, user_lat = get_long_lat(address)
    # Need to replace hardcoded latitude and longitude
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id, name, address, link , round((acos(sin(radians({user_lat})) * sin(radians(latitude)) + cos(radians({user_lat})) * cos(radians(latitude)) * cos(radians({user_lng}) - radians(longitude))) * 6371 * 0.621371)::numeric,2) AS distance FROM theveganmenu_restaurant ORDER BY distance LIMIT 3") 
        rows = cursor.fetchall()
    restaurant_ids = [r[0] for r in rows]

    restaurants = [{'id' : rows[i][0],
                 'name' : rows[i][1],
                 'address': rows[i][2], 
                 'link': rows[i][3],
                 'distance': rows[i][4]}  
                    for i in range(len(rows))]

    q = q & Q(restaurant_id__in = restaurant_ids)
    q_food = q & Q(item_type = 'food')
    q_beverage = q & Q(item_type = 'beverage')
    q_dessert = q & Q(item_type = 'dessert')
    menu_items = MenuItem.objects.all()
    food_items = menu_items.filter(q_food)
    beverage_items = menu_items.filter(q_beverage)
    dessert_items = menu_items.filter(q_dessert)

    food_items_dict = get_menu_dict(food_items)
    beverage_items_dict = get_menu_dict(beverage_items)
    dessert_items_dict = get_menu_dict(dessert_items)
    
     # for each restaurant display the restaurants below
     # Add api key
    context = {'restaurants': restaurants, 
               'foods': food_items_dict, 
               'beverages': beverage_items_dict, 
               'desserts':dessert_items_dict}
    return render(request, 'theveganmenu/partial/restaurant_list.html', context)



    

