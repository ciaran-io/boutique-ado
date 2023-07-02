from django.urls import path
from .views import CartPageView
from .utils import add_to_cart

urlpatterns = [
    path('', CartPageView.as_view(), name='cart'),
    path('add/<item_id>/', add_to_cart, name='add_to_cart'),
]
