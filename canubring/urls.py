from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(regex=r'^$', view='website.views.home', name='home', kwargs = {'template': 'search.html',}),
    url(r'^my/', include('website.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^facebook/', include('django_facebook.urls')),
    # url(r'^auth/', include('django_facebook.auth_urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

