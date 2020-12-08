from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegistration
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group
from .models import User

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
