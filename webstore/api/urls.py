from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('customer/', CustomerView.as_view(), name='customer-settings'),
    path('customer-address/', CustomerAddressView.as_view(), name='customer-address'),
    path('product/<slug:slug>/', ProductDetails.as_view(), name='product-details'),
    path('product-list/', ProductList.as_view(), name='product-list'),
    path('category-product-list/<str:category>/', ProductCategoryList.as_view(), name='category-product-list'),
    path('brand-product-list/<str:brand>/', ProductBrandList.as_view(), name='brand-product-list'),
    path('search-product/<str:search>/', SearchProductView.as_view(), name='search-product'),
    path('cart-list/', CartView.as_view(), name='cart-list'),
    path('cart-details/<slug:slug>/', CartDetailsView.as_view(), name='cart-details'),
    path('checkout/', CheckoutView.as_view(), name='checkout-view'),
    path('discount/<str:name>/', CheckDiscount.as_view(), name='discount-view'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', CreateUserView.as_view()),
]
