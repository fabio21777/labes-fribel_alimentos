from django import forms
from .models import Carga


class libera_box_Form(forms.Form):
    carga = forms.ModelChoiceField(queryset=Carga.objects.filter(status='liberado',box=''))
