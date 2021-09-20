import json
from django.core.serializers import json as django_json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geos import Point
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView

from web.models import Route, Commute, Sacco, BusStop


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

        # create Point A
        point_a = Point(route["inputWaypoints"][0]["latLng"]["lng"], route["inputWaypoints"][0]["latLng"]["lat"],
                        srid=4326)
        # create Point B
        point_b = Point(route["inputWaypoints"][1]["latLng"]["lng"], route["inputWaypoints"][1]["latLng"]["lat"],
                        srid=4326)

        sacco_ids = []

        # 0.008 degrees is roughly a kilometre in radius
        # Get all saccos and routes getting on point A
        point_a_saccos = Sacco.objects.filter(ending_point__dwithin=(point_a, 0.090))
        point_a_routes = Route.objects.filter(starting_point__dwithin=(point_a, 0.090))

        # Get all saccos and routes getting on point B
        point_b_saccos = Sacco.objects.filter(ending_point__dwithin=(point_b, 0.090))
        point_b_routes = Route.objects.filter(starting_point__dwithin=(point_b, 0.090))

        # Filter the saccos and routes by those getting on point B
        for route in point_a_routes:
            for sacco in route.saccos.all():
                if sacco in point_b_saccos:
                    sacco_ids.append(sacco.id)
        for route in point_b_routes:
            for sacco in route.saccos.all():
                if sacco in point_a_saccos:
                    sacco_ids.append(sacco.id)

        # Get Bus Stops within point B
        point_b_bus_stops = BusStop.objects.filter(point__dwithin=(point_b, 0.090))


        data = dict()
        saccos = Sacco.objects.filter(id__in=sacco_ids)
        json_serializer = django_json.Serializer()
        json_serialized = json_serializer.serialize(saccos)
        data["saccos"] = json_serialized
        return JsonResponse(data)
