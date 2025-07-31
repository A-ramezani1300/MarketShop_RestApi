from django.contrib import admin
from .models import *

@admin.register(UserShop)
class UserShopAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'is_staff']
    list_filter = ['first_name', 'last_name', 'phone', 'is_staff', 'is_admin', 'is_superuser']


