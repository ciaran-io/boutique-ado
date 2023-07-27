from django.urls import path

from .utils import cache_checkout_data
from .views import CheckoutSuccessView, CheckoutView
from .webhooks import webhook

urlpatterns = [
    path('', CheckoutView.as_view(), name='checkout'),
    path('checkout_success/<order_number>', CheckoutSuccessView.as_view(),
         name='checkout_success'),
    path('wh/', webhook, name='webhook'),
    path('cache_checkout_data/', cache_checkout_data,
         name='cache_checkout_data'),
]
