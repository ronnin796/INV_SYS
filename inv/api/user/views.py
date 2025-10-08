from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse , JsonResponse
from django.urls import reverse


from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from django.contrib import messages
# Create your views here.

from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
def logout_view(request):
    logout(request)  # clears the session
    return redirect('user:login')

def signup(request):
    if request.method =='POST':
        form = SignupForm(request.POST  )

        if form.is_valid():
            form.save()
            messages.success(request, "Signup successful! Await admin approval.")
            return redirect('user/login/')
    else:
        form = SignupForm()

    return render(request , 'user/signup.html', {'form':form})

def awaiting_approval(request):
    return HttpResponse("Your account is awaiting admin approval.")

def inbox(request):
    return HttpResponse("Welcome to your inbox!")