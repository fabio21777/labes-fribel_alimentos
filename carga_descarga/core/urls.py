from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('acompanhamento/<str:usuario>', views.acomp, name='acompanhamento'),
    path('adicionarCarga/', views.addCarga, name='adicionar-carga'),
    path('', views.login, name='login'), #Tela home
]