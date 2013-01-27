from tastypie.resources import ModelResource
from trips.models import Trip


class TripResource(ModelResource):
    class Meta:
        queryset = Trip.objects.all()
        resource_name = 'trip'

