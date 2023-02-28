from django.db.models import Q
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView
from .utilis import product_order, total_amount_for_session, get_discount
from django.views import View
from .forms import *
from decimal import Decimal


# TODO checkout, login, register, password reset, account settings
# TODO forms
class CartList(ListView):
    model = Cart
    template_name = 'core/cart.html'
    paginate_by = 10

    def get_queryset(self):
        session = Session.objects.get(pk=self.request.session.session_key)
        return Cart.objects.filter(session=session)

    def get_context_data(self, **kwargs):
        context = super(CartList, self).get_context_data(**kwargs)
        context['total'] = total_amount_for_session(self.get_queryset())
        return context


class ProductList(ListView):
    model = Product
    template_name = 'core/product_list.html'
    paginate_by = 60

    def get_queryset(self):
        if self.request.GET.get("order_by"):
            order_by = product_order[self.request.GET.get("order_by")]
            queryset = Product.objects.all().order_by(order_by)
        else:
            queryset = Product.objects.all().order_by('-no_of_items_sold')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['input'] = self.request.GET.get("order_by")
        return context


class ProductCategoryList(ListView):
    model = Product
    template_name = 'core/product_list.html'
    paginate_by = 60

    def get_queryset(self):
        category = Category.objects.get(name=self.kwargs['category'])
        queryset = Product.objects.filter(category=category)
        if self.request.GET.get("order_by"):
            order_by = product_order[self.request.GET.get("order_by")]
            queryset = queryset.order_by(order_by)
        else:
            queryset = queryset.order_by('-no_of_items_sold')

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryList, self).get_context_data(**kwargs)
        context['input'] = self.request.GET.get("order_by")
        return context


class ProductBrandList(ListView):
    model = Product
    template_name = 'core/product_list.html'
    paginate_by = 60

    def get_queryset(self):
        brand = Brand.objects.get(name=self.kwargs['brand'])
        queryset = Product.objects.filter(brand=brand)
        if self.request.GET.get("order_by"):
            order_by = product_order[self.request.GET.get("order_by")]
            queryset = queryset.order_by(order_by)
        else:
            queryset = queryset.order_by('-no_of_items_sold')

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductBrandList, self).get_context_data(**kwargs)
        context['input'] = self.request.GET.get("order_by")
        return context

class OrderList(ListView):
    model = Order
    template_name = 'core/order_list.html'
    paginate_by = 60

    def get_queryset(self):
        queryset = Order.objects.filter(owner=Customer.objects.get(user=self.request.user))

        return queryset

class ProductSearchList(ListView):
    model = Product
    template_name = 'core/search.html'
    paginate_by = 60

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-no_of_items_sold')
        if self.request.GET.get("search"):
            search = self.request.GET.get("search")
            queryset = queryset.filter(Q(name__icontains=search))
        if self.request.GET.get("order_by"):
            order_by = product_order[self.request.GET.get("order_by")]
            queryset = queryset.order_by(order_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductSearchList, self).get_context_data(**kwargs)
        context['input'] = self.request.GET.get("order_by")
        context['search'] = self.request.GET.get("search")
        return context


class ProductDetail(DetailView):
    def get_queryset(self, request, slug):
        product = Product.objects.get(slug=slug)
        context = {'product': product, }
        return render(request, 'core/product_details.html', context)


class AddToCart(View):

    def post(self, request):
        session = Session.objects.get(pk=request.session.session_key)
        form = CartForm(request.POST)
        if form.is_valid():
            product = Product.objects.get(slug=form.cleaned_data['slug'])
            quantity = form.cleaned_data['quantity']
            if Cart.objects.filter(session=session, item=product).exists():
                cart = Cart.objects.get(session=session, item=product)
                if product.no_of_items_in_stock > quantity and quantity > 0:
                    cart.quantity += quantity
                    cart.save()
            else:
                if product.no_of_items_in_stock >= quantity and quantity > 0:
                    Cart.objects.create(session=session, item=product, quantity=quantity)

        return redirect(request.META.get('HTTP_REFERER'))

    def get(self, request, slug):
        session = Session.objects.get(pk=request.session.session_key)
        product = Product.objects.get(slug=slug)
        if Cart.objects.filter(session=session, item=product).exists():
            cart = Cart.objects.get(session=session, item=product)
            if product.no_of_items_in_stock > cart.quantity + 1:
                cart.quantity += 1
                cart.save()
        else:
            if product.no_of_items_in_stock > 0:
                Cart.objects.create(session=session, item=product, quantity=1)
        return redirect(request.META.get('HTTP_REFERER'))


class DeleteCart(View):
    def get(self, request, slug):
        session = Session.objects.get(pk=request.session.session_key)
        product = Product.objects.get(slug=slug)

        if Cart.objects.filter(session=session, item=product).exists():
            cart = Cart.objects.get(session=session, item=product)
            cart.delete()

        return redirect(request.META.get('HTTP_REFERER'))


class Checkout(View):

    def get(self, request):
        session = Session.objects.get(pk=self.request.session.session_key)
        carts = Cart.objects.filter(session=session)
        customer = Customer.objects.get(user=self.request.user)

        context = {
            'cart_list': carts,
            'total': total_amount_for_session(carts),
            'discount_form': DiscountForm,
            'address': CustomerAddressForm(instance=CustomerAddress.objects.get(customer=customer)),
        }

        return render(request, "core/checkout.html", context)

    def post(self, request):
        session = Session.objects.get(pk=self.request.session.session_key)
        customer = Customer.objects.get(user=self.request.user)
        carts = Cart.objects.filter(session=session)
        total = total_amount_for_session(carts)
        context = {
            'cart_list': carts,
            'total': total_amount_for_session(carts),
            'discount_form': DiscountForm,
            'address': CustomerAddressForm(instance=CustomerAddress.objects.get(customer=customer)),
            'discount': ''
        }
        if 'discount' in request.POST:
            discount_form = DiscountForm(request.POST)
            if discount_form.is_valid():
                if Discount.objects.filter(name=discount_form.cleaned_data['name']).exists():
                    discount = Discount.objects.get(name=discount_form.cleaned_data['name'])
                    if discount.active:
                        context.update({'discount': discount.name,
                                        'total': get_discount(discount.amount, total),
                                        'saved': float(total) - get_discount(discount.amount, total),
                                        })

            return render(request, "core/checkout.html", context)
        else:
            address_form = CustomerAddressForm(request.POST, instance=CustomerAddress.objects.get(customer=customer))
            if address_form.is_valid():
                address_form.save()
                if len(request.POST['discount_name']) > 0:
                    if Discount.objects.filter(name=request.POST['discount_name']).exists():
                        discount = Discount.objects.get(name=request.POST['discount_name'])
                        if discount.active:
                            total = get_discount(discount.amount, total)
                        else:
                            return redirect(request.META.get('HTTP_REFERER'))
                    else:
                        return redirect(request.META.get('HTTP_REFERER'))

                order = Order.objects.create(owner=customer, total=total)
                for cart in carts:
                    OrderItem.objects.create(order=order, total=cart.total(), amount=cart.quantity, item=cart.item)
                carts.delete()
                # return to orders-list

            else:
                return redirect(request.META.get('HTTP_REFERER'))
