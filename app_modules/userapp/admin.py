from django.contrib import admin
from app_modules.userapp import models
from django.contrib.auth.admin import UserAdmin
from app_modules.userapp.models import CustomUser

# Register your models here.

#login  
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('username', 'email', 'role', 'is_approved', 'is_staff')
    list_filter = ('role', 'is_approved')

    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {
            'fields': ('role', 'is_approved', 'phone_number', 'profile_image', 'address', 'date_of_birth')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {
            'fields': (
                'role',
                'is_approved',
                'phone_number',
                'address',
                'date_of_birth',
                'profile_image'
            ),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)


#Booking
admin.site.register(models.Booking)