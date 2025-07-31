from django.contrib import admin
from .models import *

# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ['user', 'created', 'updated']
#     list_filter = ['user', 'created', 'updated']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'created', 'updated']
    list_filter = ['cart', 'product', 'quantity', 'created', 'updated']


# class CartItemInline(admin.TabularInline):
#     model = CartItem
#     raw_id_fields = ('product',)
#
#
# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'created', 'updated']
#     list_filter = ['user', 'created', 'updated']
#     inlines = [CartItemInline]
