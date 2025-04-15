from django.core.management.base import BaseCommand
from theveganmenu.models import Restaurant
from django.db.models import Q
import requests
import logging
import google.cloud.logging
from google.cloud import secretmanager
from theveganmenu.common.utils import access_secret_version

client = google.cloud.logging.Client()

def get_long_lat(address):
    api_key = access_secret_version('projects/537347910332/secrets/google_map_api_key/versions/1')
    payload = {'address': address, 'key':api_key}
    json_res = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=payload).json()
    if len(json_res['results']) == 0:
        return None
    else:
        lng = json_res['results'][0]['geometry']['location']['lng']
        lat = json_res['results'][0]['geometry']['location']['lat']
        return (lng,lat)


class Command(BaseCommand):
    # def handle(self, *args, **options):
    #     restaurants = Restaurant.objects.all()
    #     for r in restaurants:
    #         api_key = access_secret_version('projects/537347910332/secrets/google_map_api_key/versions/1')
    #         payload = {'address': r.address, 'key':api_key}
    #         json_res = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=payload).json()
    #         if len(json_res['results']) == 0:
    #             logging.error(f"There was no result for {r['address']}")
    #         else:
    #             lat = json_res['results'][0]['geometry']['location']['lat']
    #             lng = json_res['results'][0]['geometry']['location']['lng']
    #             r.longitude = lng
    #             r.latitude = lat
    #             print(f'Saving lng {lng} and lat {lat} for {r.address}')
    #             logging.info(f'Saving lng {lng} and lat {lat} for {r.address}')
    #             r.save()
    def handle(self, *args, **options):
        import pdb; pdb.set_trace()
        q = Q(longitude=0) & Q(latitude=0)
        restaurants = Restaurant.objects.filter(q)
        for r in restaurants:
            lng_lat = get_long_lat(r.address)
            if not lng_lat is None:
                r.longitude = lng_lat[0]
                r.latitude = lng_lat[1]
                logging.info(f'Saving lng {r.longitude} and lat {r.latitude} for {r.address}')
                r.save()
            else:
                logging.error(f"There was no result for {r.address}")