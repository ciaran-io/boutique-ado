from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views import View
from django.views.generic import CreateView, ListView, \
    TemplateView, UpdateView

from .forms import ProductForm
from .models import Category, Product

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

sizes = ['xs', 's', 'm', 'l', 'xl']


class AllProductsView(ListView):
    """A view to show all products, including sorting and search queries"""
    template_name = 'products.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        sort = self.request.GET.get('sort')
        direction = self.request.GET.get('direction')

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

        if category and category != '':
            categories = category.split(',')
            queryset = queryset.filter(category__name__in=categories)

        if sort:
            if sort == 'name':
                sort = 'lower_name'
                queryset = queryset.annotate(lower_name=Lower('name'))
            elif sort == 'category':
                sort = 'category__name'
            else:
                sort = None

        if direction == 'desc':
            sort = f'-{sort}' if sort else None

        if sort:
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        sort = self.request.GET.get('sort')
        direction = self.request.GET.get('direction')

        context['search_term'] = query
        context['search_results'] = bool(self.get_queryset())
        context['current_categories'] = \
            Category.objects.filter(name__in=category.split(
                ',')) if category and category != '' else None
        context['current_sorting'] = \
            f'{sort}_{direction}' if sort and direction else None
        context['sort_options'] = sort_options
        context['sizes'] = sizes

        return context

    def render_to_response(self, context, **response_kwargs):
        if not context['search_results']:
            messages.error(self.request,
                           "No products found for the search criteria.")
            return redirect(reverse('products'))

        return super().render_to_response(context, **response_kwargs)


class ProductDetailView(TemplateView):
    """ A view to show individual product details """
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=kwargs['product_id'])
        context['product'] = product
        context['sizes'] = sizes
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_add.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'Sorry, only store owners can do that.')
            return redirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Successfully added product!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,
                       'Failed to add product. '
                       'Please ensure the form is valid.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('product_detail', args=[self.object.pk])


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'product_edit.html'
    form_class = ProductForm
    context_object_name = 'product'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'Sorry, only store owners can do that.')
            return redirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Successfully updated product!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to update product. '
                                     'Please ensure the form is valid.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, f'You are editing {self.object.name}')
        return context

    def get_success_url(self):
        return reverse('product_detail', args=[self.object.pk])


class ProductDeleteView(LoginRequiredMixin, View):
    """ A view to delete a product """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'Sorry, only store owners can do that.')
            return redirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        messages.success(request, 'Product deleted!')
        return redirect(reverse('products'))
