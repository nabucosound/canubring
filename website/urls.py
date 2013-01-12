from django.conf.urls import patterns, url


urlpatterns = patterns('website.views',
    url(
        regex=r'^profile/$',
        view='profile',
        name='profile',
        kwargs = {'template': 'profile.html'}
    ),
    url(
        regex=r'^newtrip/$',
        view='new_trip',
        name='new_trip',
        kwargs = {'template': 'new_trip.html'}
    ),
)

