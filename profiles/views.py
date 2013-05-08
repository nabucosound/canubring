from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy

from profiles.models import ProfileCountry
from profiles.forms import EmailSignupForm, EmailLoginForm, PictureUploadForm, EmailForm, PasswordResetForm
from profiles.utils import create_nb_user


@login_required
def other_profile(request, user_id, template):
    ctxt = dict()
    other_user = get_object_or_404(User, id=user_id)
    ctxt['profile'] = other_user.userprofile
    return render(request, template, ctxt)


@login_required
@require_POST
def update_profile(request):
    user = request.user
    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get('last_name')
    user.save()
    profile = user.userprofile
    country = ProfileCountry.objects.get(code=request.POST.get('country'))
    profile.country = country
    profile.language = request.POST.get('language')
    profile.second_language = request.POST.get('second_language')
    if not profile.completed:
        profile.completed = True
        profile.save()
        request.session['show_signup_sys_msg'] = True
    return HttpResponse(json.dumps('/my/profile/'), mimetype="application/json")

@login_required
@require_POST
def update_social(request):
    profile = request.user.userprofile
    for pos in range(1, 8):
        obj, created = profile.sociallink_set.get_or_create(pos=pos)
        url = request.POST.get('social%s' % pos, '')
        obj.url = url
        obj.save()
    return redirect('profile')

def verify_email(request, template, token):
    from django.core import signing
    # from django.http import Http404
    ctxt = dict()
    token_expires = 3600 * 48  # Two days
    salt = 'password_recovery'
    try:
        pk = signing.loads(token, max_age=token_expires,
                           salt=salt)
    except signing.BadSignature:
        ctxt['email_verified'] = False
        from django.http import Http404
        raise Http404
    else:
        ctxt['email_verified'] = True
        user = get_object_or_404(User, pk=pk)
        profile = user.userprofile
        profile.email_verified = True
        profile.save()
        request.session['show_email_verified_sys_msg'] = True
        return redirect('profile')

@require_POST
def login_view(request):
    form = EmailLoginForm(request.POST)
    email = form.data.get('email')
    password = form.data.get('password')

    if not form.is_valid():
        error_msg = form.errors['email'][0]
        return HttpResponseBadRequest(json.dumps(error_msg), mimetype="application/json")

    user = User.objects.get(email__iexact=email)
    if getattr(settings, 'BYPASS_AUTHENTICATION', False):
        auth_user = user
        auth_user.backend = 'django.contrib.auth.backends.ModelBackend'
    else:
        auth_user = authenticate(username=user.username, password=password)
        if not auth_user.userprofile.email_verified:
            error_msg = "You must verify your email first"
            return HttpResponseBadRequest(json.dumps(error_msg), mimetype="application/json")
        if auth_user is None or not auth_user.is_active:
            error_msg = "Bad authentication"
            return HttpResponseBadRequest(json.dumps(error_msg), mimetype="application/json")

    login(request, auth_user)
    return HttpResponse(json.dumps('/my/profile/'), mimetype="application/json")

@require_POST
def signup_view(request):
    form = EmailSignupForm(request.POST)
    email = form.data.get('email')
    password = form.data.get('password')

    if form.is_valid():
        # Create User and Profile
        user = create_nb_user(email, password)
        user = authenticate(username=user.username, password=password)
        login(request, user)

        request.session['show_signup_sys_msg'] = True
        return HttpResponse(json.dumps('/my/profile/'), mimetype="application/json")

    error_msg = form.errors['email'][0]
    return HttpResponseBadRequest(json.dumps(error_msg), mimetype="application/json")

@login_required
@require_POST
def upload_profile_picture(request):
    profile = request.user.userprofile
    form = PictureUploadForm(request.POST, request.FILES, instance=profile)
    if not form.is_valid():
        messages.error(request, "Error while uploading new avatar picture")
        return redirect('profile')
    form.save()
    messages.success(request, "You have modified your avatar picture")
    return redirect('profile')


class EmailSettingsView(FormView):
    form_class = EmailForm
    template_name = 'edit_settings/edit_settings.html'
    success_url = reverse_lazy('settings')

    def get_form_kwargs(self):
        kwargs = super(EmailSettingsView, self).get_form_kwargs()
        kwargs.update({'request' : self.request})
        return kwargs

    def form_invalid(self, form):
        for error in form.errors.get('email'):
            messages.error(self.request, error)
        return redirect('settings')
        return super(EmailSettingsView, self).form_invalid(form)

    def form_valid(self, form):
        self.request.user.email = form.cleaned_data.get('email')
        self.request.user.save()
        messages.success(self.request, "You have updated your email")
        return redirect('settings')
        return super(EmailSettingsView, self).form_valid(form)


class PasswordSettingsView(FormView):
    form_class = PasswordResetForm
    template_name = 'edit_settings/edit_settings.html'
    success_url = reverse_lazy('settings')

    def get_form_kwargs(self):
        kwargs = super(PasswordSettingsView, self).get_form_kwargs()
        kwargs.update({'request' : self.request})
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, "Passwords didn't match")
        return super(PasswordSettingsView, self).form_invalid(form)

    def form_valid(self, form):
        self.request.user.set_password(form.cleaned_data['password1'])
        self.request.user.save()
        messages.success(self.request, "You have updated your password")
        return super(PasswordSettingsView, self).form_valid(form)


