import json
from django.core.serializers import json as django_json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geos import Point
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView

from web.models import Route, Commute, Sacco


def landing_page(request):
    # redirect to home page if user is already logged in
    if request.user.is_authenticated:
        return redirect(home)
    # renders landing page, html file in web/templates directory
    return render(request, 'web/landing-page.html')


@login_required()
def home(request):
    return render(request, 'web/home.html')


@login_required()
@csrf_exempt
def search(request):
    if request.method == "POST":
        route = json.loads(request.POST["route"])
        # save route to session
        request.session['route'] = route
        # create Point A
        point_a = Point(route["inputWaypoints"][0]["latLng"]["lng"], route["inputWaypoints"][0]["latLng"]["lat"],
                        srid=4326)
        # create Point B
        point_b = Point(route["inputWaypoints"][1]["latLng"]["lng"], route["inputWaypoints"][1]["latLng"]["lat"],
                        srid=4326)
        sacco_ids = []

        # 0.008 degrees is roughly a kilometre in radius
        # Get all saccos and routes getting on point A
        point_a_saccos = Sacco.objects.filter(ending_point__dwithin=(point_a, 0.050))
        point_a_routes = Route.objects.filter(starting_point__dwithin=(point_a, 0.050))

        # Get all saccos and routes getting on point B
        point_b_saccos = Sacco.objects.filter(ending_point__dwithin=(point_b, 0.050))
        point_b_routes = Route.objects.filter(starting_point__dwithin=(point_b, 0.050))
        # Filter the saccos and routes by those getting on point B
        for route in point_a_routes:
            for sacco in route.saccos.all():
                if sacco in point_b_saccos:
                    sacco_ids.append(sacco.id)
        for route in point_b_routes:
            for sacco in route.saccos.all():
                if sacco in point_a_saccos:
                    sacco_ids.append(sacco.id)
        data = dict()
        saccos = Sacco.objects.filter(id__in=sacco_ids)
        json_serializer = django_json.Serializer()
        json_serialized = json_serializer.serialize(saccos)
        data["saccos"] = json_serialized
        return JsonResponse(data)


class RouteDetailView(DetailView, LoginRequiredMixin):
    # This class based view is handled by django
    # html template by default is route-detail.html
    model = Route

    # override get_context_data method to pass in only saccos on the chosen route that have the destination
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the chosen route
        route = Route.objects.get(id=self.kwargs['pk'])
        # filter saccos on route to only show ones with the destination
        context['saccos'] = route.saccos.filter(id__in=self.request.session.get('sacco_ids'))
        return context


class CommuteCreateView(LoginRequiredMixin, CreateView):
    model = Commute
    fields = ['pickup_point', 'drop_off_point', ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
