from django.contrib import admin

from .models import CustomUser, CustomUserManager


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_superuser']


admin.site.register(CustomUser, UserAdmin)
