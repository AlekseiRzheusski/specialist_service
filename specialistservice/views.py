from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
import folium
from django.db.models import Count
from django.views import generic
from .forms import UserRegistration, UserUpdateForm, SpecialistForm, CommentForm
from .decorators import unauthenticated_user, allowed_users
from .models import User, Specialist, Comment, Request
from .function import get_latlong, get_distance, phone_match
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
    print(lat,lon)


    if lat is not None or lon is not None:
        map = folium.Map(width=400, height = 250, location=[lat,lon])
        folium.Marker([lat,lon], tooltip='Your location').add_to(map)
    else:
        map = folium.Map(width=400, height = 250, location=[53.8843138,27.3131922])
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

    specialist = Specialist(person = user)
    specialist.save()
    return redirect('specialistupdate')


@login_required
@allowed_users(allowed_roles=['specialist'])
def specialist_update_page(request):
    specialist = request.user.specialist
    print(specialist.person)
    form = SpecialistForm(instance=specialist)
    if request.method == 'POST':
        form = SpecialistForm(request.POST, request.FILES,instance=specialist)
        if form.is_valid():
            form.save()

    return render(request,'specialistservice/specialist_update_page.html',{'form':form})


def specialist_detail_view(request, pk):
    try:
        specialist = Specialist.objects.get(pk=pk)
    except Specialist.DoesNotExist:
        raise Http404("Такого специалиста не существует")

    specialist_lat = specialist.person.latitude
    specialist_lon = specialist.person.longtitude
    map = '------'
    distance = '------'
    form_comment = 'Вы должны авторизоваться чтобы оставить комментарий'
    if specialist_lat is not None or specialist_lon is not None:
        map = folium.Map(width=460, height = 250, location=[specialist_lat,specialist_lon])
        folium.Marker([specialist_lat,specialist_lon], tooltip='Specialist location', icon=folium.Icon(color='red')).add_to(map)
        if request.user.is_authenticated:
            user_lat = request.user.latitude
            user_lon = request.user.longtitude
            if user_lat is not None or user_lon is not None:
                folium.Marker([user_lat,user_lon], tooltip='Your location', icon=folium.Icon(color='green')).add_to(map)
                distance = get_distance((user_lat,user_lon),(specialist_lat,specialist_lon))

        map = map._repr_html_()

    # print(request.user)


    if request.user.is_authenticated:
        if request.user.id == specialist.person.id:
            form_comment = 'Вы не можете оставлять комментарии на своей странице'
        else:
            form_comment = CommentForm()
            if request.method == 'POST':
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment_text = form['comment'].value()
                    # print(request.user)
                    comment = Comment(specialist=specialist,user=request.user,comment=comment_text)
                    comment.save()

    context = {}
    context['specialist'] = specialist
    context['map'] = map
    context['form'] = form_comment
    context['distance'] = distance
    return render(request,'specialistservice/specialist_detail_page.html', context)


class SpecialistListView(generic.ListView):
    model = Specialist
    paginate_by = 10

    def get_queryset(self): # new
        print(self.request.user)
        if self.request.user.is_authenticated:
            object_list = Specialist.objects.filter(person__city=self.request.user.city).annotate(num_comments = Count('comment')).order_by('-num_comments')
        else:
            object_list = Specialist.objects.all()
        return object_list


def add_request(request,pk):
    try:
        specialist = Specialist.objects.get(pk=pk)
    except Specialist.DoesNotExist:
        raise Http404("Такого специалиста не существует")
    new_request = Request(specialist=specialist,user=request.user) 
    new_request.save()
    return redirect('specialist-detail', pk=pk)

class RequestsListView(generic.ListView):
    model = Request

    def get_queryset(self):
        object_list = Request.objects.filter(specialist__person__id = self.request.user.id)
        return object_list

def delete_request(request,pk):
    try:
        del_request = Request.objects.get(pk=pk)
    except Request.DoesNotExist:
        raise Http404("Такого специалиста не существует")
    del_request.delete()
    return redirect('request-list')


class UserDetailView(generic.DetailView):
    model = User