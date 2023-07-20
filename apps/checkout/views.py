from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView

from .forms import OrderForm


# Create your views here.


class CheckoutView(TemplateView):
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        if not cart:
            messages.error(self.request, "Your cart is empty")
            return redirect(reverse('products'))

        order_form = OrderForm()

        context = {
            'order_form': order_form,
        }

        return context
