# Generated by Django 4.2.7 on 2025-02-07 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theveganmenu', '0002_menuitem_restaurant_restaurant_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='latitude',
            field=models.DecimalField(decimal_places=13, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='longitude',
            field=models.DecimalField(decimal_places=13, default=0, max_digits=20),
        ),
    ]
