from .models import Product
from django.views.generic import TemplateView
# Create your views here.


class AllProductsView(TemplateView):
    template_name = 'products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context

