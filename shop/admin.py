from django.contrib import admin
from .models import *

class ImageInline(admin.TabularInline):
    model = Image
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_filter = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'name']
    list_filter = ['category', 'name']
    prepopulated_fields = {'slug':('name',)}
    inlines = [ImageInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'is_reply']
    list_filter = ['product', 'name', 'is_reply']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'title', 'subject', 'created']
    list_filter = ['name', 'phone', 'title', 'subject', 'created']


@admin.register(TicketResponse)
class TicketResponse(admin.ModelAdmin):
    list_display = ['ticket', 'user_response', 'created']
    list_filter = ['ticket', 'user_response', 'created']




