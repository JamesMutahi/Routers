from django.shortcuts import render


def home(request):
    # renders home page
    return render(request, 'home.html')
