from django.shortcuts import render 
from store.models import Product

def home (request):
    products =  Product.objects.all().filter(is_available= True)
    context ={'products':products}
    return render (request, 'home.html', context)

    # cd venv
    # Scripts\activate
    # cd ..
    # cd greatkart
    # python manage.py runserver