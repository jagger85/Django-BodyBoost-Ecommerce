from django.shortcuts import render, get_object_or_404
from .models import Product, Category, ProductVariant
from accounts.forms import AddressForm
from django.views import View
from cart.utils import get_cart
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from decimal import Decimal

def cart(request):
    cart = get_cart(request.session)
    context = cart.get_cart_details(request)
    return render(request, 'store/cart.html', context)

def apply_filters(queryset, filters):
    """
    Apply multiple filters to a queryset based on request parameters
    """
    if filters.get('categories'):
        # Handle multiple categories
        categories = filters['categories']
        if categories:
            queryset = queryset.filter(product__category__slug__in=categories)
    
    if filters.get('price_range'):
        try:
            price = int(filters['price_range'])
            queryset = queryset.filter(price__lte=price)
        except (ValueError, TypeError):
            pass
    
    if filters.get('brand'):
        queryset = queryset.filter(product__brand__name__iexact=filters['brand'])

    if filters.get('search'):
        queryset = queryset.filter(
            Q(product__name__icontains=filters['search']) |
            Q(product__description__icontains=filters['search'])
        )

    return queryset

def store(request, category_slug=None):
    # Initialize base queryset
    products = ProductVariant.objects.all()
    categories = Category.objects.all()
    
    # Collect all filter parameters
    filters = {
        'categories': request.GET.getlist('category'),  # Get multiple categories
        'price_range': request.GET.get('price_range'),
        'brand': request.GET.get('brand'),
        'search': request.GET.get('search'),
    }
    
    # Add category from URL if present
    if category_slug and category_slug not in filters['categories']:
        filters['categories'].append(category_slug)
    
    # Remove empty filters
    filtered_filters = {filter_key: filter_value for filter_key, filter_value in filters.items() if filter_value}
    filters = filtered_filters
    
    # Apply filters
    products = apply_filters(products, filters)
    
    # Get price range for context
    max_price = ProductVariant.objects.order_by('-price').first().price if ProductVariant.objects.exists() else 1000
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    
    context = {
        'variants': paged_products,
        'categories': categories,
        'products_count': products.count(),
        'applied_filters': filters,
        'max_price': max_price,
        'current_price_range': filters.get('price_range', max_price)
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
