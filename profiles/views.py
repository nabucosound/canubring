from django.shortcuts import render


def other_profile(request, template):
    ctxt = dict()
    return render(request, template, ctxt)

