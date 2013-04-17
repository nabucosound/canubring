import datetime

from django.shortcuts import render
from django.db.models import Q

from trips.models import Trip, Country, City
from website.utils import listing


def search(request, template):
    ctxt = dict()
    now = datetime.datetime.now()
    trip_results = Trip.objects.filter(destination_dt__gte=now).order_by('destination_dt')

    active_dep_countries = Country.objects.filter(dep_country_trips__in=trip_results).distinct().order_by('name')
    active_dest_countries = Country.objects.filter(dest_country_trips__in=trip_results).distinct().order_by('name')
    ctxt['active_dep_countries'] = active_dep_countries
    ctxt['active_dest_countries'] = active_dest_countries

    departure_country_complex_lookup = None
    departure_country = request.GET.get('departure_country', None)
    if departure_country:
        ctxt['departure_country'] = int(departure_country)
        departure_country_complex_lookup = (Q(dep_country__id=departure_country))

    destination_country_complex_lookup = None
    destination_country = request.GET.get('destination_country', None)
    if destination_country:
        ctxt['destination_country'] = int(destination_country)
        destination_country_complex_lookup = (Q(dest_country__id=destination_country))

    departure_city_complex_lookup = None
    departure_city = request.GET.get('departure_city', None)
    if departure_city:
        ctxt['departure_city'] = int(departure_city)
        departure_city_complex_lookup = (Q(dep_city__id=departure_city))

    destination_city_complex_lookup = None
    destination_city = request.GET.get('destination_city', None)
    if destination_city:
        ctxt['destination_city'] = int(destination_city)
        destination_city_complex_lookup = (Q(dest_city__id=destination_city))

    if departure_country_complex_lookup:
        trip_results = trip_results.filter(departure_country_complex_lookup)
    if destination_country_complex_lookup:
        trip_results = trip_results.filter(destination_country_complex_lookup)
    if departure_city_complex_lookup:
        trip_results = trip_results.filter(departure_city_complex_lookup)
    if destination_city_complex_lookup:
        trip_results = trip_results.filter(destination_city_complex_lookup)

    active_dep_cities = City.objects.filter(dep_city_trips__in=trip_results).distinct().order_by('name')
    active_dest_cities = City.objects.filter(dest_city_trips__in=trip_results).distinct().order_by('name')
    ctxt['active_dep_cities'] = active_dep_cities
    ctxt['active_dest_cities'] = active_dest_cities

    trips = listing(request, trip_results)
    ctxt['trips'] = trips
    return render(request, template, ctxt)

