from django.forms import ModelForm
from pirateWarApp.models import Ship


class ShipUpdateForm(ModelForm):
    class Meta:
        model = Ship
        fields = ['name', 'crew', 'cannon', 'life']
