from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson as json

from trips.models import Trip
from cargos.models import Cargo


@login_required
def ask_for_cargo(request):
    content = request.POST.get('content', None)
    cargo_id = request.POST.get('cargo_id', None)
    if not content:
        return redirect('home')
    trip = get_object_or_404(Trip, id=cargo_id)
    cargo, created = Cargo.objects.get_or_create(trip=trip, requesting_user=request.user, traveller_user=trip.user)
    cargo.cargocomment_set.create(user=request.user, content=content)
    return redirect('cargos')

@login_required
def reply_cargo(request, template='trips'):
    content = request.POST.get('content', None)
    cargo_id = request.POST.get('cargo_id', None)
    if request.POST.get('from_my_cargos', False):
        template = 'cargos'
    if not content:
        return redirect('home')
    cargo = get_object_or_404(Cargo, id=cargo_id)
    cargo.cargocomment_set.create(user=request.user, content=content)
    return redirect(template)

@login_required
def update_unread_status(request, cargo_id):
    user = request.user
    cargo = get_object_or_404(Cargo, traveller_user=user, id=cargo_id)
    cargo.cargocomment_set.exclude(user=request.user).update(unread=False)
    return HttpResponse(json.dumps('OK'), mimetype="application/json")

