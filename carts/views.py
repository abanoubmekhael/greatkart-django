from django.shortcuts import render , redirect , get_object_or_404
from store.models import Product, Variation
from . models import Cart , CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
# إنشاء جلسة
# مجرد id 
def _cart_id (request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# إنشاء:
#  بروداكت 
#   +
# TRY/EXCRT
# كارت )  <=الكارت id) -سيف
#  +
#  والكمية الكارت ايتم (البرودكت والكارت الفورين كي)  - سيف
# علامة الزائد +
def add_cart (request ,  product_id):
    product= Product.objects.get(id = product_id) 
    product_variation = []
    if request.method == 'POST':
        # color = request.POST['color']
        # size  = request.POST['size']
        # print (color, size) 
        for item in request.POST:     # more smarter
            key   = item              # Key
            value = request.POST[key] # method to fetch value  
            print(key , value)
    # try_variation
            try:
                variation = Variation.objects.get(product = product , variation_category__iexact = key , variation_value__iexact = value)
                product_variation.append(variation)  
            except:
                pass    # متعمش إي حإجة     
    # try_cart
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request)) 
    cart.save()
    # try_cart_item 
    is_cart_item_exists = CartItem.objects.filter( product= product , cart = cart).exists()
    if is_cart_item_exists : 
        # variation_existing => database            == cart(variations)
        # variation_current  => product_variation   ==__iexact, __iexact
        # item_id            => database
        cart_item = CartItem.objects.filter(product = product , cart = cart) 
        ex_var_list = []  #database
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
        print (ex_var_list)
        #if current in database
        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation) # os elblawy
            item_id = id[index]
            # return HttpResponse('True')
            #increase quatitiy
            item = CartItem.objects.get(product = product , id = item_id )
            item.quantatity +=1
            item.save()
        else:
            # return HttpResponse('False')
            #ceate new item
            item = CartItem.objects.create(product= product, cart = cart, quantatity=1) 
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)       
        # cart_item.quantatity +=1
        item.save()
    else: 
        cart_item= CartItem.objects.create( 
            product = product,
            cart = cart,
            quantatity = 1,)
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    
    # return HttpResponse(cart_item.product)
    # exit()
    return redirect ('cart')

#     الكارت نفسه
#     =
#     فيه الكارت والكارت ايتمس
#     كارت id
#     فلتر الاكتيف والالكارت فورين كي
#     بعد ين  LOOP عليهم
# بارامترات توتال  - الكمية 

# علامة الناقص
def remove_cart (request , product_id , cart_item_id):
    cart      = Cart.objects.get(cart_id=_cart_id(request))
    product   = Product.objects.get(id= product_id)
    try:
        cart_item = CartItem.objects.get(product = product , cart = cart , id = cart_item_id)
    
        if cart_item.quantatity > 1:
            cart_item.quantatity-=1
            cart_item.save()
        else:
            cart.delete()
    except:
        pass    
    return redirect ('cart')

 # الكارت كله اللي بيعمل LOOP

# مسح المنتجات
def remove_cart_item(request , product_id , cart_item_id): # نقٌص منتج
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product , id = product_id)
    cart_item = CartItem.objects.get(product= product , cart = cart , id = cart_item_id)
    cart_item.delete()
    return redirect ('cart')

# كمية، توتإل ، إلكإرت فقط ، جرإند توتإل ، شحن 
def cart (request , total =0 , quantatity = 0 , cart_items = None):
    try:
        tax         = 0
        grand_total = 0
        cart        = Cart.objects.get(cart_id = _cart_id(request))
        cart_items  = CartItem.objects.filter(cart = cart , is_active= True)
        for cart_item in cart_items:
            total      +=  (cart_item.product.price * cart_item.quantatity)
            quantatity +=  cart_item.quantatity
        tax = (2* total) /100
        grand_total = tax + total   
    except ObjectDoesNotExist:
        pass

    context = {'total': total, 'quantatity':quantatity , 'cart_items':cart_items , 'grand_total': grand_total , 'tax': tax  }    
    return render(request , 'store/cart.html' , context)

    # __iexact
    # يتم استخدام البحث الدقيق للحصول على سجلات ذات قيمة محددة. لإجراء بحث حساس لحالة الأحرف، استخدم البحث الدقيق.
    # __iexact => is a Filter للبحث الدقيق وبحساسية الحروف، ب