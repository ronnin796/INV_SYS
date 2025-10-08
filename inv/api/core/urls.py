
from django.contrib import admin
from django.urls import path
from .views import  fonttest
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    path('font/', fonttest , name='fonttest'),
    
]
    