from django import forms
from .models import Carga


class BoxForm(forms.Form):
    Carga = forms.ModelChoiceField(queryset=Carga.objects.filter(status='liberado'), to_field_name="box")
