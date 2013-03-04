from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required

from website.utils import listing

def logout(request):
    django_logout(request)
    return redirect('/')

@login_required
def profile(request, template):
    ctxt = dict()
    ctxt['profile'] = request.user.userprofile
    if request.session.pop('show_signup_sys_msg', False):
        ctxt['show_signup_sys_msg'] = True
    return render(request, template, ctxt)

@login_required
def trips(request, template, profile_attr='current_trips'):
    ctxt = dict()
    ctxt['trips'] = listing(request, getattr(request.user.userprofile, profile_attr))
    ctxt['past_trips'] = profile_attr == 'past_trips'
    return render(request, template, ctxt)

@login_required
def new_trip(request, template):
    ctxt = dict()
    return render(request, template, ctxt)

@login_required
def cargos(request, template):
    ctxt = dict()
    ctxt['my_cargos'] = True
    return render(request, template, ctxt)

@login_required
def evaluations(request, template):
    ctxt = dict()
    return render(request, template, ctxt)

