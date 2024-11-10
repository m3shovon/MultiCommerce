from django.forms import ModelForm
from App_Auth.models import User, CustomerProfile
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from App_Auth.models import User, CustomerProfile


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


