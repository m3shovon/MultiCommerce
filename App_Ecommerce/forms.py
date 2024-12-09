from django import forms
# from .models import CartItem

# class CartItemForm(forms.ModelForm):
#     class Meta:
#         model = CartItem
#         fields = ['quantity']

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

class AddToCartForm(forms.Form):
    color = forms.CharField(max_length=255, required=True)
    size = forms.CharField(max_length=255, required=True)
    quantity = forms.IntegerField(min_value=1, required=True)