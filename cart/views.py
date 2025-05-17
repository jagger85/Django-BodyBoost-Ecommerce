from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from .services import CartService


def _cart_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def get_or_create_cart(request):
    cart_id = _cart_id(request)
    cart, _ = Cart.objects.get_or_create(cart_id=cart_id)
    return cart


def add_to_cart(request, product_id):
    cart_service = CartService(request.session)
    cart_service.add_item(product_id)
    return redirect('/cart/')


def remove_from_cart(request, product_id):
    cart_service = CartService(request.session)
    cart_service.remove_item(product_id)
    return redirect('/cart/')


def remove_all_itemcart_products(request, product_id):
    cart_service = CartService(request.session)
    cart_service.clear_item(product_id)
    return redirect('/cart/')


def cart(request):
    cart_service = CartService(request.session)
    context = cart_service.get_cart_details()
    return render(request, 'cart/cart.html', context)    

