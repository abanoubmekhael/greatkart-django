from django.contrib import admin
from . models import Cart
from . models import CartItem

class CartAdmin (admin.ModelAdmin):
    list_display = ('cart_id' , 'date_added')
    
class CartItemAdmin (admin.ModelAdmin):
    list_display = ('product' , 'cart' , 'quantatity' , 'is_active')
   

# Register your models here.
admin.site.register(Cart , CartAdmin)
admin.site.register(CartItem , CartItemAdmin)