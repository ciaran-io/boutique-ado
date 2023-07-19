from django.urls import path
from .views import CartPageView
from .utils import add_to_cart, adjust_cart, remove_from_cart

urlpatterns = [
    path('', CartPageView.as_view(), name='cart'),
    path('add/<item_id>/', add_to_cart, name='add_to_cart'),
    path('adjust/<item_id>/', adjust_cart, name='adjust_cart'),
    path('remove/<item_id>/', remove_from_cart, name='remove_from_cart'),
]
