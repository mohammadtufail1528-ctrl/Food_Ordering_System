"""
Management command to populate Foodie with sample data
Run: python manage.py populate_data
"""

from django.core.management.base import BaseCommand
from apps.menu.models import Category, FoodItem


CATEGORIES = [
    {'name': 'Burgers',   'icon': '🍔', 'slug': 'burgers'},
    {'name': 'Pizza',     'icon': '🍕', 'slug': 'pizza'},
    {'name': 'Biryani',   'icon': '🍛', 'slug': 'biryani'},
    {'name': 'Pasta',     'icon': '🍝', 'slug': 'pasta'},
    {'name': 'Salads',    'icon': '🥗', 'slug': 'salads'},
    {'name': 'Desserts',  'icon': '🍰', 'slug': 'desserts'},
    {'name': 'Beverages', 'icon': '🥤', 'slug': 'beverages'},
    {'name': 'Sushi',     'icon': '🍱', 'slug': 'sushi'},
]

FOOD_ITEMS = [
    # ── Burgers ──
    {
        'name': 'Classic Smash Burger',
        'category': 'burgers',
        'description': 'Two smash-style beef patties, American cheese, special sauce, pickles, and caramelized onions on a toasted brioche bun.',
        'short_description': 'Double smash patty with signature sauce',
        'price': 299, 'discounted_price': 249,
        'image_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&q=80',
        'spice_level': 'mild', 'prep_time': 15, 'calories': 650,
        'is_veg': False, 'is_featured': True, 'is_bestseller': True,
        'rating': 4.8, 'total_reviews': 312,
    },
    {
        'name': 'Crispy Chicken Burger',
        'category': 'burgers',
        'description': 'Crispy fried chicken thigh, coleslaw, pickled jalapeños, and honey mustard sauce on a sesame brioche bun.',
        'short_description': 'Southern-style crispy fried chicken',
        'price': 279,
        'image_url': 'https://images.unsplash.com/photo-1606755962773-d324e0a13086?w=500&q=80',
        'spice_level': 'medium', 'prep_time': 18, 'calories': 580,
        'is_veg': False, 'is_featured': True, 'is_bestseller': True,
        'rating': 4.6, 'total_reviews': 245,
    },
    {
        'name': 'Veggie Avocado Burger',
        'category': 'burgers',
        'description': 'Black bean patty, fresh avocado, tomato, lettuce, and chipotle mayo on a whole wheat bun.',
        'short_description': 'Plant-based delight with avocado',
        'price': 249,
        'image_url': 'https://images.unsplash.com/photo-1550547660-d9450f859349?w=500&q=80',
        'spice_level': 'mild', 'prep_time': 12, 'calories': 420,
        'is_veg': True, 'is_featured': False, 'is_new': True,
        'rating': 4.4, 'total_reviews': 98,
    },

    # ── Pizza ──
    {
        'name': 'Margherita Classica',
        'category': 'pizza',
        'description': 'San Marzano tomato sauce, fresh mozzarella di bufala, basil, and extra virgin olive oil on a hand-tossed crust.',
        'short_description': 'The timeless Italian classic',
        'price': 349, 'discounted_price': 299,
        'image_url': 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=500&q=80',
        'spice_level': 'mild', 'prep_time': 20, 'calories': 720,
        'is_veg': True, 'is_featured': True, 'is_bestseller': True,
        'rating': 4.9, 'total_reviews': 521,
    },
    {
        'name': 'BBQ Chicken Pizza',
        'category': 'pizza',
        'description': 'Smoky BBQ sauce, grilled chicken, red onions, bell peppers, mozzarella, and fresh cilantro.',
        'short_description': 'Smoky BBQ with grilled chicken',
        'price': 399,
        'image_url': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=500&q=80',
        'spice_level': 'medium', 'prep_time': 22, 'calories': 890,
        'is_veg': False, 'is_featured': True,
        'rating': 4.7, 'total_reviews': 389,
    },
    {
        'name': 'Spicy Pepperoni',
        'category': 'pizza',
        'description': 'Generous pepperoni, spicy salami, jalapeños, crushed red pepper flakes, and double mozzarella.',
        'short_description': 'Extra hot pepperoni fiesta',
        'price': 379,
        'image_url': 'https://images.unsplash.com/photo-1528137871618-79d2761e3fd5?w=500&q=80',
        'spice_level': 'hot', 'prep_time': 20, 'calories': 950,
        'is_veg': False, 'is_bestseller': True,
        'rating': 4.5, 'total_reviews': 287,
    },

    # ── Biryani ──
    {
        'name': 'Hyderabadi Dum Biryani',
        'category': 'biryani',
        'description': 'Authentic Hyderabadi-style biryani with marinated mutton, fragrant basmati, saffron, caramelized onions, and whole spices. Slow-cooked in dum.',
        'short_description': 'Authentic dum-cooked Hyderabadi style',
        'price': 349,
        'image_url': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=500&q=80',
        'spice_level': 'medium', 'prep_time': 45, 'calories': 780,
        'is_veg': False, 'is_featured': True, 'is_bestseller': True,
        'rating': 4.9, 'total_reviews': 628,
    },
    {
        'name': 'Vegetable Dum Biryani',
        'category': 'biryani',
        'description': 'Fragrant basmati rice layered with mixed vegetables, paneer, saffron, and aromatic spices. A vegetarian delight.',
        'short_description': 'Aromatic veg biryani with paneer',
        'price': 249,
        'image_url': 'https://images.unsplash.com/photo-1631515243349-e0cb75fb8d3a?w=500&q=80',
        'spice_level': 'medium', 'prep_time': 40, 'calories': 620,
        'is_veg': True, 'is_featured': True,
        'rating': 4.6, 'total_reviews': 312,
    },
    {
        'name': 'Chicken Tikka Biryani',
        'category': 'biryani',
        'description': 'Tandoor-smoked chicken tikka layered in saffron basmati with mint raita and mirchi ka salan.',
        'short_description': 'Tandoor-smoked chicken tikka style',
        'price': 319,
        'image_url': 'https://images.unsplash.com/photo-1552611052-33e04de081de?w=500&q=80',
        'spice_level': 'hot', 'prep_time': 40, 'calories': 820,
        'is_veg': False, 'is_new': True,
        'rating': 4.7, 'total_reviews': 198,
    },

    # ── Pasta ──
    {
        'name': 'Spaghetti Carbonara',
        'category': 'pasta',
        'description': 'Authentic Roman-style with guanciale, egg yolks, Pecorino Romano, and black pepper. No cream!',
        'short_description': 'Authentic Roman egg and guanciale pasta',
        'price': 299,
        'image_url': 'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=500&q=80',
        'spice_level': 'mild', 'prep_time': 20, 'calories': 680,
        'is_veg': False, 'is_featured': True,
        'rating': 4.7, 'total_reviews': 203,
    },
    {
        'name': 'Penne Arrabbiata',
        'category': 'pasta',
        'description': 'Spicy San Marzano tomatoes, garlic, red chilli flakes, and fresh basil. A simple Italian classic.',
        'short_description': 'Spicy tomato and garlic pasta',
        'price': 249,
        'image_url': 'https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=500&q=80',
        'spice_level': 'hot', 'prep_time': 18, 'calories': 520,
        'is_veg': True, 'is_new': True,
        'rating': 4.4, 'total_reviews': 134,
    },

    # ── Desserts ──
    {
        'name': 'Belgian Chocolate Lava Cake',
        'category': 'desserts',
        'description': 'Warm chocolate fondant with a molten Belgian chocolate center, served with vanilla bean ice cream.',
        'short_description': 'Molten chocolate center with ice cream',
        'price': 199,
        'image_url': 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=500&q=80',
        'spice_level': 'mild', 'prep_time': 12, 'calories': 480,
        'is_veg': True, 'is_featured': True, 'is_bestseller': True,
        'rating': 4.8, 'total_reviews': 445,
    },
    {
        'name': 'Mango Kulfi',
        'category': 'desserts',
        'description': 'Creamy Indian ice cream made with condensed milk, real Alphonso mangoes, and pistachio.',
        'short_description': 'Creamy Alphonso mango kulfi',
        'price': 129,
        'image_url': 'https://images.unsplash.com/photo-1501443762994-82bd5dace89a?w=500&q=80',
        'spice_level': 'mild', 'prep_time': 5, 'calories': 280,
        'is_veg': True, 'is_new': True,
        'rating': 4.6, 'total_reviews': 189,
    },

    # ── Beverages ──
    {
        'name': 'Mango Lassi',
        'category': 'beverages',
        'description': 'Thick and creamy yogurt blended with fresh Alphonso mango pulp, cardamom, and a hint of saffron.',
        'short_description': 'Thick Alphonso mango yogurt drink',
        'price': 99,
        'image_url': 'https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=500&q=80',
        'spice_level': 'mild', 'prep_time': 5, 'calories': 220,
        'is_veg': True, 'is_featured': False,
        'rating': 4.7, 'total_reviews': 267,
    },

    # ── Salads ──
    {
        'name': 'Greek Salad',
        'category': 'salads',
        'description': 'Crisp cucumbers, ripe tomatoes, Kalamata olives, red onions, and creamy feta with oregano dressing.',
        'short_description': 'Fresh Mediterranean salad with feta',
        'price': 199,
        'image_url': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=500&q=80',
        'spice_level': 'mild', 'prep_time': 8, 'calories': 280,
        'is_veg': True, 'is_new': True,
        'rating': 4.3, 'total_reviews': 87,
    },
]


class Command(BaseCommand):
    help = 'Populate database with sample food data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🍔 Populating Foodie database...\n')

        # Create categories
        cat_map = {}
        for cat_data in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name'], 'icon': cat_data['icon']},
            )
            cat_map[cat_data['slug']] = cat
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  {cat_data["icon"]} [{status}] Category: {cat.name}')

        # Create food items
        for item_data in FOOD_ITEMS:
            cat_slug = item_data.pop('category')
            category = cat_map.get(cat_slug)

            food, created = FoodItem.objects.get_or_create(
                name=item_data['name'],
                defaults={**item_data, 'category': category},
            )
            status = '✅ Created' if created else '⏭  Exists'
            self.stdout.write(f'  {status}: {food.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\n🎉 Done! {FoodItem.objects.count()} food items across {Category.objects.count()} categories.'
        ))
