from django import forms


class CartForm(forms.Form):
    slug = forms.SlugField()
    quantity = forms.IntegerField(min_value=0)