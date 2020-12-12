import geopy
from django import forms
import geopy.distance
import re

def get_latlong(adress):
    locator = geopy.geocoders.Nominatim(user_agent='myGeocoder')
    location = locator.geocode(adress + ', Беларусь',language='ru_RU') 
    return location

def get_distance(user_latlon,specialist_latlon):
    dist = geopy.distance.distance(user_latlon, specialist_latlon).km
    return dist

def phone_match(phone):
    return re.fullmatch(r'/^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$/', '+1-541-754-3010')

