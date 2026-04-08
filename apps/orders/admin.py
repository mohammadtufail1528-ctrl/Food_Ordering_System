from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem



class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['item_total']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'subtotal', 'created_at']
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['item_total']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'status',
                    'payment_method', 'grand_total', 'created_at']
    list_filter = ['status', 'payment_method', 'is_paid', 'created_at']
    search_fields = ['order_number', 'full_name', 'phone', 'email']
    list_editable = ['status']
    readonly_fields = ['order_id', 'order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Info', {'fields': ('order_id', 'order_number', 'user')}),
        ('Customer Details', {'fields': ('full_name', 'phone', 'email')}),
        ('Delivery Address', {'fields': ('address', 'city', 'state', 'pincode')}),
        ('Pricing', {'fields': ('subtotal', 'delivery_charge', 'grand_total')}),
        ('Status & Payment', {'fields': ('status', 'payment_method', 'is_paid')}),
        ('Extras', {'fields': ('special_instructions', 'created_at', 'updated_at')}),
    )
