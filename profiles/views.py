from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.utils import simplejson as json

from profiles.models import UserProfile
from profiles.forms import EmailSignupForm, EmailLoginForm
from profiles.utils import create_nb_user


def other_profile(request, template):
    ctxt = dict()
    return render(request, template, ctxt)


@require_POST
def login_view(request):
    form = EmailLoginForm(request.POST)
    email = form.data.get('email')
    password = form.data.get('password')

    if not form.is_valid():
        error_msg = form.errors['email'][0]
        return HttpResponseBadRequest(json.dumps(error_msg), mimetype="application/json")

    user = User.objects.get(email__iexact=email)
    auth_user = authenticate(username=user.username, password=password)
    if auth_user is None or not auth_user.is_active:
        error_msg = "Bad authentication"
        return HttpResponseBadRequest(json.dumps(error_msg), mimetype="application/json")

    login(request, auth_user)
    return HttpResponse(json.dumps('/my/profile/'), mimetype="application/json")

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

        request.session['show_signup_sys_msg'] = True
        return HttpResponse(json.dumps('/my/profile/'), mimetype="application/json")

    error_msg = form.errors['email'][0]
    return HttpResponseBadRequest(json.dumps(error_msg), mimetype="application/json")

