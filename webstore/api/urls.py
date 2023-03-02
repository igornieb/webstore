from django.urls import path, include
from .views import *

urlpatterns = [
    path('customer/', CustomerView.as_view(), name='customer-settings'),
    path('customer-address/', CustomerAddressView.as_view(), name='customer-address'),

]
