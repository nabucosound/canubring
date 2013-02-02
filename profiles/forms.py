from django import forms
from django.contrib.auth.models import User


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



