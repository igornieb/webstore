from django.db.models import Q, Sum
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import *
from .serializers import *
from core.utilis import product_order, total_amount_for_session, get_discount

class CustomerView(APIView):
    def get_permissions(self):
        return [permissions.IsAuthenticated()]
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
    def get_permissions(self):
        return [permissions.IsAuthenticated()]
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
            return Product.objects.filter(brand=brand).order_by('-no_of_items_sold')
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


class SearchProductView(APIView):
    def get_queryset(self, search):
        return Product.objects.filter(Q(name__icontains=search) | Q(brand__name__icontains=search) | Q(
            category__name__icontains=search)).order_by('-no_of_items_sold')

    def get_queryset_ordered(self, search, ob):
        return Product.objects.filter(Q(name__icontains=search) | Q(brand__name__icontains=search) | Q(
            category__name__icontains=search)).order_by(ob)

    def get(self, request, search):
        if 'order_by' in request.query_params:
            o_b = str(request.query_params['order_by'])
            if o_b in product_order:
                product = self.get_queryset_ordered(search, product_order.get(o_b))
            else:
                message = f"wrong GET parameter {o_b}"
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            product = self.get_queryset(search)
        serializer = ProductSerializer(product, many=True, context={'request': request})
        return Response(serializer.data)


class CartView(APIView):

    def get_queryset(self):
        session = Session.objects.get(pk=self.request.session.session_key)
        return Cart.objects.filter(session=session)

    def get_session(self):
        return Session.objects.get(pk=self.request.session.session_key)

    def get(self, request):
        carts = self.get_queryset()
        serializer = CartSerializer(carts, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        try:
            session = self.get_session()
            product = Product.objects.get(slug=request.data['item'])
        except Product.DoesNotExist:
            raise Http404

        if Cart.objects.filter(session=session, item=product).exists():
            cart = Cart.objects.get(session=session, item=product)
            serializer = CartSerializer(cart, data=request.data, partial=True, context={'request': request})
        else:
            serializer = CartSerializer(data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save(item=product, session=session)
            if request.data['quantity'] > product.no_of_items_in_stock:
                return Response("not enough items in stock", status=status.HTTP_403_FORBIDDEN)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailsView(APIView):

    def get_queryset(self, slug):
        try:
            return Cart.objects.get(item__slug=slug)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        cart = self.get_queryset(slug)
        serializer = CartSerializer(cart, many=False, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, slug):
        cart = self.get_queryset(slug)
        serializer = CartSerializer(cart, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            if request.data['quantity'] > cart.item.no_of_items_in_stock:
                return Response("not enough items in stock", status=status.HTTP_403_FORBIDDEN)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        cart = self.get_queryset(slug)
        cart.delete()
        return Response(status=status.HTTP_200_OK)


class CheckoutView(APIView):
    def get_permissions(self):
        return [permissions.IsAuthenticated()]
    def get_queryset(self):
        session = Session.objects.get(pk=self.request.session.session_key)
        if Cart.objects.filter(session=session).exists():
            return Cart.objects.filter(session=session)
        else:
            raise Http404

    def get(self, request):
        carts = self.get_queryset()
        total = total_amount_for_session(carts)
        message = {'total': total}
        return Response(message, status=status.HTTP_200_OK)

    def post(self, request):
        carts = self.get_queryset()
        customer = self.request.user.customer
        total = total_amount_for_session(carts)
        if 'discount_code' in request.data:
            # check if discount exist -> set total or return error
            if Discount.objects.filter(name=request.data['discount_code']).exists():
                discount = Discount.objects.get(name=request.data['discount_code'])
                if discount.active:
                    total = get_discount(discount.amount, total)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        order = Order.objects.create(owner=customer, total=total)
        for cart in carts:
            if 'discount_code' in request.data:
                discount = Discount.objects.get(name=request.data['discount_code'])
                total = get_discount(discount.amount, cart.total())
                OrderItem.objects.create(order=order, total=total, amount=cart.quantity, item=cart.item)
            else:
                OrderItem.objects.create(order=order, total=cart.total(), amount=cart.quantity, item=cart.item)
        carts.delete()
        return Response(status=status.HTTP_201_CREATED)


class CheckDiscount(APIView):
    def get_queryset(self, name):
        try:
            return Discount.objects.get(name=name, active=True)
        except Discount.DoesNotExist:
            raise Http404

    def get(self, request, name):
        discount = self.get_queryset(name)
        print(discount)
        session = Session.objects.get(pk=self.request.session.session_key)
        carts = Cart.objects.filter(session=session)
        total = get_discount(discount.amount, total_amount_for_session(carts))
        message = {
            'discount_code': discount.name,
            'amount': discount.amount,
            'total': total
        }
        return Response(message, status=status.HTTP_200_OK)


class CreateUserView(CreateAPIView):

    model = User
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer



