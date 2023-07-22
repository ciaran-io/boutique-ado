import stripe
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView

from apps.cart.context_processors import cart_contents
from apps.checkout.models import Order, OrderLineItem
from apps.products.models import Product
from .forms import OrderForm

stripe_public_key = settings.STRIPE_PUBLIC_KEY
stripe_secret_key = settings.STRIPE_SECRET_KEY


class CheckoutView(TemplateView):
    template_name = 'checkout.html'

    def dispatch(self, request, *args, **kwargs):
        cart = self.request.session.get('cart', {})
        if not cart or (cart is not None and len(cart) == 0):
            messages.error(self.request, "Your cart is empty")
            return redirect(reverse('products'))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_form = OrderForm()

        current_cart = cart_contents(self.request)
        total = current_cart['grand_total']
        stripe.api_key = stripe_secret_key
        stripe_total = round(total * 100)
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        context.update({
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        })

        return context
