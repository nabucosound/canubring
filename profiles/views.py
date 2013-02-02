from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import authenticate, login
# from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponse
# from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
# from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json

from profiles.models import UserProfile
from profiles.forms import EmailSignupForm
from profiles.utils import create_nb_user


def other_profile(request, template):
    ctxt = dict()
    return render(request, template, ctxt)


@require_POST
def signup_view(request):
    form = EmailSignupForm(request.POST)
    email = form.data.get('email')
    password = form.data.get('password')

    if form.is_valid():
        # Create User and Profile
        user = create_nb_user(email, password)
        user = authenticate(username=user.username, password=password)
        user.userprofile = UserProfile.objects.create(user=user)
        user.first_name = user.email
        user.save()
        login(request, user)

        # Send welcome email
        if getattr(settings, 'SEND_EMAIL_NOTIFICATIONS', False):
            from boto.ses.exceptions import SESAddressNotVerifiedError
            try:
                pass  # TODO
                # send_welcome_email(request)
            except SESAddressNotVerifiedError:
                pass

        # messages.success(request, "Welcome!")
        return HttpResponse(json.dumps('/'), mimetype="application/json")

    error_msg = form.errors['email'][0]
    # messages.error(request, error_msg)
    return HttpResponseBadRequest(json.dumps(error_msg), mimetype="application/json")

