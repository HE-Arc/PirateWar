from pirateWarApp.models import Ship

from django.contrib.auth.models import User
from django.forms import ModelForm


class ShipUpdateForm(ModelForm):
    class Meta:
        model = Ship
        fields = ['name', 'crew', 'cannon', 'life']


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
