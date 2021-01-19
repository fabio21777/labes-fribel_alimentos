from django import forms
from .models import Box


class BoxForm(forms.Form):
    box = forms.ModelChoiceField(queryset=Box.objects.filter(is_free=True))
