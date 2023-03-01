from django import forms
from .models import CustomerAddress, Customer


class CartForm(forms.Form):
    slug = forms.SlugField()
    quantity = forms.IntegerField(min_value=0)


class DiscountForm(forms.Form):
    name = forms.CharField(max_length=20)


class CustomerAddressForm(forms.ModelForm):
    class Meta:
        model = CustomerAddress
        fields = '__all__'
        exclude = ('customer',)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['firstname','lastname','phone_number']
