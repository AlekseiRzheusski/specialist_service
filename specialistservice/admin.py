from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import City, Specialty, Specialist, Comment, PrivateRoom, Message, Notification
from .models import User
from .forms import CustomUserCreationForm
# Register your models here.


class CustomUserAdmin(UserAdmin):
    """Custom user form page for change user"""
    model = User
    add_form = CustomUserCreationForm
    fieldsets = (
        *UserAdmin.fieldsets, (
            'Additional info',
            {
                'fields': (
                    'phone',
                    'city',
                    'street',
                    'house',
                    'latitude',
                    'longtitude',
                    'profile_pic',
                )
            }
        )
    )


admin.site.register(City)
admin.site.register(Specialty)
admin.site.register(Specialist)
admin.site.register(Comment)
admin.site.register(User, CustomUserAdmin)
admin.site.register(PrivateRoom)
admin.site.register(Message)
admin.site.register(Notification)
