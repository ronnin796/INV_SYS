
from django.contrib import admin
from django.urls import path
from .views import  subcategory_list , subcategory_create , delete_subcategory  , edit_subcategory


app_name = 'subcategory'


urlpatterns = [
   path('list/<int:pk>/', subcategory_list, name='subcategory_list'),
   path('create/', subcategory_create, name='subcategory_create'),
   path('delete/<int:pk>/', delete_subcategory, name='delete_subcategory'),
   path('edit/<int:pk>/', edit_subcategory, name='edit_subcategory'),

    
]
    