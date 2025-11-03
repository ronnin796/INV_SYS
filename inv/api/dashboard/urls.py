

from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from .views import dashboard , stock_debug_view

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard , name='dashboard'),
    path("stock-debug/", stock_debug_view, name="stock_debug"),
]

