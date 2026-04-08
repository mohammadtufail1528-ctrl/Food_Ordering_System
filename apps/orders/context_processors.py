"""
Context processor to inject cart count into all templates
This makes the cart icon badge work across all pages
"""
from .models import Cart


def cart_count(request):
    """Add cart item count to every template context"""
    count = 0
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            session_key = request.session.session_key
            cart = Cart.objects.filter(session_key=session_key).first() if session_key else None

        if cart:
            count = cart.total_items
    except Exception:
        pass

    return {'cart_count': count}
