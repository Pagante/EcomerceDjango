from django.contrib import admin
from .models import Cart,CartItem
# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id']


@admin.register(CartItem)
class CartItem(admin.ModelAdmin):
    list_display = ['product','cart','quantity','is_active']
