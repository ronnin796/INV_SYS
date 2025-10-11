from django.urls import path
from .views import (
    WarehouseListView,
    WarehouseCreateView,
    WarehouseUpdateView,
    WarehouseDeleteView
)

app_name = 'warehouse'

urlpatterns = [
    path('', WarehouseListView.as_view(), name='warehouse_list'),
    path('create/', WarehouseCreateView.as_view(), name='warehouse_create'),
    path('<int:pk>/edit/', WarehouseUpdateView.as_view(), name='warehouse_edit'),
    path('<int:pk>/delete/', WarehouseDeleteView.as_view(), name='warehouse_delete'),
]
