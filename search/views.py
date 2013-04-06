import datetime

from django.shortcuts import render
from django.db.models import Q

from trips.models import Trip, Country, City
from website.utils import listing


def search(request, template):
    ctxt = dict()
    now = datetime.datetime.now()
    trip_results = Trip.objects.filter(departure_dt__gte=now).order_by('departure_dt')
    active_countries = Country.objects.filter(Q(dep_country_trips__in=trip_results) | Q(dest_country_trips__in=trip_results)).distinct().order_by('name')
    active_cities = City.objects.filter(Q(dep_city_trips__in=trip_results) | Q(dest_city_trips__in=trip_results)).distinct().order_by('name')
    ctxt['active_countries'] = active_countries
    ctxt['active_cities'] = active_cities

    departure_country_complex_lookup = None
    departure_country = request.GET.get('departure_country', None)
    if departure_country:
        dep_country = departure_country.split(',')[0].strip()
        departure_country_complex_lookup = (Q(dep_country__id=dep_country))

    destination_country_complex_lookup = None
    destination_country = request.GET.get('destination_country', None)
    if destination_country:
        dest_country = destination_country.split(',')[0].strip()
        destination_country_complex_lookup = (Q(dest_country__id=dest_country))

    departure_city_complex_lookup = None
    departure_city = request.GET.get('departure_city', None)
    if departure_city:
        dep_city = departure_city.split(',')[0].strip()
        departure_city_complex_lookup = (Q(dep_city__id=dep_city))

    destination_city_complex_lookup = None
    destination_city = request.GET.get('destination_city', None)
    if destination_city:
        dest_city = destination_city.split(',')[0].strip()
        destination_city_complex_lookup = (Q(dest_city__id=dest_city))

    if departure_country_complex_lookup:
        trip_results = trip_results.filter(departure_country_complex_lookup)
    if destination_country_complex_lookup:
        trip_results = trip_results.filter(destination_country_complex_lookup)
    if departure_city_complex_lookup:
        trip_results = trip_results.filter(departure_city_complex_lookup)
    if destination_city_complex_lookup:
        trip_results = trip_results.filter(destination_city_complex_lookup)

    # arrival = request.GET.get('arrival', None)
    # if arrival:
    #     try:
    #         date = datetime.datetime.strptime(arrival, "%m/%d/%Y")
    #     except ValueError:
    #         pass
    #     else:
    #         trip_results = trip_results.filter(destination_dt__year=date.year, destination_dt__month=date.month, destination_dt__day=date.day)

    trips = listing(request, trip_results)
    ctxt['trips'] = trips
    return render(request, template, ctxt)

