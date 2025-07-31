from django.contrib import admin
from .models import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'payment', 'created', 'updated']
    list_filter = ['buyer', 'payment', 'created', 'updated']
    inlines = [OrderItemInline]


@admin.register(DiscountPercentage)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'active']



# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ['product', ]


# @admin.register(OrderItem)
# class OrderItem(admin.ModelAdmin):
#     list_display = ['order', 'product', 'quantity', 'price', 'created']
#     list_filter = ['order', 'product', 'quantity', 'price', 'created']
