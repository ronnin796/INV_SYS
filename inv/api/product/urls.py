from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('create/', views.ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
    path('ajax/load-products/', views.ajax_load_products, name='ajax_load_products'),
    path('ajax/load-supplier-products/', views.ajax_load_supplier_products, name='ajax_load_supplier_products'),
    path('ajax/get-price/', views.ajax_get_product_price, name='ajax_get_product_price'),

]

