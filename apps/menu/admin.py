from django.contrib import admin
from .models import Category, FoodItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discounted_price', 'is_veg',
                    'is_featured', 'is_bestseller', 'is_available', 'rating']
    list_filter = ['category', 'is_veg', 'is_featured', 'is_bestseller', 'is_available', 'spice_level']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'discounted_price', 'is_featured', 'is_bestseller', 'is_available']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'category', 'description', 'short_description')
        }),
        ('Pricing', {
            'fields': ('price', 'discounted_price')
        }),
        ('Media', {
            'fields': ('image', 'image_url')
        }),
        ('Details', {
            'fields': ('spice_level', 'prep_time', 'calories', 'serving_size', 'is_veg')
        }),
        ('Status & Flags', {
            'fields': ('is_featured', 'is_bestseller', 'is_new', 'is_available')
        }),
        ('Rating', {
            'fields': ('rating', 'total_reviews')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
