"""
Menu App Views
- Home page with featured items & categories
- Menu page with filter & search
- Food detail page
"""

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import FoodItem, Category


def home(request):
    """
    Home page - Featured food, categories, bestsellers
    """
    categories = Category.objects.filter(is_active=True)
    featured_items = FoodItem.objects.filter(is_featured=True, is_available=True)[:8]
    bestsellers = FoodItem.objects.filter(is_bestseller=True, is_available=True)[:6]
    new_items = FoodItem.objects.filter(is_new=True, is_available=True)[:4]

    context = {
        'categories': categories,
        'featured_items': featured_items,
        'bestsellers': bestsellers,
        'new_items': new_items,
        'page_title': 'Foodie - Order Delicious Food Online',
    }
    return render(request, 'menu/home.html', context)


def menu(request):
    """
    Menu page - All items with category filter and search
    """
    categories = Category.objects.filter(is_active=True)
    food_items = FoodItem.objects.filter(is_available=True).select_related('category')

    # ── Category Filter ─────────────────────────────────────
    category_slug = request.GET.get('category', '')
    if category_slug:
        food_items = food_items.filter(category__slug=category_slug)

    # ── Search ───────────────────────────────────────────────
    query = request.GET.get('q', '')
    if query:
        food_items = food_items.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    # ── Veg / Non-Veg Filter ─────────────────────────────────
    veg_filter = request.GET.get('veg', '')
    if veg_filter == 'veg':
        food_items = food_items.filter(is_veg=True)
    elif veg_filter == 'nonveg':
        food_items = food_items.filter(is_veg=False)

    # ── Sort ─────────────────────────────────────────────────
    sort_by = request.GET.get('sort', '')
    sort_options = {
        'price_low': 'price',
        'price_high': '-price',
        'rating': '-rating',
        'newest': '-created_at',
        'popular': '-total_reviews',
    }
    if sort_by in sort_options:
        food_items = food_items.order_by(sort_options[sort_by])

    # Get currently selected category object
    selected_category = None
    if category_slug:
        selected_category = Category.objects.filter(slug=category_slug).first()

    context = {
        'categories': categories,
        'food_items': food_items,
        'selected_category': selected_category,
        'category_slug': category_slug,
        'query': query,
        'veg_filter': veg_filter,
        'sort_by': sort_by,
        'total_count': food_items.count(),
        'page_title': 'Menu - Foodie',
    }
    return render(request, 'menu/menu.html', context)


def food_detail(request, slug):
    """
    Food detail page - Full info + related items
    """
    food = get_object_or_404(FoodItem, slug=slug, is_available=True)

    # Related items from same category
    related_items = FoodItem.objects.filter(
        category=food.category,
        is_available=True
    ).exclude(id=food.id)[:4]

    context = {
        'food': food,
        'related_items': related_items,
        'page_title': f'{food.name} - Foodie',
    }
    return render(request, 'menu/food_detail.html', context)
