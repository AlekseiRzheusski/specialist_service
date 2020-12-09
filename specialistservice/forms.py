from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.forms import ModelForm


class CustomUserCreationForm(UserCreationForm):
    """Custom user form for admin"""
    class Meta:
        model = User
        fields = '__all__' 

class UserRegistration(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(ModelForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone','street','house','city']