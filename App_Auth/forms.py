from django.forms import ModelForm
from App_Auth.models import User, CustomerProfile
from App_Hotel.models import Payment
from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from App_Auth.models import User, CustomerProfile
from App_Hotel import models as HotelModel

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            CustomerProfile.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )  
        return user

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=255)

class AdminLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=255)

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['user', 'first_name', 'last_name', 'phone', 'address', 'city', 'zipcode', 'country']
        widgets = {
            'user': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', }),
            'address': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user.email

# ################# For Hotel
class LocationForm(forms.ModelForm):
    class Meta:
        model = HotelModel.Location
        fields = ['name']

class AmenityForm(forms.ModelForm):
    class Meta:
        model = HotelModel.Amenity
        fields = ['name', 'icon']


class HotelForm(forms.ModelForm):
    class Meta:
        model = HotelModel.Hotel
        fields = ['name', 'location', 'description', 'amenities', 'price_per_night', 'images', 'featured_images']
    
    amenities = forms.ModelMultipleChoiceField(
        queryset=HotelModel.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'amenity-checkbox'})
    )

    price_per_night = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price per night'}))

    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hotel Name'}),
        'location': forms.Select(attrs={'class': 'form-control'}),
        'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a brief description of the hotel'}),
        'images': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        'featured_images': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
    }


class RoomForm(forms.ModelForm):
    class Meta:
        model = HotelModel.Room
        fields = ['hotel', 'room_type', 'amenities', 'number_of_beds', 'price_per_night', 'is_available', 'images']
        widgets = {
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'room_type': forms.TextInput(attrs={'class': 'form-control'}),
            'amenities': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'number_of_beds': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'images': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [ 'is_cancelled', 'is_confirmed'] 