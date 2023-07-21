from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView

from .forms import OrderForm


# Create your views here.


class CheckoutView(TemplateView):
    template_name = 'checkout.html'

    def dispatch(self, request, *args, **kwargs):
        cart = self.request.session.get('cart', {})
        if not cart or len(cart) == 0:
            messages.error(self.request, "Your cart is empty")
            return redirect(reverse('products'))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_form = OrderForm()

        context.update({
            'order_form': order_form,
            'stripe_public_key': 'pk_test_51NWENXHz16WjPxj2PfvHYDoyJvpFVx2mPuvPWAkKVFRvCL1gHRnFOQuENXEqdRiM7ttBdjbuDkHlKZKsKnQZkJfS00Yw6TZvpZ',
            'client_secret': 'test client secret'
        })

        return context
