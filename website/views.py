from django.shortcuts import render


def home(request, template):
    ctxt = dict()
    return render(request, template, ctxt)

def profile(request, template):
    ctxt = dict()
    return render(request, template, ctxt)

def trips(request, template):
    ctxt = dict()
    return render(request, template, ctxt)

def new_trip(request, template):
    ctxt = dict()
    from trips.forms import NewTrip
    form = NewTrip()
    ctxt['form'] = form
    return render(request, template, ctxt)

