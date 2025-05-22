from django.contrib import admin
from .models import Category, Product, ProductVariant, Brand
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
    prepopulated_fields = {'slug': ['name']}
    list_display = ('name', 'slug')

admin.site.register(Category, CategoryAdmin) 


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    list_display = ('name', 'slug')

admin.site.register(Product, ProductAdmin) 


class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'stock','flavor', 'size', 'is_active')
    list_editable = ('is_active',)
admin.site.register(ProductVariant, ProductVariantAdmin)


class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    list_display = ('name', 'slug', 'is_active')
    list_editable = ('is_active',)

admin.site.register(Brand, BrandAdmin)