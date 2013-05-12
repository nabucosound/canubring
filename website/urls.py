from django.conf.urls import patterns, url
from django.views.generic import TemplateView


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
        regex=r'^trips/past/$',
        view='trips',
        name='past_trips',
        kwargs = {'template': 'trips.html', 'profile_attr': 'past_trips'}
    ),
    url(
        regex=r'^newtrip/$',
        view='new_trip',
        name='new_trip',
        kwargs = {'template': 'new_trip.html'}
    ),
    url(r'^triplegform/', TemplateView.as_view(template_name="new_trip_leg.html"), name='trip_leg_form'),
    url(
        regex=r'^cargos/$',
        view='cargos',
        name='cargos',
        kwargs = {'template': 'cargos.html'}
    ),
    url(
        regex=r'^cargos/past/$',
        view='cargos',
        name='past_cargos',
        kwargs = {'template': 'cargos.html', 'profile_attr': 'past_cargos'}
    ),
    url(
        regex=r'^evaluations/$',
        view='evaluations',
        name='evaluations',
        kwargs = {'template': 'evaluations.html'}
    ),
    url(
        regex=r'^evaluations/by-me$',
        view='evaluations',
        name='evaluations_by_me',
        kwargs = {'template': 'evaluations.html', 'profile_attr': 'get_all_reviews_by_me'}
    ),
    url(
        regex=r'^delete/account/$',
        view='delete_account',
        name='delete_account',
    ),
)

