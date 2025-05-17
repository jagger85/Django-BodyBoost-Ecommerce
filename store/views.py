from django.shortcuts import render, get_object_or_404
from .models import Product, Category


# Create your views here.
def store(request, category_slug=None):
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories)
    
    else:        
        categories = Category.objects.all()
        products = Product.objects.all()

    context = {
        'products' : products,
        'categories': categories,
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):

    context = {
        'product': Product.objects.get(slug=product_slug)
    }

    return render(request, 'store/product_detail.html', context)