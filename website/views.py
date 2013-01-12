from django.shortcuts import render


def home(request, template):
    ctxt = dict()
    return render(request, template, ctxt)

def profile(request, template):
    ctxt = dict()
    return render(request, template, ctxt)

def new_trip(request, template):
    ctxt = dict()
    return render(request, template, ctxt)

