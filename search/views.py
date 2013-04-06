import datetime

from django.shortcuts import render
from django.db.models import Q

from trips.models import Trip
from website.utils import listing


def search(request, template):
    ctxt = dict()
    now = datetime.datetime.now()
    trip_results = Trip.objects.filter(departure_dt__gte=now).order_by('departure_dt')

    departure_complex_lookup = None
    departure = request.GET.get('departure', None)
    if departure:
        dep_city = departure.split(',')[0].strip()
        # dep_country = departure.split(',')[-1].strip()
        #departure_complex_lookup = (Q(dep_city__name__iexact=dep_city) | Q(dep_country__name__iexact=dep_country))
        departure_complex_lookup = (Q(dep_city__name__iexact=dep_city))

    destination_complex_lookup = None
    destination = request.GET.get('destination', None)
    if destination:
        dest_city = destination.split(',')[0].strip()
        # dest_country = destination.split(',')[-1].strip()
        # destination_complex_lookup = (Q(dest_city__name__iexact=dest_city) | Q(dest_country__name__iexact=dest_country))
        destination_complex_lookup = (Q(dest_city__name__iexact=dest_city))

    if departure_complex_lookup:
        trip_results = trip_results.filter(departure_complex_lookup)
    if destination_complex_lookup:
        trip_results = trip_results.filter(destination_complex_lookup)

    arrival = request.GET.get('arrival', None)
    if arrival:
        try:
            date = datetime.datetime.strptime(arrival, "%m/%d/%Y")
        except ValueError:
            pass
        else:
            trip_results = trip_results.filter(destination_dt__year=date.year, destination_dt__month=date.month, destination_dt__day=date.day)

    trips = listing(request, trip_results)
    col = trips.object_list.count() / 4
    ctxt['trips_col1'] = trips.object_list[:col]
    ctxt['trips_col2'] = trips.object_list[col:col+col]
    ctxt['trips_col3'] = trips.object_list[col+col:col+col+col]
    ctxt['trips_col4'] = trips.object_list[col+col+col:]
    return render(request, template, ctxt)

