from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    """Custom user form for admin"""
    class Meta:
        model = User
        fields = '__all__'