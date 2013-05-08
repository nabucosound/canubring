from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from profiles.views import EmailSettingsView, PasswordSettingsView


urlpatterns = patterns('profiles.views',
    url(
        regex=r'^(?P<user_id>\d+)/$',
        view='other_profile',
        name='other_profile',
        kwargs = {'template': 'profile.html'}
    ),
    url(
        regex=r'^update/$',
        view='update_profile',
        name='update_profile',
    ),
    url(
        regex=r'^update/social/$',
        view='update_social',
        name='update_social',
    ),
    url(
        regex=r'^avatar/new/$',
        view='upload_profile_picture',
        name='upload_profile_picture',
    ),
    url(
        regex=r'^verify/email/(?P<token>[\w:-]+)/$',
        view='verify_email',
        name='verify_email',
        kwargs = {'template': 'verify_email.html'}
    ),
    url(r'^settings/$', login_required(EmailSettingsView.as_view()), name='settings'),
    url(r'^settings/email/$', login_required(EmailSettingsView.as_view()), name='settings_email'),
    url(r'^settings/password/$', login_required(PasswordSettingsView.as_view()), name='password_settings'),
)

