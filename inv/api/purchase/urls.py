from django.urls import path
from . import views

app_name = "purchase"

urlpatterns = [
    path("", views.PurchaseOrderListView.as_view(), name="purchase_list"),
    path("create/", views.PurchaseOrderCreateView.as_view(), name="purchase_create"),
    path("<int:pk>/update/", views.PurchaseOrderUpdateView.as_view(), name="purchase_update"),
    path("<int:pk>/delete/", views.PurchaseOrderDeleteView.as_view(), name="purchase_delete"),
    path("<int:pk>/receive/", views.mark_as_received, name="mark_as_received"),
]
