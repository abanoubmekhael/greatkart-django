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



# class manage function of choices
class VariationManager (models.Manager):
    def colors (self):
        return super (VariationManager , self).filter(variation_category= 'color', is_active = True)

    def sizes(self):
        return super (VariationManager , self).filter(variation_category = 'size', is_active = True)

# choices
variation_category_choice = (
    ('color', 'color'),
    ('size' , 'size'),
    )

class Variation(models.Model):
    product            = models.ForeignKey(Product , on_delete = models.CASCADE)    
    variation_category = models.CharField(max_length=100 , choices = variation_category_choice)
    variation_value    = models.CharField(max_length=100)
    is_active          = models.BooleanField(default = True)
    created_date       = models.DateTimeField(auto_now_add = True)
    objects            = VariationManager()

    def __str__(self):
        return self.variation_value






    # class ProductAdmin(admin.ModelAdmin):
    #     prepopulated_fields = {'slug':('product_name',)}
    #     list_display = ()
    #     list_display_links =('','',)
    #     readonly_fields=()
    #     ordering = ('-')
    #     list_filter=()
    #     filter_horizontal = ()
    #     fieldsets = ()

    # __str__ versus __unicode__
    # In 3.0, str contains characters, so the same methods are named __bytes__() and __str__(). These behave as expected.