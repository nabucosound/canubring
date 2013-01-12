from django.shortcuts import render


def home(request, template):
    ctxt = dict()
    return render(request, template, ctxt)

