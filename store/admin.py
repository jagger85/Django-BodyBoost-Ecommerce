from django.contrib import admin
from .models import Category, Product
from django import forms


class CategoryForm(forms.ModelForm):
    class Meta: 
        model = Category
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40})
        }

class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    prepopulated_fields = {'slug': ['category_name']}
    list_display = ('category_name', 'slug')

admin.site.register(Category, CategoryAdmin) 



class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['product_name']}
    list_display = ('product_name', 'slug')

admin.site.register(Product, ProductAdmin) 



    