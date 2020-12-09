from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import folium
from .forms import UserRegistration, UserUpdateForm
from .decorators import unauthenticated_user, allowed_users
from .models import User
from .function import get_latlong
from django import forms


# Create your views here.

def index(request):
    return render(request,'index.html')

@unauthenticated_user
def register_page(request):
    form = UserRegistration()
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.save()
            user.groups.add(group)
            return redirect('login')

    return render(request, 'specialistservice/register_page.html', {'form':form})


@login_required
@allowed_users(allowed_roles=['customer','specialist'])
def user_update_page(request):
    user = request.user

    lat = user.latitude
    lon = user.longtitude



    map = folium.Map(width=800, height = 500, location=[53.8843138,27.3131922])
    if lat is not None or lon is not None:
        folium.Marker([user.latitude,user.longtitude], tooltip='Your location').add_to(map)
    map = map._repr_html_()

    form = UserUpdateForm(instance = user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES,instance=user)
        if form.is_valid():

            city = form['city'].value()
            street = form['street'].value()
            house = form['house'].value()

            adress = f'{house}, улица {street}, {city}'

            print(adress)

            location = get_latlong(adress)

            if location is None:
                messages.info(request, 'Проверьте введенный адрес')

            else:
                upd_user = form.save()
                upd_user.latitude = location.latitude
                upd_user.longtitude = location.longitude
                upd_user.save()
    return render(request, 'specialistservice/user_update_page.html', {'form':form, 'map':map})

@login_required
@allowed_users(allowed_roles=['customer'])
def make_specialist(request):
    user = request.user
    print(user.username)
    specialist_group = Group.objects.get(name='specialist')
    customer_group = Group.objects.get(name='customer')
    customer_group.user_set.remove(user)
    specialist_group.user_set.add(user)
    return redirect('userupdate')


@login_required
@allowed_users(allowed_roles=['specialist'])
def specialist_update_page(request):
    pass

