from .utils import get_cart

def cart_context(request):
    """
    Context processor that adds cart information to all templates.
    """
    cart = get_cart(request.session)
    total_quantity = cart.get_total_quantity()
    
    return {
        'cart_quantity': total_quantity,
    } 