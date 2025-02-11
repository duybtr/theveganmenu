from .views import (
    HomePageView,
    get_restaurants
)
from django.urls import path


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('get_restaurants', get_restaurants, name='get_restaurants')
]