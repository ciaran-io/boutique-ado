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

    def post(self, request, *args, **kwargs):

        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.save()
            #
            cart = self.request.session.get('cart', {})
            for item_id, item_data in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data,
                                  int):  # if item_data is an integer
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:  # if item_data is a dictionary
                        for size, quantity in \
                                item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found in "
                        "our database."
                        "Please call us for assistance!")
                                   )
                    order.delete()
                    return redirect(reverse('view_cart'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(
                reverse('checkout_success', args=[order.order_number]))

        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
            return redirect(reverse('checkout'))


class CheckoutSuccessView(TemplateView):
    template_name = 'checkout_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_number = kwargs.get('order_number')
        order = get_object_or_404(Order, order_number=order_number)
        messages.success(self.request, f'Order successfully processed! \
            Your order number is {order_number}. A confirmation \
            email will be sent to {order.email}.')
        if 'cart' in self.request.session:
            del self.request.session['cart']
        customer_details = {
            'full_name': order.full_name,
            'email': order.email,
            'phone_number': order.phone_number,
            'country': order.country,
            'postcode': order.postcode,
            'town_or_city': order.town_or_city,
            'street_address1': order.street_address1,
            'street_address2': order.street_address2,
            'county': order.county,
        }
        # add N/a for empty fields
        for field, value in customer_details.items():
            if not value:
                customer_details[field] = 'N/a'
        # remove _ from field names
        customer_details = {k.replace('_', ' ').title(): v for k, v in
                            customer_details.items()}

        context.update({
            'order': order,
            'customer_details': customer_details,
        })
        return context
