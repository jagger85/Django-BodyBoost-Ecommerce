from django.shortcuts import render
from store.models import Product, Category


def home(request):

    context = {
        'products': Product.objects.all().filter(is_available=True),
        'all_categories': Category.objects.all()
    }

    return render(request,'home.html', context)