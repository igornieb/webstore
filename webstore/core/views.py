from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView


class ProductList(ListView):
    model = Product
    template_name = 'home.html'
    ordering = '-no_of_items_sold'
    paginate_by = 60


class ProductDetail(DetailView):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        context = {'product':product,}
        return render(request, 'product_detail.html', context)




