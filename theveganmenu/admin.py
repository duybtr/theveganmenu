from django.contrib import admin
from .models import Restaurant, RestaurantChain, Menu, MenuSection, MenuItem

# Register your models here.
admin.site.register([Restaurant, RestaurantChain, Menu, MenuSection, MenuItem])