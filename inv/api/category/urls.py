
from django.contrib import admin
from django.urls import path
from .views import  category_list , category_create , delete_category  , edit_category


app_name = 'category'


urlpatterns = [
   path('list/', category_list, name='category_list'),
   path('create/', category_create, name='category_create'),
   path('delete/<int:pk>/', delete_category, name='delete_category'),
   path('edit/<int:pk>/', edit_category, name='edit_category'),

    
]
    