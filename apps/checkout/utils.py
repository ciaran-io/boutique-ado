import json

import stripe
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_POST


@require_POST
def cache_checkout_data(request):
    try:
        data = json
        pid = None
        if data.get('client_secret'):
            pid = data.get('client_secret').split('_secret')[0]

        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': data.get('save_info'),
            'username': request.user,
        })

        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)
