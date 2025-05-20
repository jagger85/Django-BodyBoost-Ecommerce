from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.views import View
from cart.services import CartService
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def store(request, category_slug=None):
    # Fetch categories
    categories = get_object_or_404(Category, slug=category_slug) if category_slug else Category.objects.all()
    
    # Fetch products based on category
    products = Product.objects.filter(category=categories) if category_slug else Product.objects.all()
    
    # Pagination
    paginator = Paginator(products, 1)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'products' : paged_products,
        'categories': categories,
        'products_count': products.count()
    }

    return render(request, 'store/store.html', context)


class ProductDetail(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs['product_slug'])
        context = {
            'product': product
        }
        return render(request, 'store/product_detail.html', context)
    
    # sended by htmx
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs['product_slug'])
        cart = CartService(request.session)
        
        action = request.POST.get('action')
        if action == 'add':
            cart.add_item(product.id)
        elif action == 'remove':
            cart.remove_item(product.id)
            
        context = {
            'product': product,
            'total_quantity': cart.get_total_quantity()
        }
        
        # Return just the updated controls
        return render(request, 'store/partials/product_controls.html', context)