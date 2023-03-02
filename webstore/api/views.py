from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Customer, CustomerAddress, Product, Category, Brand
from .serializers import *
from core.utilis import product_order


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


class ProductDetails(APIView):
    def get_queryset(self, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        product = self.get_queryset(slug)
        serializer = ProductSerializer(product, many=False, context={'request': request})
        return Response(serializer.data)


class ProductList(APIView):
    def get_queryset_ordered(self, ob=""):
        return Product.objects.all().order_by(ob)

    def get_queryset(self):
        return Product.objects.all().order_by('no_of_items_sold')

    def get(self, request):
        if 'order_by' in request.query_params:
            o_b = str(request.query_params['order_by'])
            if o_b in product_order:
                product = self.get_queryset_ordered(product_order.get(o_b))
            else:
                message = f"wrong GET parameter {o_b}"
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            product = self.get_queryset()
        serializer = ProductSerializer(product, many=True, context={'request': request})
        return Response(serializer.data)


class ProductCategoryList(APIView):
    def get_queryset_ordered(self, category, ob):
        try:
            category = Category.objects.get(name=category)
            return Product.objects.filter(category=category).order_by(ob)
        except Category.DoesNotExist:
            raise Http404

    def get_queryset(self, category):
        try:
            category = Category.objects.get(name=category)
            return Product.objects.filter(category=category).order_by('no_of_items_sold')
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category):
        if 'order_by' in request.query_params:
            o_b = str(request.query_params['order_by'])
            if o_b in product_order:
                product = self.get_queryset_ordered(category, product_order.get(o_b))
            else:
                message = f"wrong GET parameter {o_b}"
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            product = self.get_queryset(category)
        serializer = ProductSerializer(product, many=True, context={'request': request})
        return Response(serializer.data)


class ProductBrandList(APIView):
    def get_queryset_ordered(self, brand, ob):
        try:
            brand = Brand.objects.get(name=brand)
            return Product.objects.filter(brand=brand).order_by(ob)
        except Brand.DoesNotExist:
            raise Http404

    def get_queryset(self, brand):
        try:
            brand = Brand.objects.get(name=brand)
            return Product.objects.filter(brand=brand).order_by('no_of_items_sold')
        except Brand.DoesNotExist:
            raise Http404

    def get(self, request, brand):
        if 'order_by' in request.query_params:
            o_b = str(request.query_params['order_by'])
            if o_b in product_order:
                product = self.get_queryset_ordered(brand, product_order.get(o_b))
            else:
                message = f"wrong GET parameter {o_b}"
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            product = self.get_queryset(brand)
        serializer = ProductSerializer(product, many=True, context={'request': request})
        return Response(serializer.data)
