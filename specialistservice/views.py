from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
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
@allowed_users(allowed_roles=['customer'])
def user_update_page(request):
    user = request.user
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
            upd_user = form.save()
            upd_user.latitude = location.latitude
            upd_user.longtitude = location.longitude
            upd_user.save()
    return render(request, 'specialistservice/user_update_page.html', {'form':form})

