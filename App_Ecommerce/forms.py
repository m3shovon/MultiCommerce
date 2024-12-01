from django import forms
from .models import Order

# class AddToCartForm(forms.Form):
#     color = forms.ModelChoiceField(queryset=None, required=True, empty_label="Select Color")
#     size = forms.ModelChoiceField(queryset=None, required=True, empty_label="Select Size")
#     quantity = forms.IntegerField(min_value=1, required=True)

#     def __init__(self, item, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['color'].queryset = ItemVariation.objects.filter(item=item).distinct('color')
#         self.fields['size'].queryset = ItemVariation.objects.filter(item=item).distinct('size')


class OrderForm(forms.ModelForm):
    color = forms.ChoiceField(
        label="Color",
        choices=[],  # Dynamically populated in the view
        widget=forms.RadioSelect
    )
    size = forms.ChoiceField(
        label="Size",
        choices=[],  # Dynamically populated in the view
        widget=forms.RadioSelect
    )
    quantity = forms.IntegerField(
        label="Quantity",
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Order
        fields = ['customer_name', 'phone', 'address', 'quantity', 'color', 'size']

    def __init__(self, *args, **kwargs):
        item_variations = kwargs.pop('item_variations', None)
        super().__init__(*args, **kwargs)

        # Populate color choices based on available item variations
        if item_variations:
            colors = {iv.color for iv in item_variations}
            self.fields['color'].choices = [(color, color) for color in colors]