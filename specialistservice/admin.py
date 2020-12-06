from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import City, District, Specialty, Specialist, VisitToClient, Comment
from .models import User
from .forms import CustomUserCreationForm
# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,(
            'Additional info',
            {
                'fields':(
                    'phone',
                    'adress',
                    'latitude',
                    'longtitude',
                    'profile_pic',
                    'district'
                )
            }
        )
    )

admin.site.register(City)
admin.site.register(District)
admin.site.register(Specialty)
admin.site.register(Specialist)
admin.site.register(VisitToClient)
admin.site.register(Comment)
admin.site.register(User, CustomUserAdmin)
