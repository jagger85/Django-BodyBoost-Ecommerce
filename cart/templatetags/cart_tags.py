from django import template
from ..utils import get_cart

register = template.Library()

@register.simple_tag(takes_context=True)
def is_in_cart(context, product_id):
    request = context['request']
    cart = get_cart(request.session)
    return cart.has_product(product_id)


@register.simple_tag(takes_context=True)
def cart_item_quantity(context, product_id):
    request = context['request']
    cart = get_cart(request.session)
    return cart.get_item_quantity(product_id)