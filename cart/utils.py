from django.contrib.sessions.backends.base import SessionBase
from .services import CartService

def get_cart(session: SessionBase) -> CartService:
    return CartService(session)