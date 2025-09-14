from django import forms
from .models import Restaurant

class CreateRestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name' , 'address' ,'website_link', 'is_fully_vegan']
        