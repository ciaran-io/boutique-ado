from django.views.generic import TemplateView

# Create your views here.


class CartPageView(TemplateView):
    template_name = 'cart.html'
