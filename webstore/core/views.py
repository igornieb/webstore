from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView
from .utilis import product_order
from django.views import View


class ProductList(ListView):
    model = Product
    template_name = 'test.html'
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
    template_name = 'test.html'
    paginate_by = 60

    def get(self, request, category):
        category = Category.objects.get(name=category)
        queryset = Product.objects.filter(category=category)
        if self.request.GET.get("order_by"):
            order_by = product_order[self.request.GET.get("order_by")]
            queryset = queryset.order_by(order_by)
        else:
            queryset = queryset.order_by('-no_of_items_sold')
        context = {
            'product_list': queryset,
        }

        return render(request, 'test.html', context)

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryList, self).get_context_data(**kwargs)
        context['input'] = self.request.GET.get("order_by")
        return context


class ProductBrandList(ListView):
    model = Product
    template_name = 'test.html'
    paginate_by = 60

    def get(self, request, brand):
        brand = Brand.objects.get(name=brand)
        queryset = Product.objects.filter(brand=brand)
        if self.request.GET.get("order_by"):
            order_by = product_order[self.request.GET.get("order_by")]
            queryset = queryset.order_by(order_by)
        else:
            queryset = queryset.order_by('-no_of_items_sold')
        context = {
            'product_list': queryset,
        }

        return render(request, 'test.html', context)

    def get_context_data(self, **kwargs):
        context = super(ProductBrandList, self).get_context_data(**kwargs)
        context['input'] = self.request.GET.get("order_by")
        return context


class ProductSearchList(ListView):
    model = Product
    template_name = 'search.html'
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
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        context = {'product': product, }
        return render(request, 'product_detail.html', context)


class AddToCart(View):
    def get(self, request, slug):
        session = Session.objects.get(pk=request.session.session_key)
        product = Product.objects.get(slug=slug)

        if Cart.objects.filter(session=session, item=product).exists():
            cart = Cart.objects.get(session=session, item=product)
            if product.no_of_items_in_stock > cart.quantity:
                cart.quantity += 1
                cart.save()
        else:
            if product.no_of_items_in_stock > 0:
                Cart.objects.create(session=session, item=product, quantity=1)

        return redirect(request.META.get('HTTP_REFERER'))


class RemoveFromCart(View):
    def get(self, request, slug):
        session = Session.objects.get(pk=request.session.session_key)
        product = Product.objects.get(slug=slug)

        if Cart.objects.filter(session=session, item=product).exists():
            cart = Cart.objects.get(session=session, item=product)
            if cart.quantity == 1:
                cart.delete()
            else:
                cart.quantity -= 1
                cart.save()

        return redirect(request.META.get('HTTP_REFERER'))
