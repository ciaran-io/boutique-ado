from django.contrib import admin
from django.urls import path
from .views import AllProductsView

urlpatterns = [
    path('', AllProductsView.as_view(), name='products'),
]
