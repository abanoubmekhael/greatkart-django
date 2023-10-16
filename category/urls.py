from django.urls import path
from .views import category
urlpatterns = [
    path('category', views.category , name = 'category'),