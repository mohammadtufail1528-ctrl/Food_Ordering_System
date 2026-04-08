@echo off
:: ═══════════════════════════════════════════════════════════
:: Foodie — Windows Setup Script
:: ═══════════════════════════════════════════════════════════

echo.
echo  🍔  ==================================
echo      FOODIE - Django Food Ordering App
echo      ==================================
echo.

echo [1/7] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Could not create venv. Is Python 3.10+ installed?
    pause
    exit /b 1
)

echo [2/7] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/7] Installing dependencies...
pip install -r requirements.txt

echo [4/7] Running database migrations...
python manage.py makemigrations
python manage.py migrate

echo [5/7] Loading sample food data...
python manage.py populate_data

echo [6/7] Collecting static files...
python manage.py collectstatic --noinput

echo [7/7] Create superuser for admin panel...
python manage.py createsuperuser

echo.
echo  ✅ ==================================
echo     Setup Complete!
echo     ==================================
echo.
echo  Visit:  http://127.0.0.1:8000/
echo  Admin:  http://127.0.0.1:8000/admin/
echo.

python manage.py runserver
pause
