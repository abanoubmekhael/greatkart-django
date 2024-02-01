from .models import Cart , CartItem
from django.urls import path
from . views import _cart_id


def counter(request):
    cart_count = 0 
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id = _cart_id(request))
            # Cart.objects.filter VS CartItem.objects.all().filter()
            # must return a QuerySet. Vs Proxied
            # dealing with a QuerySet and not a Manager, because MyModel.objects returns a Manager.
            cart_items = CartItem.objects.all().filter(cart =cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantatity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict (cart_count = cart_count)



# ع الشاشة أثناء السكرول
    # Fixed مسمار في النافبار وتحدد ال 4 قيم توب بوتوم رايت ليفت
    # Relative: بيتحرك ويحجز مكانه زي ماهو
    # absolute: يدور ع الاب relative ثم  مش مسمار 