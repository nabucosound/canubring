from django.contrib import admin
from trips.models import Trip


class TripAdmin(admin.ModelAdmin):
    list_display = ('departure_city', 'destination_city', 'destination_dt', 'travelling_by', 'comments')
    search_fields = ('departure_city', 'destination_city', 'comments')

admin.site.register(Trip, TripAdmin)

