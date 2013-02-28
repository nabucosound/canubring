from django.forms import ModelForm
from cargos.models import Cargo


class CargoForm(ModelForm):
    class Meta:
        model = Cargo
        exclude = ('trip', 'requesting_user', 'traveller_user', 'state',)

