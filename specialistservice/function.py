import geopy
from django import forms
import geopy.distance
import re
from django.utils.deconstruct import deconstructible
import os
from uuid import uuid4


def get_latlong(adress):
    locator = geopy.geocoders.Nominatim(user_agent='myGeocoder')
    location = locator.geocode(adress + ', Беларусь',language='ru_RU') 
    return location

def get_distance(user_latlon,specialist_latlon):
    dist = geopy.distance.distance(user_latlon, specialist_latlon).km
    return dist

def phone_match(phone):
    return re.match(r'^((8|\+375)[\- ]?)?(\(?\d{2}\)?[\- ]?)?[\d\- ]{7,10}$', phone)

@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if instance.username:
            filename = '{}.{}'.format(instance.username, ext)
        if os.path.exists(os.path.join(self.path, filename)):
            print(os.path.join(self.path, filename))
            os.remove(os.path.join(self.path, filename))
        return os.path.join(self.path, filename)

path_and_rename = PathAndRename("./account_images")