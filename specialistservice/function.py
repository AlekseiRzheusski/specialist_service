import geopy
from django import forms
import geopy.distance
import re
from .models import PrivateRoom, Message


def get_latlong(adress):
    locator = geopy.geocoders.Nominatim(user_agent='myGeocoder')
    location = locator.geocode(adress + ', Беларусь',language='ru_RU') 
    return location

def get_distance(user_latlon,specialist_latlon):
    dist = geopy.distance.distance(user_latlon, specialist_latlon).km
    return dist

def phone_match(phone):
    return re.match(r'^((8|\+375)[\- ]?)?(\(?\d{2}\)?[\- ]?)?[\d\- ]{7,10}$', phone)


def get_messages(private_room_id):
    try:
        messages = Message.objects.filter(private_room__room_name=private_room_id)
    except Message.DoesNotExist:
        print('no messages')
    return messages.order_by('timestamp').all()