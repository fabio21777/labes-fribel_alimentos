from django import forms
from .models import Carga,Box




class BoxForm(forms.Form):
    id_box = []
    nome_box = []
    BOX_DISPONIVEIS=[]
    box_livres = Box.objects.filter(is_free=True)
    for i in box_livres:
        id_box.append(i.id)
        nome_box.append(i.name)
    BOX_DISPONIVEIS = zip(id_box,nome_box)
    box = forms.CharField(
        max_length=3,
        widget=forms.Select(choices=BOX_DISPONIVEIS),
    )
   