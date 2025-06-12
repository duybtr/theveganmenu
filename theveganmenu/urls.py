from .views import (
    HomePageView,
    get_restaurants,
    get_menu,
    get_food_menu,
    get_dessert_menu,
    get_beverage_menu,
    get_menu_sections,
    get_menu_items
)
from django.urls import path

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('get_restaurants', get_restaurants, name='get_restaurants'),
    path('get_menu', get_menu, name='get_menu'),
    path('<int:restaurant_pk>/get_food_menu', get_food_menu, name='get_food_menu'),
    path('<int:restaurant_pk>/get_dessert_menu', get_dessert_menu, name='get_dessert_menu'),
    path('<int:restaurant_pk>/get_beverage_menu', get_beverage_menu, name='get_beverage_menu'),
    path('<int:menu_id>/get_menu_sections', get_menu_sections, name='get_menu_sections'),
    path('<int:menu_section_id>/get_menu_items', get_menu_items, name='get_menu_items'),
]