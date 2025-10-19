# inventory/urls.py
from django.urls import path
from . import views

app_name = 'forecast'

urlpatterns = [
    path('', views.forecast_dashboard, name='forecast_dashboard'),
    path("<int:product_id>/<int:warehouse_id>/chart/", views.forecast_chart_view, name="forecast_chart"),
  
]
# --- IGNORE ---