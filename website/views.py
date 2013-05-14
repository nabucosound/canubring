from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.utils import translation
from django.conf import settings

from website.utils import listing
from profiles.models import ProfileCountry

def set_language_from_get_request(request, lang):
    # lang = kwargs['lang']
    for language in settings.LANGUAGES:
        if language[0] == lang:
            request.session['django_language'] = lang
            translation.activate(lang)
            request.LANGUAGE_CODE = translation.get_language()
    return redirect('home')

def logout(request):
    django_logout(request)
    return redirect('/')

@login_required
def profile(request, template):
    ctxt = dict()
    ctxt['profile'] = request.user.userprofile
    if request.session.pop('show_signup_sys_msg', False):
        ctxt['show_signup_sys_msg'] = True
    if request.session.pop('show_email_verified_sys_msg', False):
        ctxt['show_email_verified_sys_msg'] = True
    ctxt['profile_countries'] = ProfileCountry.objects.all()
    return render(request, template, ctxt)

@login_required
def trips(request, template, profile_attr='current_trips'):
    ctxt = dict()
    ctxt['trips'] = listing(request, getattr(request.user.userprofile, profile_attr))
    ctxt['past_trips'] = profile_attr == 'past_trips'
    if request.GET.get('m') == '1':
        ctxt['show_new_trip_sys_msg'] = True
    return render(request, template, ctxt)

@login_required
def new_trip(request, template):
    ctxt = dict()
    return render(request, template, ctxt)

@login_required
def cargos(request, template, profile_attr='current_cargos'):
    ctxt = dict()
    ctxt['my_cargos'] = True
    ctxt['cargos'] = listing(request, getattr(request.user.userprofile, profile_attr))
    ctxt['past_cargos'] = profile_attr == 'past_cargos'
    return render(request, template, ctxt)

@login_required
def evaluations(request, template, profile_attr='get_reviews_about_me'):
    ctxt = dict()
    ctxt['reviews'] = listing(request, getattr(request.user.userprofile, profile_attr))
    ctxt['reviews_by_me'] = profile_attr == 'get_all_reviews_by_me'
    return render(request, template, ctxt)

@login_required
def delete_account(request):
    user = request.user
    user.is_active = False
    user.save()
    django_logout(request)
    return redirect('/')

