from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.conf import settings
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _

from website.utils import listing
from cities_light.models import Country


def set_language_from_get_request(request, lang):
    for language in settings.LANGUAGES:
        if language[0] == lang:
            request.session['django_language'] = lang
            translation.activate(lang)
            request.LANGUAGE_CODE = translation.get_language()
    return redirect('home')

def logout(request):
    django_logout(request)
    return redirect('/')

@login_required
def profile(request, template):
    ctxt = dict()
    ctxt['profile'] = request.user.userprofile
    if request.session.pop('show_signup_sys_msg', False):
        ctxt['show_signup_sys_msg'] = True
    if request.session.pop('show_email_verified_sys_msg', False):
        ctxt['show_email_verified_sys_msg'] = True
    ctxt['profile_countries'] = Country.objects.all()
    return render(request, template, ctxt)

@login_required
def trips(request, template, profile_attr='current_trips'):
    ctxt = dict()
    ctxt['trips'] = listing(request, getattr(request.user.userprofile, profile_attr))
    ctxt['past_trips'] = profile_attr == 'past_trips'
    if request.GET.get('m') == '1':
        ctxt['show_new_trip_sys_msg'] = True
    return render(request, template, ctxt)

@login_required
def new_trip(request, template):
    ctxt = dict()
    ctxt['countries'] = Country.objects.order_by('name')
    return render(request, template, ctxt)

@login_required
def cargos(request, template, profile_attr='current_cargos'):
    ctxt = dict()
    ctxt['my_cargos'] = True
    ctxt['cargos'] = listing(request, getattr(request.user.userprofile, profile_attr))
    ctxt['past_cargos'] = profile_attr == 'past_cargos'
    return render(request, template, ctxt)

@login_required
def evaluations(request, template, profile_attr='get_reviews_about_me'):
    ctxt = dict()
    ctxt['reviews'] = listing(request, getattr(request.user.userprofile, profile_attr))
    ctxt['reviews_by_me'] = profile_attr == 'get_all_reviews_by_me'
    return render(request, template, ctxt)

@login_required
def delete_account(request):
    user = request.user
    user.is_active = False
    user.save()
    django_logout(request)
    return redirect('/')

def get_cities(request, country_id):
    from django.shortcuts import get_object_or_404
    from cities_light.models import Country
    country = get_object_or_404(Country, id=country_id)

    # JSON Response
    from django.template.loader import render_to_string
    from django.http import HttpResponse
    from django.utils import simplejson as json
    html = render_to_string('city_select_options.html', {'cities': country.city_set.order_by('name')})
    response = {'html': html}
    return HttpResponse(json.dumps(response), mimetype="application/json")

class TripLegFormView(TemplateView):
    def get_context_data(self, **kwargs):
        ctxt = super(TripLegFormView, self).get_context_data(**kwargs)
        ctxt['countries'] = Country.objects.order_by('name')
        return ctxt

def reference_price(request):
    ctxt = dict()
    template = "reference_prices.html"
    if request.method == 'POST':
        distance = request.POST.get('distance')
        weight = request.POST.get('weight')
        size = request.POST.get('size')
        price = request.POST.get('price')
        from django.contrib import messages
        if not distance or not weight or not size or not price:
            messages.error(request, _("All fields are required"))
            return render(request, template, ctxt)
        from website.utils import reference_price, reference_saving
        ref_price = reference_price(distance, float(weight), float(size), float(price))
        ref_saving = reference_saving(distance, float(weight), float(size), float(price))
        messages.success(request, _("Reference price is: %(price)s $USD") % {'price': int(ref_price)})
        messages.success(request, _("Reference saving is: %(saving)s %%") % {'saving': int(ref_saving)})
    return render(request, template, ctxt)

