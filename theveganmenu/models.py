from django.db import models

# Create your models here.


class RestaurantChain(models.Model):
    name = models.CharField(max_length=50)
    menu = models.ForeignKey(
        'Menu',
        on_delete = models.CASCADE,
        related_name = 'chain_menu',
        null = True,
        blank = True
    )

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    restaurant_chain = models.ForeignKey(
        RestaurantChain,
        on_delete = models.CASCADE,
        related_name = 'restaurant_chain',
        null = True,
        blank = True
    )
    menu = models.ForeignKey(
        'Menu',
        on_delete = models.CASCADE,
        related_name = 'restaurant_menu',
        null = True,
        blank = True
    )
    is_fully_vegan = models.BooleanField(default=False)
    address = models.CharField(max_length=300)
    link = models.CharField(max_length=500)
    longitude = models.DecimalField(max_digits=20, decimal_places=13, default=0)
    latitude = models.DecimalField(max_digits=20, decimal_places=13, default=0)

    def get_menu(self):
        if not self.restaurant_chain is None:
            if not self.restaurant_chain.menu is None:
                return self.restaurant_chain.menu
        return self.menu

    def __str__(self):
        return self.name

class Menu(models.Model):
    name = models.CharField(max_length=100, blank=True) 
    
    def __str__(self):
        return f'{str(self.name)}'

class MenuSection(models.Model):
    name = models.CharField(max_length=100)
    menu = models.ForeignKey(
        Menu,
        on_delete = models.CASCADE,
        related_name = 'menu',
    )
    order = models.IntegerField(default=0)

    def __str__(self):
        return f'{str(self.menu.name)} {self.name}'

class MenuItem(models.Model):
    item_name = models.CharField(max_length=300)
    item_description = models.CharField(max_length=2000, blank=True, default='')
    menu_section = models.ForeignKey(
        MenuSection,
        on_delete = models.CASCADE,
        related_name = 'menu_sections'
    )
    additional_info = models.CharField(max_length=5000, default='', blank=True)

    def __str__(self):
        return f'{self.item_name}|{str(self.menu_section)}'