from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm, AdminLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from App_Hotel import models as App_HotelModel
from App_Hotel import forms as App_HotelForms
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


@login_required
def profile_view(request):
    """
    View to display the user's profile.
    """
    profile = get_object_or_404(App_AuthModel.CustomerProfile, user=request.user)
    return render(request, 'App_Auth/profile_view.html', {'profile': profile})

@login_required
def profile_update(request):
    """
    View to update the user's profile.
    """
    profile = get_object_or_404(App_AuthModel.CustomerProfile, user=request.user)

    if request.method == 'POST':
        form = App_AuthForms.CustomerProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('App_Auth:profile_view')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = App_AuthForms.CustomerProfileForm(instance=profile, user=request.user)

    return render(request, 'App_Auth/profile_update.html', {'form': form})


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

@user_passes_test(is_admin)
def dashboard(request):
    user = request.user
    total_hotels = App_HotelModel.Hotel.objects.count()
    total_rooms = App_HotelModel.Room.objects.count()
    total_new_payments = App_HotelModel.Payment.objects.filter(is_confirmed=False).count()
    total_paid_payments = App_HotelModel.Payment.objects.filter(is_paid=True, is_confirmed=True).count()
    total_non_superusers = App_AuthModel.User.objects.filter(is_superuser=False).count()
    
    context = {
        'user': user,
        'total_hotels': total_hotels,
        'total_rooms': total_rooms,
        'total_new_payments': total_new_payments,
        'total_paid_payments': total_paid_payments,
        'total_non_superusers': total_non_superusers,
    }
    
    return render(request, 'App_Admin/dashboard.html', context)
@user_passes_test(is_admin)
def location_list(request):
    locations = App_HotelModel.Location.objects.all()
    return render(request, 'App_Admin/location_list.html', {'locations': locations})

@user_passes_test(is_admin)
def add_location(request):
    if request.method == 'POST':
        form = App_AuthForms.LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('App_Auth:location_list')
    else:
        form = App_AuthForms.LocationForm()
    return render(request, 'App_Admin/add_location.html', {'form': form})

@user_passes_test(is_admin)
def amenity_list(request):
    amenities = App_HotelModel.Amenity.objects.all()
    return render(request, 'App_Admin/amenity_list.html', {'amenities': amenities})

@user_passes_test(is_admin)
def add_amenity(request):
    if request.method == 'POST':
        form = App_AuthForms.AmenityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('App_Auth:amenity_list')
    else:
        form = App_HotelForms.AmenityForm()
    return render(request, 'App_Admin/add_amenity.html', {'form': form})

@user_passes_test(is_admin)
def hotel_list(request):
    hotels = App_HotelModel.Hotel.objects.all()
    return render(request, 'App_Admin/hotel_list.html', {'hotels': hotels})

@user_passes_test(is_admin)
def add_hotel(request):
    if request.method == 'POST':
        form = App_AuthForms.HotelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('App_Auth:hotel_list')
    else:
        form = App_AuthForms.HotelForm()
    return render(request, 'App_Admin/add_hotel.html', {'form': form})

@user_passes_test(is_admin)
def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(App_HotelModel.Hotel, id=hotel_id)
    rooms = hotel.rooms.all()

    if request.method == 'POST':
        form = App_AuthForms.RoomForm(request.POST, request.FILES)
        if form.is_valid():
            new_room = form.save(commit=False)
            new_room.hotel = hotel
            new_room.save()
            return redirect('App_Admin:hotel_detail', hotel_id=hotel.id)
    else:
        form = App_AuthForms.RoomForm()

    return render(request, 'App_Admin/hotel_details.html', {
        'hotel': hotel,
        'rooms': rooms,
        'form': form
    })

@user_passes_test(is_admin)
def room_list(request):
    rooms = App_HotelModel.Room.objects.all()
    return render(request, 'App_Admin/room_list.html', {'rooms': rooms})

@user_passes_test(is_admin)
def add_room(request):
    if request.method == 'POST':
        form = App_AuthForms.RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('App_Auth:room_list')
    else:
        form = App_AuthForms.RoomForm()
    return render(request, 'App_Admin/add_room.html', {'form': form})


# ############### Payment ##################

@user_passes_test(is_admin)
def payment_list(request):
    # Annotate payments with the first_name of the first booking's customer, defaulting to None if not found
    payments = App_HotelModel.Payment.objects.annotate(
        customer_name=Coalesce(
            Subquery(
                App_HotelModel.Booking.objects.filter(
                    payment=OuterRef('pk')
                ).values('user__first_name')[:1]
            ),
            Value('N/A')  # Use Value to provide 'N/A' as a text default
        )
    ).prefetch_related('booking__room__hotel')
    
    return render(request, 'App_Admin/payment_list.html', {'payments': payments})


@user_passes_test(is_admin)
def view_payment(request, pk):
    payment = get_object_or_404(App_HotelModel.Payment, pk=pk)
    return render(request, 'App_Admin/payment_view.html', {'payment': payment})

@user_passes_test(is_admin)
def update_payment(request, pk):
    payment = get_object_or_404(App_HotelModel.Payment, pk=pk)
    if request.method == 'POST':
        form = App_AuthForms.PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('App_Auth:payment_list')
    else:
        form = App_AuthForms.PaymentForm(instance=payment)
    return render(request, 'App_Admin/payment_update.html', {'form': form})

@user_passes_test(is_admin)
def view_profiles(request):
    profiles = App_AuthModel.CustomerProfile.objects.all()
    return render(request, 'App_Admin/profile_list.html', {'profiles': profiles})