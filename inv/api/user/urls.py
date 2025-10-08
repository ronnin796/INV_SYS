
from django.contrib import admin
from django.urls import path
from .views import  logout_view , inbox
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from . import views
from .forms import LoginForm

app_name = 'user'

urlpatterns = [
    path("",  auth_views.LoginView.as_view(template_name='user/login.html',authentication_form=LoginForm , redirect_authenticated_user=True,next_page='dashboard:dashboard') , name='login' ),
    path('inbox/', inbox , name='inbox'),
    path('signup/', views.signup , name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html',authentication_form=LoginForm , redirect_authenticated_user=True,next_page='dashboard:dashboard') , name='login' ),
    path('logout/', logout_view, name='logout'),
    path('awaiting_approval/', views.awaiting_approval, name='awaiting_approval'),
]
    