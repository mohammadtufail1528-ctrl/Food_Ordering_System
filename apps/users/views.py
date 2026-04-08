"""
Users App Views
- Signup
- Login
- Logout
- Profile
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def signup_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('menu:home')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        # Validations
        if not all([first_name, username, email, password1, password2]):
            messages.error(request, '❌ All fields are required.')
            return render(request, 'users/signup.html')

        if password1 != password2:
            messages.error(request, '❌ Passwords do not match.')
            return render(request, 'users/signup.html')

        if len(password1) < 8:
            messages.error(request, '❌ Password must be at least 8 characters.')
            return render(request, 'users/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, '❌ Username already taken.')
            return render(request, 'users/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, '❌ Email already registered.')
            return render(request, 'users/signup.html')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
        )

        login(request, user)
        messages.success(request, f'🎉 Welcome to Foodie, {first_name}! Your account is created.')
        return redirect('menu:home')

    return render(request, 'users/signup.html', {'page_title': 'Sign Up - Foodie'})


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('menu:home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if not remember_me:
                # Session expires when browser closes
                request.session.set_expiry(0)

            messages.success(request, f'👋 Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'menu:home')
            return redirect(next_url)
        else:
            messages.error(request, '❌ Invalid username or password.')

    return render(request, 'users/login.html', {'page_title': 'Login - Foodie'})


def logout_view(request):
    """User logout"""
    logout(request)
    messages.info(request, '👋 You have been logged out. See you soon!')
    return redirect('menu:home')


@login_required
def profile_view(request):
    """User profile page"""
    from apps.orders.models import Order
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()

        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()

        messages.success(request, '✅ Profile updated successfully!')
        return redirect('users:profile')

    context = {
        'user': request.user,
        'recent_orders': recent_orders,
        'page_title': 'My Profile - Foodie',
    }
    return render(request, 'users/profile.html', context)
