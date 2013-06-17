from django.contrib import admin
from trips.models import Trip


class TripAdmin(admin.ModelAdmin):
    list_display = ('user', 'dep_country', 'dep_city', 'dest_country', 'dest_city', 'destination_dt', 'travelling_by')
    search_fields = ('dep_country__name', 'dep_city__name', 'dest_country__name', 'dest_city__name', 'comments')
    raw_id_fields = ('user', 'dep_country', 'dep_city', 'dest_country', 'dest_city')

admin.site.register(Trip, TripAdmin)

