from .models import Product
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
# Create your views here.


class AllProductsView(TemplateView):
    """ A view to show all products, including sorting and search queries"""
    template_name = 'products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class ProductDetailView(TemplateView):
    """ A view to show individual product details """
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=kwargs['product_id'])
        context['product'] = product
        return context
