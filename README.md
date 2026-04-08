# 🍔 Foodie — Django Food Ordering Website
### Zomato/Swiggy-inspired | Bootstrap 5 | SQLite | Python/Django

---

## 📁 Project Structure

```
foodie_project/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── foodie/                        # Django project config
│   ├── settings.py                # All settings, Jazzmin theme
│   ├── urls.py                    # Root URL config
│   └── wsgi.py
│
├── apps/
│   ├── menu/                      # 🍕 Food items & categories
│   │   ├── models.py              # Category, FoodItem
│   │   ├── views.py               # Home, Menu, Food Detail
│   │   ├── urls.py
│   │   ├── admin.py               # Advanced admin config
│   │   └── management/commands/
│   │       └── populate_data.py   # Sample data loader
│   │
│   ├── orders/                    # 🛒 Cart, Checkout, Orders
│   │   ├── models.py              # Cart, CartItem, Order, OrderItem
│   │   ├── views.py               # Cart CRUD, Checkout, History
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── context_processors.py # Cart count in navbar
│   │
│   └── users/                     # 👤 Auth
│       ├── views.py               # Signup, Login, Logout, Profile
│       └── urls.py
│
├── templates/
│   ├── base.html                  # Master layout (navbar + footer)
│   ├── partials/
│   │   └── food_card.html         # Reusable card component
│   ├── menu/
│   │   ├── home.html              # Hero + Featured + Categories
│   │   ├── menu.html              # Full menu with filters
│   │   └── food_detail.html       # Single food detail
│   ├── orders/
│   │   ├── cart.html              # Cart with AJAX updates
│   │   ├── checkout.html          # Checkout form
│   │   ├── order_success.html     # Confirmation page
│   │   ├── order_history.html     # All past orders
│   │   └── order_detail.html      # Single order detail
│   └── users/
│       ├── login.html
│       ├── signup.html
│       └── profile.html
│
└── static/
    ├── css/style.css              # Full custom CSS (1000+ lines)
    └── js/main.js                 # AJAX cart, animations, toasts
```

---

## 🚀 Setup Instructions (Step-by-Step)

### Step 1 — Prerequisites
Make sure you have Python 3.10+ installed:
```bash
python --version
```

### Step 2 — Create Virtual Environment
```bash
cd foodie_project
python -m venv venv

# Activate:
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- **Django 4.2** — Web framework
- **Pillow** — Image upload support
- **django-jazzmin** — Beautiful admin theme

### Step 4 — Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5 — Populate Sample Data
```bash
python manage.py populate_data
```
This adds 8 categories and 16 food items automatically!

### Step 6 — Create Admin Superuser
```bash
python manage.py createsuperuser
```
Enter username, email, and password when prompted.

### Step 7 — Collect Static Files (optional in dev)
```bash
python manage.py collectstatic
```

### Step 8 — Run the Server
```bash
python manage.py runserver
```

### Step 9 — Visit the Site 🎉
| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000/ | Home Page |
| http://127.0.0.1:8000/menu/ | Full Menu |
| http://127.0.0.1:8000/orders/cart/ | Shopping Cart |
| http://127.0.0.1:8000/users/login/ | Login |
| http://127.0.0.1:8000/users/signup/ | Signup |
| http://127.0.0.1:8000/admin/ | Admin Dashboard |

---

## ✨ Features

| Feature | Implementation |
|---------|----------------|
| 🏠 Home Page | Hero, categories, featured, bestsellers |
| 🍕 Menu Page | Category filter, veg/non-veg, sort, search |
| 🍔 Food Detail | Full info, related items, qty selector |
| 🛒 Cart | AJAX add/remove/update, live total |
| 💳 Checkout | Multi-step form, payment methods |
| ✅ Order Success | Animated confirmation + timeline |
| 📦 Order History | All past orders with status |
| 🔐 Auth | Signup, Login, Logout, Profile |
| 👨‍💼 Admin | Jazzmin-themed advanced dashboard |
| 🔔 Toasts | AJAX toast notifications |
| 💫 Animations | Scroll reveal, float effects, loaders |

---

## 🎨 Tech Stack

- **Backend:** Django 4.2 (Python)
- **Database:** SQLite (default)
- **Frontend:** Bootstrap 5.3 + Custom CSS
- **Icons:** Bootstrap Icons + Font Awesome
- **Fonts:** Poppins + Playfair Display (Google Fonts)
- **Admin:** django-jazzmin with custom theme
- **Images:** Unsplash (external URLs)

---

## 📋 Adding Food Items via Admin

1. Go to `http://127.0.0.1:8000/admin/`
2. Login with your superuser credentials
3. Under **Menu** → **Food Items** → **Add Food Item**
4. Fill in name, category, price, image URL, and flags

**Quick image trick:** Use any Unsplash URL like:
```
https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&q=80
```

---

## 🔧 Customization Tips

### Change Color Theme
Edit `static/css/style.css`, update the `:root` variables:
```css
:root {
  --red:    #e63946;   /* Primary red */
  --orange: #f4a261;   /* Accent orange */
  --yellow: #f8c91e;   /* Highlight yellow */
}
```

### Add New Pages
1. Create view in relevant app's `views.py`
2. Add URL in app's `urls.py`
3. Create template in `templates/` folder

### Enable Email Notifications
Add to `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

---

## ⚡ Performance Tips

1. **Image Optimization** — Use WebP format for food images
2. **Database Indexing** — Already on slug fields via `SlugField`
3. **Caching** — Add `django.middleware.cache.FetchFromCacheMiddleware`
4. **CDN** — Serve static files via Cloudflare or AWS CloudFront in production
5. **Gunicorn** — Use `gunicorn foodie.wsgi` for production serving
6. **select_related** — Already used in views to reduce DB queries

---

## 🌐 SEO Optimization

Each page has:
- Unique `<title>` tags via `{% block title %}`
- Meta description in `base.html`
- `alt` attributes on all images
- Semantic HTML5 elements (header, nav, main, footer, section)
- Breadcrumbs on detail pages
- Mobile-first responsive design
- Fast-loading with deferred JS

---

## 🤝 Contributing / Extension Ideas

- [ ] Add product reviews & star ratings
- [ ] WhatsApp order notification
- [ ] Razorpay/Stripe payment integration
- [ ] Real-time order tracking with WebSockets
- [ ] Admin order status email alerts
- [ ] Multi-restaurant support
- [ ] Loyalty points system
- [ ] PWA (Progressive Web App) support

---

Made with ❤️ | Foodie © 2024
