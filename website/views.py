from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout

from trips.models import Trip


def logout(request):
    django_logout(request)
    return redirect('/')

def home(request, template):
    ctxt = dict()
    ctxt['trip_results'] = Trip.objects.order_by('-creation_dt')
    return render(request, template, ctxt)

def profile(request, template):
    ctxt = dict()
    ctxt['profile'] = request.user.userprofile
    if request.session.pop('show_signup_sys_msg', False):
        ctxt['show_signup_sys_msg'] = True

    return render(request, template, ctxt)

def trips(request, template):
    ctxt = dict()
    return render(request, template, ctxt)

def new_trip(request, template):
    ctxt = dict()
    return render(request, template, ctxt)

def cargos(request, template):
    ctxt = dict()
    ctxt['my_cargos'] = True
    return render(request, template, ctxt)

def evaluations(request, template):
    ctxt = dict()
    return render(request, template, ctxt)

