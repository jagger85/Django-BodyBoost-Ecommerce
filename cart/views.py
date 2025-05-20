from django.shortcuts import render, get_object_or_404
from django.views import View
from store.models import Product
from .models import Cart
from .services import CartService
from django.http import HttpResponse


def _cart_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def get_or_create_cart(request):
    cart_id = _cart_id(request)
    cart, _ = Cart.objects.get_or_create(cart_id=cart_id)
    return cart

def get_cart_quantity(request):
    """View to return the current cart quantity for HTMX requests"""
    cart_service = CartService(request.session)
    quantity = cart_service.get_total_quantity()
    response = HttpResponse(str(quantity))
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

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
        
        response = render(request, 'cart/partials/cart_update.html', context)
        response['HX-Trigger'] = 'cartUpdate'
        return response
    
    def delete(self, request, product_id):
        cart_service = CartService(request.session)
        cart_service.clear_item(product_id)
        
        cart_details = cart_service.get_cart_details()
        
        # If it was the last item, return an empty response with HX-Redirect
        if cart_service.get_total_quantity() == 0:
            response = HttpResponse('')
            response['HX-Redirect'] = '/cart/'
            return response
            
        context = {
            'total': cart_details['total'],
            'tax': cart_details['tax'],
            'grand_total': cart_details['grand_total'],
            'total_quantity': cart_details['quantity']
        }
        
        response = render(request, 'cart/partials/cart_totals.html', context)
        response['HX-Trigger'] = 'cartUpdate'
        return response

