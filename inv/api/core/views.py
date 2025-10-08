from django.shortcuts import render

# Create your views here.
def fonttest(request):
    return render(request, 'core/fonttest.html')