from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.

class Product (models.Model):
    product_name  = models.CharField(max_length= 200, unique = True)
    slug          = models.SlugField (max_length= 200 , unique= True)
    description   = models.TextField(max_length = 500 , blank = True)
    price         = models.IntegerField()
    product_image = models.ImageField(upload_to='photos/products', blank = True )
    stock         = models.IntegerField()
    is_available  = models.BooleanField(default = True)
    category      = models.ForeignKey(Category, on_delete = models.CASCADE )
    created_date  = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)


    def get_url (self):
        return reverse('product_detail' , args= [self.category.slug , self.slug])

    def __str__ (self):
        return self.product_name

    
    # class ProductAdmin(admin.ModelAdmin):
    #     prepopulated_fields = {'slug':('product_name',)}
    #     list_display = ()
    #     list_display_links =('','',)
    #     readonly_fields=()
    #     ordering = ('-')
    #     list_filter=()
    #     filter_horizontal = ()
    #     fieldsets = ()