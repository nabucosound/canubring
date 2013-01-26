from django.conf.urls import patterns, url


urlpatterns = patterns('website.views',
    url(
        regex=r'^profile/$',
        view='profile',
        name='profile',
        kwargs = {'template': 'profile.html'}
    ),
    url(
        regex=r'^trips/$',
        view='trips',
        name='trips',
        kwargs = {'template': 'trips.html'}
    ),
    url(
        regex=r'^newtrip/$',
        view='new_trip',
        name='new_trip',
        kwargs = {'template': 'new_trip.html'}
    ),
    url(
        regex=r'^cargos/$',
        view='cargos',
        name='cargos',
        kwargs = {'template': 'cargos.html'}
    ),
    url(
        regex=r'^evaluations/$',
        view='evaluations',
        name='evaluations',
        kwargs = {'template': 'evaluations.html'}
    ),
)

