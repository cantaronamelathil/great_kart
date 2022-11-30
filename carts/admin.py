from django.contrib import admin
from .models import Cart,Cartitem,wishlist
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'cart')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')



admin.site.register(Cart)
admin.site.register(Cartitem)
admin.site.register(wishlist)