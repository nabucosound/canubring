from django.forms import ModelForm
from cargos.models import Cargo


class CargoForm(ModelForm):
    class Meta:
        model = Cargo
        exclude = ('trip', 'requesting_user', 'traveller_user', 'state',)


class ReviewTravellerForm(ModelForm):
    class Meta:
        model = Cargo
        fields = ('traveller_user_review_stars', 'traveller_user_review_comment',)

