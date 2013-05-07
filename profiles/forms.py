from django import forms
from django.contrib.auth.models import User

from profiles.models import UserProfile

class EmailSignupForm(forms.Form):
    email = forms.EmailField(required=True)

    def clean_email(self):
        cleaned_data = self.cleaned_data
        try:
            User.objects.get(email__iexact=cleaned_data.get('email', None))
            raise forms.ValidationError("Email is already taken")
        except User.DoesNotExist:
            pass
        return cleaned_data['email']


class EmailLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    # password = forms.CharField(widget=forms.PasswordInput, required=False)

    def clean_email(self):
        cleaned_data = self.cleaned_data
        try:
            User.objects.get(email__iexact=cleaned_data.get('email', None))
        except User.DoesNotExist:
            raise forms.ValidationError("Email doesn't exist on our system")
        return cleaned_data['email']

class PictureUploadForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('profile_photo',)


class EmailForm(forms.Form):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        self.user = request.user
        return super(EmailForm, self).__init__(*args, **kwargs)

    def clean_email(self, *args, **kwargs):
        data = self.cleaned_data['email']
        try:
            User.objects.exclude(id=self.user.id).get(email=data)
        except User.DoesNotExist:
            return data
        else:
            raise forms.ValidationError("Email is already been used by another user")

