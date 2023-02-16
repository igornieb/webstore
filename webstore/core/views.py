from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView


class ProductList(ListView):
    model = Product
    template_name = 'test.html'
    paginate_by = 1

    def get_queryset(self):
        if self.request.GET.get("order_by"):
            order = {
                'bestselers': '-no_of_items_sold',
                'price_a': 'current_price',
                'price_d': '-current_price',
            }
            order_by = order[self.request.GET.get("order_by")]
            queryset = Product.objects.all().order_by(order_by)
        else:
            queryset = Product.objects.all().order_by('-no_of_items_sold')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['input'] = self.request.GET.get("order_by")
        return context


class ProductDetail(DetailView):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        context = {'product': product, }
        return render(request, 'product_detail.html', context)
