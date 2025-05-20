from django.contrib.sessions.backends.base import SessionBase
from typing import Optional, Dict, Any
from .models import Cart, CartItem
from store.models import Product
from django.shortcuts import get_object_or_404

class CartService:
    def __init__(self, session: SessionBase):
        """
        Initialize cart service with a session object instead of request
        This makes it more flexible as we only need the session, not the entire request
        """
        self.session = session
        self.cart = self._get_or_create_cart()

    def _get_cart_id(self) -> str:
        if not self.session.session_key:
            self.session.create()
        return self.session.session_key

    def _get_or_create_cart(self) -> Cart:
        cart_id = self._get_cart_id()
        cart, _ = Cart.objects.get_or_create(cart_id=cart_id)
        return cart

    @property
    def items(self):
        """Get all active items in the cart"""
        return CartItem.objects.filter(cart=self.cart, is_active=True)

    def get_cart_details(self) -> Dict[str, Any]:
        """Get complete cart information including totals"""
        cart_items = self.items
        total = sum(item.product.price * item.quantity for item in cart_items)
        quantity = sum(item.quantity for item in cart_items)
        tax = (21 * total) / 100
        grand_total = total + tax

        return {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'tax': tax,
            'grand_total': grand_total
        }

    def add_item(self, product_id: int, quantity: int = 1) -> CartItem:
        """Add an item to cart or increase its quantity"""
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            cart=self.cart,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return cart_item

    def remove_item(self, product_id: int, quantity: int = 1) -> None:
        """Remove specified quantity of an item from cart"""
        product = get_object_or_404(Product, id=product_id)
        try:
            cart_item = CartItem.objects.get(product=product, cart=self.cart)
            cart_item.quantity -= quantity
            if cart_item.quantity > 0:
                cart_item.save()
            else:
                cart_item.delete()
        except CartItem.DoesNotExist:
            pass

    def clear_item(self, product_id: int) -> None:
        """Remove all quantities of an item from cart"""
        product = get_object_or_404(Product, id=product_id)
        CartItem.objects.filter(product=product, cart=self.cart).delete()

    def has_product(self, product_id: int) -> bool:
        """
        Check if a specific product exists in the cart
        Returns True if the product is in the cart, False otherwise
        """
        return CartItem.objects.filter(
            cart=self.cart,
            product_id=product_id,
            is_active=True
        ).exists()

    def get_item_quantity(self, product_id: int) -> int:
        """
        Get the quantity of a specific product in the cart
        Returns 0 if the product is not in the cart
        """
        try:
            cart_item = CartItem.objects.get(
                cart=self.cart,
                product_id=product_id,
                is_active=True
            )
            return cart_item.quantity
        except CartItem.DoesNotExist:
            return 0
        
    def get_total_quantity(self) -> int:
        """"
        Get the total cart products quantity
        """
        return sum(item.quantity for item in self.items)
        