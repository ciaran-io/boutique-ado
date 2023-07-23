from django.urls import path

from .views import CheckoutSuccessView, CheckoutView
from .webhooks import webhook

urlpatterns = [
    path('', CheckoutView.as_view(), name='checkout'),
    path('checkout_success/<order_number>', CheckoutSuccessView.as_view(),
         name='checkout_success'),
    path('wh/', webhook, name='webhook'),
]
