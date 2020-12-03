from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('acompanhamento/<str:usuario>', views.acomp, name = 'acompanhamento'),
    path('acompanhamento/adicionarCarga/', views.addCarga, name = 'adicionar-carga'),
    path('acompanhamento/adicionarCarga/submit',views.set_carga, name = 'set-carga'),
    path('liberar',views.liberar_carga, name = 'liberar-carga'),
    path('liberar/<str:id>/',views.liberar, name = 'liberar'),
    path('', views.login, name = 'login'), #Tela home
]