from django.shortcuts import redirect, get_object_or_404

from trips.models import Trip
from cargos.models import Cargo


def ask_for_cargo(request):
    content = request.POST.get('content', None)
    cargo_id = request.POST.get('cargo_id', None)
    if not content:
        return redirect('home')
    trip = get_object_or_404(Trip, id=cargo_id)
    cargo, created = Cargo.objects.get_or_create(trip=trip, requesting_user=request.user, traveller_user=trip.user)
    cargo.cargocomment_set.create(user=request.user, content=content)
    return redirect('cargos')

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

