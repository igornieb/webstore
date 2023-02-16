from django.db.models import Q
from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView
from .utilis import product_order

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


class ProductSearchList(ListView):
    model = Product
    template_name = 'search.html'
    paginate_by = 60

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-no_of_items_sold')
        if self.request.GET.get("search"):
            search = self.request.GET.get("search")
            queryset=queryset.filter(Q(name__icontains=search))
        if self.request.GET.get("order_by"):
            order_by = product_order[self.request.GET.get("order_by")]
            queryset=queryset.order_by(order_by)
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
