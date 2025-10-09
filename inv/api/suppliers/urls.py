# urls.py
from django.urls import path
from .views import (
    SupplierListView, SupplierCreateView, SupplierUpdateView, SupplierDeleteView
)
app_name = 'suppliers'
urlpatterns = [
    path('suppliers/', SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/create/', SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/<int:pk>/edit/', SupplierUpdateView.as_view(), name='supplier_update'),
    path('suppliers/<int:pk>/delete/', SupplierDeleteView.as_view(), name='supplier_delete'),
]
