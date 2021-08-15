from django.shortcuts import render


def home(request):
    # renders home page, html file in web/templates directory
    return render(request, 'home.html')
