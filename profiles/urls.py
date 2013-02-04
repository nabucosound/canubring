from django.conf.urls import patterns, url


urlpatterns = patterns('profiles.views',
    url(
        regex=r'^$',
        view='other_profile',
        name='other_profile',
        kwargs = {'template': 'other_profile.html'}
    ),
    url(
        regex=r'^update/$',
        view='update_profile',
        name='update_profile',
    ),
)

