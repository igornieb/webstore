from rest_framework import serializers
from core.models import Customer, CustomerAddress


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
