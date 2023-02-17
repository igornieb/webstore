from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path('product/<slug>', views.ProductDetail.as_view(), name='product'),
    path('search', views.ProductSearchList.as_view(), name='search'),
    path('category/<str:category>', views.ProductCategoryList.as_view(), name='category'),
    path('brand/<str:brand>', views.ProductBrandList.as_view(), name='brand'),
    path('add-to-cart/<str:slug>', views.AddToCart.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:slug>', views.RemoveFromCart.as_view(), name='remove_from_cart '),
]