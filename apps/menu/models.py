"""
Menu App Models
- Category: Food categories (Pizza, Burger, etc.)
- FoodItem: Individual food items with details
"""

from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Food category model (e.g., Pizza, Burger, Sushi)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, default='🍔', help_text='Emoji icon for category')
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    """Food item model with all details"""

    SPICE_LEVELS = [
        ('mild', '🟢 Mild'),
        ('medium', '🟡 Medium'),
        ('hot', '🔴 Hot'),
        ('extra_hot', '🌶️ Extra Hot'),
    ]

    # Basic info
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='food_items')
    description = models.TextField()
    short_description = models.CharField(max_length=150, blank=True)

    # Pricing
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    # Media
    image = models.ImageField(upload_to='food_items/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text='Use URL if no uploaded image')

    # Details
    spice_level = models.CharField(max_length=20, choices=SPICE_LEVELS, default='mild')
    prep_time = models.PositiveIntegerField(default=20, help_text='Prep time in minutes')
    calories = models.PositiveIntegerField(default=0)
    serving_size = models.CharField(max_length=50, default='1 serving')

    # Flags
    is_veg = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    # Rating (can be replaced with a separate Review model)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.0)
    total_reviews = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def display_price(self):
        """Return discounted price if available, else regular price"""
        return self.discounted_price if self.discounted_price else self.price

    @property
    def discount_percent(self):
        """Calculate discount percentage"""
        if self.discounted_price and self.price > self.discounted_price:
            return int(((self.price - self.discounted_price) / self.price) * 100)
        return 0

    @property
    def get_image(self):
        """Return image URL (uploaded or external)"""
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        return '/static/images/default-food.jpg'

    def __str__(self):
        return self.name
