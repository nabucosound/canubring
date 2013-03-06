from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class CompleteRegistration(object):
    def process_request(self, request):
        if request.user.is_authenticated() and not request.user.is_superuser:
            profile_url = reverse('profile')
            update_profile_url = reverse('update_profile')
            try:
                profile = request.user.userprofile
            except User.DoesNotExist:
                return None
            if not profile.completed:
                if request.META['PATH_INFO'] in (profile_url, update_profile_url):
                    if request.META['PATH_INFO']  == update_profile_url:
                        return None
                    if request.META['PATH_INFO'] == profile_url and request.META['QUERY_STRING'] == 'profile=1':
                        return None
                return HttpResponseRedirect("%s?profile=1" % profile_url)
        return None



