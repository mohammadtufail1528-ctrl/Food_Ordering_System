#!/bin/bash
# ═══════════════════════════════════════════════════════════
# Foodie — One-Command Setup Script
# Usage: bash setup.sh
# ═══════════════════════════════════════════════════════════

echo ""
echo "🍔  =================================="
echo "    FOODIE — Django Food Ordering App"
echo "    =================================="
echo ""

# Step 1: Create virtual environment
echo "📦 Step 1: Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Failed to create venv. Make sure Python 3.10+ is installed."
    exit 1
fi

# Step 2: Activate venv
echo "⚡ Step 2: Activating virtual environment..."
source venv/bin/activate

# Step 3: Install requirements
echo "📥 Step 3: Installing dependencies..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies."
    exit 1
fi

# Step 4: Run migrations
echo "🗄️  Step 4: Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Step 5: Populate sample data
echo "🌱 Step 5: Loading sample food data..."
python manage.py populate_data

# Step 6: Collect static files
echo "📂 Step 6: Collecting static files..."
python manage.py collectstatic --noinput --clear

# Step 7: Create superuser
echo ""
echo "👤 Step 7: Create Admin Superuser"
echo "   (You'll use this to log into /admin/)"
python manage.py createsuperuser

# Done!
echo ""
echo "✅ =================================="
echo "   Setup Complete!"
echo "   =================================="
echo ""
echo "🚀 Starting development server..."
echo "   Visit: http://127.0.0.1:8000/"
echo "   Admin: http://127.0.0.1:8000/admin/"
echo ""
python manage.py runserver
