from django.core.management.base import BaseCommand
from theveganmenu.models import Restaurant
import requests
import logging
import google.cloud.logging

client = google.cloud.logging.Client()
class Command(BaseCommand):
    def handle(self, *args, **options):
        restaurants = Restaurant.objects.all()
        for r in restaurants:
            payload = {'address': r.address, 'key':'AIzaSyCM1pTtJL8eBKe6iun6VU-L5GWQ3VxB5qQ'}
            json_res = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=payload).json()
            if len(json_res['results']) == 0:
                logging.error(f"There was no result for {r['address']}")
            else:
                lat = json_res['results'][0]['geometry']['location']['lat']
                lng = json_res['results'][0]['geometry']['location']['lng']
                r.longitude = lng
                r.latitude = lat
                print(f'Saving lng {lng} and lat {lat} for {r.address}')
                logging.info(f'Saving lng {lng} and lat {lat} for {r.address}')
                r.save()
            