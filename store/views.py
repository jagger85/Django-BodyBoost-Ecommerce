from django.shortcuts import render, get_object_or_404
from .models import Product, Category, ProductVariant
from django.views import View
from cart.utils import get_cart
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def cart(request):
    cart = get_cart(request.session)
    context = cart.get_cart_details(request)
    return render(request, 'store/cart.html', context)


def store(request, category_slug=None):
    # Fetch categories
    categories = get_object_or_404(Category, slug=category_slug) if category_slug else Category.objects.all()
    
    # Fetch all product variants based on category
    products = ProductVariant.objects.filter(product__category=categories) if category_slug else ProductVariant.objects.all()
    
    # Pagination
    paginator = Paginator(products, 1)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'variants' : paged_products,
        'categories': categories,
        'products_count': products.count()
    }

    return render(request, 'store/store.html', context)

def search(request):
    products = ProductVariant.objects.all()
    keyword = request.GET.get('keyword', '')
    
    if keyword:
        products = ProductVariant.objects.filter(
            Q(product__description__icontains=keyword) |
            Q(product__name__icontains=keyword)
        )
    
    paginator = Paginator(products, 1)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    
    context = {
        'variants': paged_products,
        'products_count': products.count(),
        'keyword': keyword,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug, variant_id=None):
    product = get_object_or_404(Product, slug=product_slug)
    # Get the specified variant or the first variant for initial display
    if variant_id:
        initial_variant = get_object_or_404(product.variant, id=variant_id)
    else:
        initial_variant = product.variant.first()
    
    context = {
        'product': product,
        'variant': initial_variant,
    }
    return render(request, 'store/product_detail.html', context)


@login_required(login_url = 'auth:login')
def dashboard(request):
    return render(request, 'store/dashboard.html')