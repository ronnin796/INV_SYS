from django.urls import path
from . import views

app_name = "sales"

urlpatterns = [
    path("", views.SalesOrderListView.as_view(), name="sales_list"),
    path("new/", views.SalesOrderCreateView.as_view(), name="sales_create"),
    path("<int:pk>/edit/", views.SalesOrderUpdateView.as_view(), name="sales_edit"),
    path("<int:pk>/delete/", views.SalesOrderDeleteView.as_view(), name="sales_delete"),

    path('sales/<int:pk>/mark-completed/', views.mark_as_completed, name='mark_as_completed'),
]


