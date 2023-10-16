from django.shortcuts import render 
from django.http import HttpRequest

# Create your views here.


def category (request):
    return render HttpRequest ( 'Hello Category' )