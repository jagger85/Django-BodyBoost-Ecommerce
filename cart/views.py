import re
from django.shortcuts import render
from .models import Cart
from .utils import get_cart
from django.http import HttpResponse
from store.models import ProductVariant
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import AddressForm
from accounts.models import Address

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
    cart = get_cart(request.session)
    quantity = cart.get_total_quantity()
    response = HttpResponse(str(quantity))
    return response


def get_cart_variant_quantity(request, variant_id):
    """View to return the current cart variant quantity for HTMX requests"""
    cart = get_cart(request.session)    
    variant_quantity = cart.get_item_quantity(variant_id)
    response = HttpResponse(str(variant_quantity))
    return response


def add_variant(request, variant_id):
    cart = get_cart(request.session)    
    cart.add_item(variant_id)
    variant = ProductVariant.objects.get(id=variant_id)
    context = {
        'variant': variant,
    }
    response = render(request, 'store/partials/variant_control/variant_actions.html', context)
    response['HX-Trigger'] = 'cartUpdate'
    return response


def remove_variant(request, variant_id):
    cart = get_cart(request.session)    
    cart.remove_item(variant_id)
    variant = ProductVariant.objects.get(id=variant_id)

    context = {
        'variant': variant
    }
    response = render(request, 'store/partials/variant_control/variant_actions.html', context)
    response['HX-Trigger'] = 'cartUpdate'
    return response


def clear_variant(request, variant_id):
    cart = get_cart(request.session)    
    cart.clear_item(variant_id)
    variant_quantity = cart.get_item_quantity(variant_id)
    response = HttpResponse(str(variant_quantity))
    response['HX-Trigger'] = 'cartUpdate'
    return render(request,'store/cart.html', cart.get_cart_details(request))


def get_cart_view(request):
    cart = get_cart(request.session)
    context = cart.get_cart_details(request)
    return render(request, 'cart/cart.html', context)


def get_cart_totals(request):
    cart = get_cart(request.session)
    context = cart.get_cart_details(request)
    return render(request, 'cart/partials/cart_totals.html', context)

@login_required(login_url='auth:login')
def checkout(request):
    cart = get_cart(request.session).get_cart_details(request)
    form = AddressForm()
    
    context = {
        'form': form,
        'total' : cart['total'],
        'variants' : cart['cart_items'],
        'tax' : cart['tax'],
        'grand_total' : cart['grand_total'],
    }
    
    return render(request, 'cart/checkout.html' , context)

def checkout_validation(request):

    if request.method == 'POST':
        form = AddressForm(request.POST)

        if form.is_valid():
            
            address = Address.objects.create(
                name=form.cleaned_data['name'],
                street=form.cleaned_data['street'],
                post_code=form.cleaned_data['post_code'],
                city=form.cleaned_data['city'],
                province=form.cleaned_data['province'],
                country=form.cleaned_data['country'],
                order_note=form.cleaned_data['order_note'],
                user=request.user
            )
            address.save()
            messages.success(request,'Addres has been saved')


    cart = get_cart(request.session).get_cart_details(request)
    form = AddressForm()

    context = {
        'form': form,
        'total' : cart['total'],
        'variants' : cart['cart_items'],
        'tax' : cart['tax'],
        'grand_total' : cart['grand_total'],
    }
        
    return render(request, 'cart/checkout.html', context)