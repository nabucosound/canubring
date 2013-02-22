from django.conf.urls import patterns, url


urlpatterns = patterns('cargos.views',
    url(
        regex=r'^ask/$',
        view='ask_for_cargo',
        name='ask_for_cargo',
    ),
)

