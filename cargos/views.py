from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.contrib import messages

from trips.models import Trip
from cargos.models import Cargo, CargoComment
from cargos.forms import CargoForm


@login_required
def ask_for_cargo(request):
    content = request.POST.get('content', None)
    cargo_id = request.POST.get('object_id', None)
    if not content:
        return redirect('home')
    trip = get_object_or_404(Trip, id=cargo_id)
    cargo, created = Cargo.objects.get_or_create(trip=trip, requesting_user=request.user, traveller_user=trip.user)
    cargo.cargocomment_set.create(user=request.user, content=content)
    return redirect('cargos')

@login_required
def update_unread_status(request, cargo_id):
    user = request.user
    cargo = get_object_or_404(Cargo, traveller_user=user, id=cargo_id)
    cargo.cargocomment_set.exclude(user=request.user).update(unread=False)
    return HttpResponse(json.dumps('OK'), mimetype="application/json")

@login_required
@require_POST
def submit_new_comment(request, fk_name='cargo', model=Cargo, comment_model=CargoComment):
    """Adds a new comment to an existing object"""
    if request.is_ajax():
        # Validate all POST params are there and are valid
        comment_txt = request.POST.get('content', False)
        object_id = request.POST.get('object_id', False)
        if not comment_txt or not object_id:
            error_msg = 'Error posting comment'
            return HttpResponseBadRequest(json.dumps(error_msg), mimetype="application/json")

        # Get object
        try:
            obj = model.objects.get(id=object_id)
        except model.DoesNotExist:
            error_msg = 'Error posting comment'
            return HttpResponseBadRequest(json.dumps(error_msg), mimetype="application/json")

        # Create new comment
        fields = {
            'user': request.user,
            'content': comment_txt,
        }
        fields[fk_name] = obj
        comment = comment_model.objects.create(**fields)

        # JSON Response
        html = render_to_string('comment.html', {'comment': comment})
        response = {'html': html}
        return HttpResponse(json.dumps(response), mimetype="application/json")

@login_required
def cargo_form(request, cargo_id):
    # JSON Response
    cargo = get_object_or_404(Cargo, id=cargo_id)
    html = render_to_string('modals/cargo_modal_content.html', {'cargo_id': cargo.id})
    response = {'html': html}
    return HttpResponse(json.dumps(response), mimetype="application/json")

@login_required
@require_POST
def submit_cargo_form(request):
    cargo_id = request.POST.get('cargo_id', False)
    if not cargo_id:
        error_msg = 'Error posting cargo form'
        return HttpResponseBadRequest(json.dumps(error_msg), mimetype="application/json")
    cargo = get_object_or_404(Cargo, id=cargo_id)
    categories = ('food', 'medicaments', 'duty_free', 'electronics', 'baggage', 'books', 'documents', 'personal_belongings', 'clothes')
    cats = [request.POST.get(cat, False) for cat in categories]
    active_cats = filter(None, cats)
    if not active_cats:
        error_msg = 'At least one category must be selected'
        return HttpResponseBadRequest(json.dumps(error_msg), mimetype="application/json")
    form = CargoForm(request.POST, instance=cargo)
    if not form.is_valid():
        error_msg = 'Error posting cargo form'
        return HttpResponseBadRequest(json.dumps(error_msg), mimetype="application/json")
    obj = form.save()
    obj.state = 1
    obj.save()
    msg = 'I am attaching form for you to review. By accepting it you will be confirming your cargo.'
    obj.cargocomment_set.create(user=request.user, content=msg, comment_type=1)
    response = '/my/trips/'
    messages.success(request, "You have successfully posted a cargo form to the requesting user")
    return HttpResponse(json.dumps(response), mimetype="application/json")

@login_required
def confirm_cargo_form(request, cargo_id):
    # JSON Response
    cargo = get_object_or_404(Cargo, id=cargo_id)
    html = render_to_string('modals/confirm_cargo_modal_content.html', {'cargo_id': cargo.id})
    response = {'html': html}
    return HttpResponse(json.dumps(response), mimetype="application/json")

