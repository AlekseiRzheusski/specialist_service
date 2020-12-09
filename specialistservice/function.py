import geopy
from django import forms

def get_latlong(adress):
    locator = geopy.geocoders.Nominatim(user_agent='myGeocoder')
    location = locator.geocode(adress + ', Беларусь',language='ru_RU') 
    return location