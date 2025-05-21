from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    cat_image = models.ImageField(upload_to='photos/categories',blank=True)

    class Meta:
        verbose_name = 'category',
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name   

class Brand(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200)
    images = models.ImageField(upload_to='photos/brands')
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500)
    images = models.ImageField(upload_to='photos/products')
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Variant(models.Model):
    size = models.CharField(max_length=200)
    flavour = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    stock = models.IntegerField()

    def __unicode__(self):
        return self.product