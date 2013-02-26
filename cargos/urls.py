from django.conf.urls import patterns, url


urlpatterns = patterns('cargos.views',
    url(
        regex=r'^ask/$',
        view='ask_for_cargo',
        name='ask_for_cargo',
    ),
    url(
        regex=r'^reply/$',
        # view='reply_cargo',
        view='submit_new_comment',
        name='reply_cargo',
    ),
    url(
        regex=r'^update-unread-status/(?P<cargo_id>\d+)/$',
        view='update_unread_status',
        name='update_unread_status',
    ),
)

