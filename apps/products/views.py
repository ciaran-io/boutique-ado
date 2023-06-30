from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.generic import TemplateView

from .models import Product, Category

# Sort options for products
sort_options = {
    'price_asc': 'Price (low to high)',
    'price_desc': 'Price (high to low)',
    'rating_asc': 'Rating (low to high)',
    'rating_desc': 'Rating (high to low)',
    'name_asc': 'Name (A-Z)',
    'name_desc': 'Name (Z-A)',
    'category_asc': 'Category (A-Z)',
    'category_desc': 'Category (Z-A)',
}


class AllProductsView(TemplateView):
    """ A view to show all products, including sorting and search queries"""
    template_name = 'products.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        category = request.GET.get('category')
        categories = None
        sort = None
        direction = None
        products = Product.objects.all()
        search_results = True  # Flag to indicate if any search results found

        # If there is a query, that is sort my name
        if sortkey := request.GET.get('sort'):
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if sortkey == 'category':
                sortkey = 'category__name'

            if direction := request.GET.get('direction'):
                direction = direction
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if category and category != '':
            categories = request.GET.get('category').split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if query and query != '':
            products = products.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
            search_results = bool(
                products)  # Set flag based on the presence of search results
            if not search_results:
                messages.error(request,
                               "No products found for the search criteria.")

                return redirect(reverse('products'))

        current_sorting = f'{sort}_{direction}'

        context = self.get_context_data(
            products=products,
            search_term=query,
            search_results=search_results,
            current_categories=categories,
            current_sorting=current_sorting,
            sort_options=sort_options
        )
        return self.render_to_response(context)


class ProductDetailView(TemplateView):
    """ A view to show individual product details """
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=kwargs['product_id'])
        context['product'] = product
        return context
