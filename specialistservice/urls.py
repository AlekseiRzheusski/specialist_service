from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('register/',views.register_page, name = 'register'),
    path('update/', views.user_update_page, name = 'userupdate'),
]