from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Customer, CustomerAddress
from .serializers import *


# TODO authentication for views, tokens

class CustomerView(APIView):
    def get_queryset(self):
        try:
            return self.request.user.customer
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request):
        customer = self.get_queryset()
        serializer = CustomerSerializer(customer, many=False)
        return Response(serializer.data)

    def patch(self, request):
        customer = self.get_queryset()
        user = self.request.user
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request):
        user = self.request.user
        user.delete()
        message = "{'Status':'Account deleted'}"
        return Response(message, status=status.HTTP_200_OK)

class CustomerAddressView(APIView):
    def get_queryset(self):
        try:
            customer = self.request.user.customer
            return CustomerAddress.objects.get(customer=customer)
        except CustomerAddress.DoesNotExist or Customer.DoesNotExist:
            raise Http404

    def get(self, request):
        address = self.get_queryset()
        serializer = CustomerAddressSerializer(address, many=False)
        return Response(serializer.data)

    def patch(self, request):
        customer_address = self.get_queryset()
        serializer = CustomerAddressSerializer(customer_address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

