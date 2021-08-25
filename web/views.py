from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import render

from web.forms import SearchForm
from web.models import Route


def landing_page(request):
    # renders landing page, html file in web/templates directory
    return render(request, 'web/landing-page.html')


# def home(request):
#     context = {
#         'posts': Route.objects.all()
#     }
#     return render(request, 'web/home.html', context)


def home(request):
    form = SearchForm()
    location = None
    destination = None
    results = []
    if 'destination' in request.GET or 'location' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            destination = form.cleaned_data['destination']
            location = form.cleaned_data['location']
            results = Route.objects.annotate(
                similarity=TrigramSimilarity('name', location + destination),
            ).filter(similarity__gt=0.3).order_by('-similarity')
    return render(request, 'web/search.html',
                  {'form': form, 'location': location, 'destination': destination, 'results': results,
                   'title': 'Search'})
