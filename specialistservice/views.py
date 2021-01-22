from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.db.models import Q
import folium
from django.db.models import Count
from django.views import generic
from .forms import UserRegistration, UserUpdateForm, SpecialistForm, CommentForm
from .decorators import unauthenticated_user, allowed_users
from .models import User, Specialist, Comment, Request, Notification, PrivateRoom
from .function import get_latlong, get_distance, phone_match
from django import forms


# Create your views here.

def index(request):
    return render(request, 'index.html')


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

    return render(request, 'specialistservice/register_page.html', {'form': form})


@login_required
@allowed_users(allowed_roles=['customer', 'specialist'])
def user_update_page(request):
    user = request.user

    lat = user.latitude
    lon = user.longtitude
    print(lat, lon)

    if lat is not None or lon is not None:
        map = folium.Map(width=400, height=250, location=[lat, lon])
        folium.Marker([lat, lon], tooltip='Your location').add_to(map)
    else:
        map = folium.Map(width=400, height=250, location=[
                         53.8843138, 27.3131922])
    map = map._repr_html_()

    form = UserUpdateForm(instance=user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if phone_match(form['phone'].value()) is not None:
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
            else:
                messages.info(request, 'Проверьте введенный номер телефона')

    return render(request, 'specialistservice/user_update_page.html', {'form': form, 'map': map})


@login_required
@allowed_users(allowed_roles=['customer'])
def make_specialist(request):
    user = request.user
    print(user.username)

    specialist_group = Group.objects.get(name='specialist')
    customer_group = Group.objects.get(name='customer')
    customer_group.user_set.remove(user)
    specialist_group.user_set.add(user)

    specialist = Specialist(person=user)
    specialist.save()
    return redirect('specialistupdate')


@login_required
@allowed_users(allowed_roles=['specialist'])
def specialist_update_page(request):
    specialist = request.user.specialist
    print(specialist.person)
    form = SpecialistForm(instance=specialist)
    if request.method == 'POST':
        form = SpecialistForm(request.POST, request.FILES, instance=specialist)
        if form.is_valid():
            form.save()

    return render(request, 'specialistservice/specialist_update_page.html', {'form': form})


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
        map = folium.Map(width=460, height=250, location=[
                         specialist_lat, specialist_lon])
        folium.Marker([specialist_lat, specialist_lon],
                      tooltip='Specialist location', icon=folium.Icon(color='red')).add_to(map)
        if request.user.is_authenticated:
            user_lat = request.user.latitude
            user_lon = request.user.longtitude
            if user_lat is not None or user_lon is not None:
                folium.Marker([user_lat, user_lon], tooltip='Your location', icon=folium.Icon(
                    color='green')).add_to(map)
                distance = get_distance(
                    (user_lat, user_lon), (specialist_lat, specialist_lon))

        map = map._repr_html_()

    if request.user.is_authenticated:
        if request.user.id == specialist.person.id:
            form_comment = 'Вы не можете оставлять комментарии на своей странице'
        else:
            form_comment = CommentForm()
            if request.method == 'POST':
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment_text = form['comment'].value()
                    comment = Comment(specialist=specialist,
                                      user=request.user, comment=comment_text)
                    comment.save()

    context = {}
    context['specialist'] = specialist
    context['map'] = map
    context['form'] = form_comment
    context['distance'] = distance
    return render(request, 'specialistservice/specialist_detail_page.html', context)


class SpecialistListView(generic.ListView):
    model = Specialist
    paginate_by = 5

    def get_queryset(self):  # new
        print(self.request.user)
        if self.request.user.is_authenticated:
            object_list = Specialist.objects.filter(person__city=self.request.user.city).annotate(
                num_comments=Count('comment')).order_by('-num_comments')
        else:
            object_list = Specialist.objects.all()
        return object_list


class SearchSpecialistListView(generic.ListView):
    model = Specialist
    paginate_by = 5
    template_name = 'specialist_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Specialist.objects.filter(
            Q(specialty__name__icontains=query) | Q(about__icontains=query) | Q(
                person__first_name__icontains=query) | Q(person__last_name__icontains=query)
        )
        return object_list


def add_request(request, pk):
    try:
        specialist = Specialist.objects.get(pk=pk)
    except Specialist.DoesNotExist:
        raise Http404("Такого специалиста не существует")
    new_request = Request(specialist=specialist, user=request.user)
    new_request.save()
    return redirect('specialist-detail', pk=pk)


class RequestsListView(generic.ListView):
    model = Request

    def get_queryset(self):
        object_list = Request.objects.filter(
            specialist__person__id=self.request.user.id)
        return object_list


@login_required
def delete_request(request, pk):
    try:
        del_request = Request.objects.get(pk=pk)
    except Request.DoesNotExist:
        raise Http404("Такого не существует")
    del_request.delete()
    return redirect('request-list')


class UserDetailView(generic.DetailView):
    model = User


@login_required
def room_search(request, username):
    print(request.user.username)
    usernames = [request.user.username, username]
    usernames.sort()
    room_name = '_'.join(usernames)
    if not PrivateRoom.objects.filter(room_name=room_name).exists():
        print('create:'+room_name)
        private_room = PrivateRoom(first_user=request.user, second_user=User.objects.get(
            username=username), room_name=room_name)
        private_room.save()
    return redirect('room', room_name=room_name)


@login_required
def room(request, room_name):
    if not PrivateRoom.objects.filter(room_name=room_name):
        print('room doesnt exist')
        return redirect('index')
    tmp_room = PrivateRoom.objects.get(room_name=room_name)
    print(tmp_room.first_user.username+"     "+tmp_room.second_user.username)
    if request.user == tmp_room.first_user or request.user == tmp_room.second_user:
        if request.user == tmp_room.first_user:
            recipient = tmp_room.second_user
        elif request.user == tmp_room.second_user:
            recipient = tmp_room.first_user
        return render(request, 'chat/room.html', {'room_name': room_name, 'recipient_id': recipient.id})
    print('no permission')
    return redirect('index')


class NotificationsListView(generic.ListView):
    model = Notification

    def get_queryset(self):
        object_list = Notification.objects.filter(
            user__id=self.request.user.id)
        return object_list


@login_required
def delete_notification(request, pk):
    try:
        del_notification = Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        raise Http404("Такого не существует")
    del_notification.delete()
    return redirect('notification-list')


@login_required
def room_list(request):
    object_list = PrivateRoom.objects.filter(
        Q(first_user=request.user) | Q(second_user=request.user))
    user_list = []
    for tmp_room in object_list:
        if request.user == tmp_room.first_user:
            user_list.append(tmp_room.second_user)
        elif request.user == tmp_room.second_user:
            user_list.append(tmp_room.first_user)
    return render(request, 'specialistservice/room_list.html', {'user_list': user_list})
