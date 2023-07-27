from django.urls import path

from .views import (AllProductsView,
                    ProductCreateView,
                    ProductDeleteView,
                    ProductDetailView,
                    ProductUpdateView,
                    )

urlpatterns = [
    path('', AllProductsView.as_view(), name='products'),
    path('<int:product_id>/', ProductDetailView.as_view(),
         name='product_detail'),
    path('new/', ProductCreateView.as_view(),
         name='product_create'),
    path('update/<int:pk>/', ProductUpdateView.as_view(),
         name='product_update'),
    path('delete/<int:product_id>/', ProductDeleteView.as_view(),
         name='product_delete'),
]
