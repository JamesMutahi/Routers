from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from web.forms import SearchForm
from web.models import Route, Sacco


def landing_page(request):
    # redirect to home page if user is already logged in
    if request.user.is_authenticated:
        return redirect(home)
    # renders landing page, html file in web/templates directory
    return render(request, 'web/landing-page.html')


@login_required()
def home(request):
    form = SearchForm()
    location = None
    destination = None
    routes = []
    if 'destination' in request.GET or 'location' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            # Get data from form
            destination = form.cleaned_data['destination']
            location = form.cleaned_data['location']
            # filter routes by similarity to location (starting_point)
            routes = Route.objects.annotate(
                similarity=TrigramSimilarity('starting_point', location),
            ).filter(similarity__gt=0.3).order_by('-similarity')
            # filter saccos by similarity to destination (ending_point)
            saccos = Sacco.objects.annotate(
                similarity=TrigramSimilarity('ending_point', destination),
            ).filter(similarity__gt=0.3).order_by('-similarity')
            # filter routes by saccos with the destination
            routes = routes.filter(saccos__in=saccos)
            # Save sacco ids; will fetch this when viewing route detail to remove saccos not going to the destination
            sacco_ids = []
            for sacco in saccos:
                sacco_ids.append(sacco.id)
            request.session['sacco_ids'] = sacco_ids
    context = {'form': form, 'location': location, 'destination': destination, 'routes': routes, 'title': 'Search'}
    return render(request, 'web/search.html', context)


class RouteDetailView(DetailView):
    # This class based view is handled by django
    # html template by default is route-detail.html
    model = Route

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        route = Route.objects.get(id=self.kwargs['pk'])
        context['saccos'] = route.saccos.filter(id__in=self.request.session.get('sacco_ids'))
        return context
