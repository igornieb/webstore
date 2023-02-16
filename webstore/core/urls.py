from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path('product/<slug>', views.ProductDetail.as_view(), name='product'),
]