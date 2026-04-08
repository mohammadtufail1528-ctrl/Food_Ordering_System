"""
Orders App Views
- Cart: Add, Update, Remove items
- Checkout: Place order
- Order History: View past orders
- Order Detail: Single order detail
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from apps.menu.models import FoodItem
from .models import Cart, CartItem, Order, OrderItem


# ─── Helper: Get or Create Cart ──────────────────────────────────────────────
def get_or_create_cart(request):
    """Get cart for logged-in user or session user"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        # Session-based cart for guests
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart


# ─── Cart Views ───────────────────────────────────────────────────────────────
def cart_view(request):
    """Display the shopping cart"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('food_item').all()

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'page_title': 'Your Cart - Foodie',
    }
    return render(request, 'orders/cart.html', context)


@require_POST
def add_to_cart(request, food_id):
    """Add item to cart (supports AJAX)"""
    food = get_object_or_404(FoodItem, id=food_id, is_available=True)
    cart = get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        food_item=food,
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        action = 'updated'
    else:
        action = 'added'

    # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'action': action,
            'item_qty': cart_item.quantity,
            'cart_total': cart.total_items,
            'message': f'{food.name} added to cart!',
        })

    messages.success(request, f'✅ {food.name} added to cart!')
    return redirect('menu:menu')


@require_POST
def update_cart(request, item_id):
    """Update quantity of cart item"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))

    if quantity < 1:
        cart_item.delete()
        messages.info(request, 'Item removed from cart.')
    else:
        cart_item.quantity = quantity
        cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = cart_item.cart
        return JsonResponse({
            'success': True,
            'item_total': float(cart_item.item_total),
            'cart_subtotal': float(cart.subtotal),
            'cart_total': float(cart.grand_total),
            'cart_count': cart.total_items,
        })

    return redirect('orders:cart')


@require_POST
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    food_name = cart_item.food_item.name
    cart_item.delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = get_or_create_cart(request)
        return JsonResponse({
            'success': True,
            'cart_subtotal': float(cart.subtotal),
            'cart_total': float(cart.grand_total),
            'cart_count': cart.total_items,
        })

    messages.info(request, f'{food_name} removed from cart.')
    return redirect('orders:cart')


# ─── Checkout & Order Placement ──────────────────────────────────────────────
@login_required
def checkout(request):
    """Checkout page - collect delivery info and place order"""
    cart = get_or_create_cart(request)

    if cart.total_items == 0:
        messages.warning(request, '⚠️ Your cart is empty! Add some items first.')
        return redirect('menu:menu')

    if request.method == 'POST':
        # Collect form data
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        payment_method = request.POST.get('payment_method', 'cod')
        special_instructions = request.POST.get('special_instructions', '').strip()

        # Basic validation
        if not all([full_name, phone, address, city, state, pincode]):
            messages.error(request, '❌ Please fill in all required fields.')
            return redirect('orders:checkout')

        # Create Order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            email=email or request.user.email,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            payment_method=payment_method,
            special_instructions=special_instructions,
            subtotal=cart.subtotal,
            delivery_charge=cart.delivery_charge,
            grand_total=cart.grand_total,
            status='confirmed' if payment_method == 'cod' else 'pending',
        )

        # Create OrderItems from CartItems
        for cart_item in cart.items.select_related('food_item'):
            OrderItem.objects.create(
                order=order,
                food_item=cart_item.food_item,
                food_name=cart_item.food_item.name,
                food_image=cart_item.food_item.get_image,
                quantity=cart_item.quantity,
                price=cart_item.food_item.display_price,
            )

        # Clear the cart after order
        cart.items.all().delete()

        messages.success(request, f'🎉 Order #{order.order_number} placed successfully!')
        return redirect('orders:order_success', order_number=order.order_number)

    # GET: Show checkout form
    cart_items = cart.items.select_related('food_item')
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'user': request.user,
        'page_title': 'Checkout - Foodie',
    }
    return render(request, 'orders/checkout.html', context)


def order_success(request, order_number):
    """Order success confirmation page"""
    order = get_object_or_404(Order, order_number=order_number)
    context = {
        'order': order,
        'page_title': f'Order Confirmed - #{order.order_number}',
    }
    return render(request, 'orders/order_success.html', context)


@login_required
def order_history(request):
    """View all past orders for the logged-in user"""
    orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')
    context = {
        'orders': orders,
        'page_title': 'My Orders - Foodie',
    }
    return render(request, 'orders/order_history.html', context)


@login_required
def order_detail(request, order_number):
    """View details of a single order"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    context = {
        'order': order,
        'page_title': f'Order #{order.order_number} - Foodie',
    }
    return render(request, 'orders/order_detail.html', context)
