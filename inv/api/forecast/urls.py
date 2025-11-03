# inventory/urls.py
from django.urls import path
from . import views

app_name = 'forecast'

urlpatterns = [
    path('', views.forecast_dashboard, name='forecast_dashboard'),
    path("<int:product_id>/<int:warehouse_id>/chart/", views.forecast_chart_view, name="forecast_chart"),
    path("alerts/", views.forecast_alerts_view, name="forecast_alerts"),
    path("ajax/forecast-chart/", views.ajax_forecast_chart, name="ajax_forecast_chart"),

  
]
# --- IGNORE ---