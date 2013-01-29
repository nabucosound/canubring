from django.shortcuts import render
from django.db.models import Q

from trips.models import Trip


def search(request, template):
    ctxt = dict()
    trip_results = Trip.objects.order_by('-creation_dt')

    departure_complex_lookup = None
    departure = request.GET.get('departure', None)
    if departure:
        departure_complex_lookup = (Q(dep_city__name__icontains=departure) | Q(dep_country__name__icontains=departure))

    destination_complex_lookup = None
    destination = request.GET.get('destination', None)
    if destination:
        destination_complex_lookup = (Q(dest_city__name__icontains=destination) | Q(dest_country__name__icontains=destination))

    if departure_complex_lookup:
        trip_results = trip_results.filter(departure_complex_lookup)
    if destination_complex_lookup:
        trip_results = trip_results.filter(destination_complex_lookup)

    ctxt['trip_results'] = trip_results
    return render(request, template, ctxt)

