from .utils import get_cart

def cart_context(request):
    """
    Context processor that adds cart information to all templates.
    """
    cart = get_cart(request.session).get_cart_details()
    
    return {
        'cart_total_items':         cart['total_items_in_cart'],
        'cart_total_price_amount':  cart['total'],
        'cart_tax':                 cart['tax'],
        'cart_grand_total':         cart['grand_total']
    } 