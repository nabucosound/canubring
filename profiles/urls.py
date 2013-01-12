from django.conf.urls import patterns, url


urlpatterns = patterns('profiles.views',
    url(
        # regex=r'^(?P<user_id>\d+)/$',
        regex=r'^$',
        view='other_profile',
        name='other_profile',
        kwargs = {'template': 'other_profile.html'}
    ),
)

