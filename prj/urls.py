from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from tastypie.api import Api

from trips.api import TripResource, UserResource


admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(TripResource())
v1_api.register(UserResource())

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # App
    url(regex=r'^$', view='search.views.search', name='home', kwargs = {'template': 'search.html',}),
    url(r'^logout/$', 'website.views.logout', name='logout'),
    url(r'^my/', include('website.urls')),
    url(r'^profiles/', include('profiles.urls')),
    url(r'^api/', include(v1_api.urls)),
    url(regex=r'^auth/signup/email/$', view='profiles.views.signup_view', name='signup_email'),
    url(regex=r'^auth/login/email/$', view='profiles.views.login_view', name='login_email'),
    url(r'auth/', include('social_auth.urls')),
    url(regex=r'^search/$', view='search.views.search', name='search', kwargs = {'template': 'search.html',}),
    url(r'cargos/', include('cargos.urls')),
    url(r'^password/', include('password_reset.urls')),

    # Static pages
    url(r'^how-it-works/', TemplateView.as_view(template_name="how_works.html"), name='how_works'),
    url(r'^earn-carrying/', TemplateView.as_view(template_name="earn_carrying.html"), name='earn_carrying'),
    url(r'^safety-warranty/', TemplateView.as_view(template_name="safety_warranty.html"), name='safety_warranty'),
    url(r'^recommend/', TemplateView.as_view(template_name="recommend.html"), name='recommend'),
    url(r'^reference-prices/', TemplateView.as_view(template_name="reference_prices.html"), name='reference_prices'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

