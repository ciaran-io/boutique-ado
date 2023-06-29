from django.contrib import admin
from django.urls import path
from .views import AllProductsView, ProductDetailView

urlpatterns = [
    path('', AllProductsView.as_view(), name='products'),
    path('<product_id>/', ProductDetailView.as_view(), name='product_detail'),

]
