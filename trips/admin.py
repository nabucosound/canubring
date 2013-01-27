from django.contrib import admin
from trips.models import Trip


class TripAdmin(admin.ModelAdmin):
    list_display = ('departure_city', 'departure_dt', 'destination_city', 'destination_dt')
    search_fields = ('departure_city', 'destination_city')

admin.site.register(Trip, TripAdmin)

