from django.contrib.sessions.backends.base import SessionBase
from typing import Optional, Dict, Any
from .models import Cart, CartItem
from store.models import ProductVariant
from django.shortcuts import get_object_or_404
from django.db.models import Q

class CartService:
    def __init__(self, session: SessionBase):
        """
        Initialize cart service with a session object
        """
        self.session = session
        self.cart = self._get_or_create_cart()
        # Get user from session if available
        self.user = getattr(session, 'user', None)
        if hasattr(self.user, 'is_authenticated') and not self.user.is_authenticated:
            self.user = None

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

    def get_cart_details(self, request) -> Dict[str, Any]:
        """Get complete cart information including totals"""
        if request.user.is_authenticated:
            # Get items that either belong to the current cart OR are associated with the user
            cart_items = CartItem.objects.filter(
                Q(cart=self.cart) | Q(user=request.user),
                is_active=True
            ).distinct()
        else:
            cart_items = self.items
        
        total = sum(item.product.price * item.quantity for item in cart_items)
        quantity = sum(item.quantity for item in cart_items)
        tax = (21 * total) / 100
        grand_total = total + tax

        return {
            'total': total,
            'total_items_in_cart': quantity,
            'cart_items': cart_items,
            'tax': tax,
            'grand_total': grand_total
        }

    def add_item(self, variant_id: int, quantity: int = 1) -> CartItem:
        """Add a variant to cart or increase its quantity"""
        variant = get_object_or_404(ProductVariant, id=variant_id)
        cart_item, created = CartItem.objects.get_or_create(
            product=variant,
            cart=self.cart,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return cart_item

    def remove_item(self, variant_id: int, quantity: int = 1) -> None:
        """Remove specified quantity of a variant from cart"""
        variant = get_object_or_404(ProductVariant, id=variant_id)
        try:
            cart_item = CartItem.objects.get(product=variant, cart=self.cart)
            cart_item.quantity -= quantity
            if cart_item.quantity > 0:
                cart_item.save()
            else:
                cart_item.delete()
        except CartItem.DoesNotExist:
            pass

    def clear_item(self, variant_id: int) -> None:
        """Remove all quantities of a variant from cart"""
        variant = get_object_or_404(ProductVariant, id=variant_id)
        CartItem.objects.filter(product=variant, cart=self.cart).delete()

    def has_product(self, variant_id: int) -> bool:
        """
        Check if a specific variant exists in the cart
        Returns True if the variant is in the cart, False otherwise
        """
        return CartItem.objects.filter(
            cart=self.cart,
            product_id=variant_id,
            is_active=True
        ).exists()

    def get_item_quantity(self, variant_id: int) -> int:
        """
        Get the quantity of a specific variant in the cart
        Returns 0 if the variant is not in the cart
        """
        try:
            cart_item = CartItem.objects.get(
                cart=self.cart,
                product_id=variant_id,
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
        