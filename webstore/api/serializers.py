from rest_framework import serializers
from core.models import *

# TODO delete this shit XD
try:
    from ..core.models import *
except:
    pass


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Customer
        fields = ['user', 'firstname', 'lastname', 'phone_number']


class CustomerAddressSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.user', read_only=True)

    class Meta:
        model = CustomerAddress
        fields = ['customer', 'firstname', 'lastname', 'city', 'postcode', 'street', 'house_number']


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product-details', read_only=True, lookup_field='slug')
    brand = serializers.CharField(source="brand.name")
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Product
        fields = ('url', 'name', 'slug', 'category', 'brand', 'image', 'current_price', 'base_price', 'description',
                  'no_of_items_in_stock')


class CartSerializer(serializers.ModelSerializer):
    item = ProductSerializer(read_only=True)
    quantity = serializers.IntegerField(min_value=1)
    class Meta:
        model = Cart
        fields = ('item', 'quantity', 'total')
