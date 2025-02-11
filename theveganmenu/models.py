from django.db import models

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=300)
    link = models.CharField(max_length=500)
    longitude = models.DecimalField(max_digits=20, decimal_places=13, default=0)
    latitude = models.DecimalField(max_digits=20, decimal_places=13, default=0)

class MenuItem(models.Model):
    item_name = models.CharField(max_length=300)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete = models.CASCADE,
        related_name = 'restaurants'
    )
    choices = [('appetizer','appetizer'),
               ('food', 'food'),
               ('beverage','beverage'),
               ('dessert','dessert')]
    item_type = models.CharField(max_length=20, choices=choices)
    additional_info = models.CharField(max_length=2000)
