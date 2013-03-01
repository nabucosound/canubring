from django.conf.urls import patterns, url


urlpatterns = patterns('cargos.views',
    url(
        regex=r'^ask/$',
        view='ask_for_cargo',
        name='ask_for_cargo',
    ),
    url(
        regex=r'^reply/$',
        view='submit_new_comment',
        name='reply_cargo',
    ),
    url(
        regex=r'^update-unread-status/(?P<cargo_id>\d+)/$',
        view='update_unread_status',
        name='update_unread_status',
    ),
    url(
        regex=r'^cargo-form/(?P<cargo_id>\d+)/$',
        view='cargo_form',
        name='cargo_form',
    ),
    url(
        regex=r'^cargo-form/submit/$',
        view='submit_cargo_form',
        name='submit_cargo_form',
    ),
    url(
        regex=r'^confirm-cargo-form/(?P<cargo_id>\d+)/$',
        view='confirm_cargo_form',
        name='confirm_cargo_form',
    ),
    url(
        regex=r'^confirm-cargo-form/submit/$',
        view='submit_confirm_cargo_form',
        name='submit_confirm_cargo_form',
    ),
    url(
        regex=r'^reject-cargo-form/submit/$',
        view='submit_reject_cargo_form',
        name='submit_reject_cargo_form',
    ),
    url(
        regex=r'^review-traveller-form/(?P<cargo_id>\d+)/$',
        view='review_traveller_form',
        name='review_traveller_form',
    ),
)

