from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required

from trips.models import Trip


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def listing(request, trip_list):
    paginator = Paginator(trip_list, 2) # Show 25 trips per page

    page = request.GET.get('page')
    try:
        trips = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        trips = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        trips = paginator.page(paginator.num_pages)
    return trips

def logout(request):
    django_logout(request)
    return redirect('/')

def home(request, template):
    ctxt = dict()
    ctxt['trip_results'] = Trip.objects.order_by('-creation_dt')
    return render(request, template, ctxt)

@login_required
def profile(request, template):
    ctxt = dict()
    ctxt['profile'] = request.user.userprofile
    if request.session.pop('show_signup_sys_msg', False):
        ctxt['show_signup_sys_msg'] = True
    return render(request, template, ctxt)

@login_required
def trips(request, template):
    ctxt = dict()
    ctxt['current_trips'] = listing(request, request.user.userprofile.current_trips)
    ctxt['past_trips'] = listing(request, request.user.userprofile.past_trips)
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

