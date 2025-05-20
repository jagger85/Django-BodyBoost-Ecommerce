from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from store.models import Product
from .models import Cart, CartItem
from .services import CartService
from django.http import HttpResponse
from django.http import HttpResponseRedirect


def _cart_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def get_or_create_cart(request):
    cart_id = _cart_id(request)
    cart, _ = Cart.objects.get_or_create(cart_id=cart_id)
    return cart


class CartView(View):
    def get(self, request):
        cart_service = CartService(request.session)
        context = cart_service.get_cart_details()
        return render(request, 'cart/cart.html', context)
    
    def post(self, request, product_id):
        cart_service = CartService(request.session)
        action = request.POST.get('action')
        
        if action == 'add':
            cart_service.add_item(product_id)
        elif action == 'remove':
            cart_service.remove_item(product_id)
            
        cart_details = cart_service.get_cart_details()
        product = get_object_or_404(Product, id=product_id)
        cart_item = next((item for item in cart_details['cart_items'] if item.product.id == product_id), None)
        
        context = {
            'product': product,
            'cart_item': cart_item,
            'total': cart_details['total'],
            'tax': cart_details['tax'],
            'grand_total': cart_details['grand_total'],
            'total_quantity': cart_details['quantity']
        }
        
        return render(request, 'cart/partials/cart_update.html', context)
    
    def delete(self, request, product_id):
        cart_service = CartService(request.session)
        cart_service.clear_item(product_id)
        
        # Check if this was the last item
        if cart_service.get_total_quantity() == 0:
            # If it was the last item, redirect to refresh the page
            return HttpResponseRedirect('/cart/')
            
        cart_details = cart_service.get_cart_details()
        context = {
            'total': cart_details['total'],
            'tax': cart_details['tax'],
            'grand_total': cart_details['grand_total'],
            'total_quantity': cart_details['quantity']
        }
        
        return render(request, 'cart/partials/cart_totals.html', context)


# Legacy views for non-HTMX requests
def add_to_cart(request, product_id):
    cart_service = CartService(request.session)
    cart_service.add_item(product_id)
    return redirect('cart:cart')


def remove_from_cart(request, product_id):
    cart_service = CartService(request.session)
    cart_service.remove_item(product_id)
    return redirect('cart:cart')


def remove_all_itemcart_products(request, product_id):
    cart_service = CartService(request.session)
    cart_service.clear_item(product_id)
    return redirect('cart:cart')
    
