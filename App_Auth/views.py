from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm, AdminLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from App_Auth import models as App_AuthModel
from App_Auth import forms as App_AuthForms
from django.db.models import Subquery, OuterRef, Value
from django.db.models.functions import Coalesce

# 404 Error
def handle_not_found(request,exception):
	return render(request, "App_Auth/404.html", status=404)

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('App_Auth:signin')
    else:
        form = SignupForm()

    return render(request, 'App_Auth/signup.html', {'form': form})

def signin_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('App_Hotel:home')  # Redirect to home after login
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'App_Auth/signin.html', {'form': form})

@login_required
def signout_view(request):
    logout(request)
    return redirect('App_Auth:signin')  


# ######### +++++++++++++++++++++ ADMIN PANEL +++++++++++++++++++++ #########

def is_admin(user):
    return user.is_authenticated and user.is_staff and user.is_superuser

def admin_logout_view(request):
    logout(request)
    return redirect('App_Auth:admin-login')  

def admin_login_view(request):
    if request.method == 'POST':
        form = AdminLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_staff and user.is_superuser:  
                    login(request, user)
                    return redirect('App_Auth:dashboard')  
                else:
                    messages.error(request, 'Access denied. Admin only.')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = AdminLoginForm()
    return render(request, 'App_Admin/login.html', {'form': form})

