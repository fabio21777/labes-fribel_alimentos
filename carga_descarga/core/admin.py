from django.contrib import admin
from .models import Carga,Box,Tipo_user,Itens_carga, Carga_Liberada

admin.site.register(Carga)
admin.site.register(Box)
admin.site.register(Tipo_user)
admin.site.register(Itens_carga)
admin.site.register(Carga_Liberada)
