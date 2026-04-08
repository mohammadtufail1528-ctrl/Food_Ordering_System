"""
Orders App Models
- Cart: Shopping cart (session-based or user-based)
- CartItem: Individual items in cart
- Order: Placed order
- OrderItem: Items in an order
"""

from django.db import models
from django.contrib.auth.models import User
from apps.menu.models import FoodItem
from django.utils import timezone
import uuid


class Cart(models.Model):
    """Shopping cart - linked to user or session"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.item_total for item in self.items.all())

    @property
    def delivery_charge(self):
        """Free delivery above ₹499"""
        return 0 if self.subtotal >= 499 else 49

    @property
    def grand_total(self):
        return self.subtotal + self.delivery_charge

    def __str__(self):
        return f"Cart of {self.user or self.session_key}"


class CartItem(models.Model):
    """Individual item in the cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['cart', 'food_item']

    @property
    def item_total(self):
        return self.food_item.display_price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.food_item.name}"


class Order(models.Model):
    """Placed order model"""

    STATUS_CHOICES = [
        ('pending', '⏳ Pending'),
        ('confirmed', '✅ Confirmed'),
        ('preparing', '👨‍🍳 Preparing'),
        ('out_for_delivery', '🛵 Out for Delivery'),
        ('delivered', '🎉 Delivered'),
        ('cancelled', '❌ Cancelled'),
    ]

    PAYMENT_METHODS = [
        ('cod', 'Cash on Delivery'),
        ('online', 'Online Payment'),
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI'),
    ]

    # Order identification
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order_number = models.CharField(max_length=20, unique=True, blank=True)

    # User info
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')

    # Delivery address
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=49)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)

    # Status & Payment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cod')
    is_paid = models.BooleanField(default=False)

    # Special instructions
    special_instructions = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number: FD + timestamp + last 4 of UUID
            self.order_number = f"FD{timezone.now().strftime('%Y%m%d%H%M')}{str(self.order_id)[-4:].upper()}"
        super().save(*args, **kwargs)

    @property
    def status_badge_class(self):
        """Bootstrap badge color for status"""
        badges = {
            'pending': 'warning',
            'confirmed': 'info',
            'preparing': 'primary',
            'out_for_delivery': 'secondary',
            'delivered': 'success',
            'cancelled': 'danger',
        }
        return badges.get(self.status, 'secondary')

    def __str__(self):
        return f"Order #{self.order_number} - {self.full_name}"


class OrderItem(models.Model):
    """Items in a placed order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True)
    food_name = models.CharField(max_length=200)  # Store name in case food is deleted
    food_image = models.URLField(blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Price at time of order

    @property
    def item_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.food_name}"
