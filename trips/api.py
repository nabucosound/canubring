from django.contrib.auth.models import User

from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization

from trips.models import Trip
from cities_light.models import Country, City


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'first_name', 'last_name', 'last_login']
        allowed_methods = ['get']


class CountryResource(ModelResource):
    class Meta:
        queryset = Country.objects.all()
        resource_name = 'country'
        authorization= Authorization()


class CityResource(ModelResource):
    class Meta:
        queryset = City.objects.all()
        resource_name = 'city'
        authorization= Authorization()


class TripResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    dep_country = fields.ForeignKey(CountryResource, 'dep_country', full=True)
    dep_city = fields.ForeignKey(CityResource, 'dep_city', full=True)
    dest_country = fields.ForeignKey(CountryResource, 'dest_country', full=True)
    dest_city = fields.ForeignKey(CityResource, 'dest_city', full=True)

    class Meta:
        queryset = Trip.objects.all()
        resource_name = 'trip'
        authorization= Authorization()

    def hydrate(self, bundle, request=None):
        bundle.obj.dep_country = Country.objects.get(pk = bundle.data['dep_country'])
        bundle.obj.dep_city = City.objects.get(pk = bundle.data['dep_city'])
        bundle.obj.dest_country = Country.objects.get(pk = bundle.data['dest_country'])
        bundle.obj.dest_city = City.objects.get(pk = bundle.data['dest_city'])
        bundle.data['dep_country'] = "/api/v1/country/%s/" % bundle.data['dep_country']
        bundle.data['dep_city'] = "/api/v1/city/%s/" % bundle.data['dep_city']
        bundle.data['dest_country'] = "/api/v1/country/%s/" % bundle.data['dest_country']
        bundle.data['dest_city'] = "/api/v1/city/%s/" % bundle.data['dest_city']
        return bundle

