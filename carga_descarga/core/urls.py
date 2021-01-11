from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('acompanhamento/<str:usuario>', views.acompanhamento_carga, name = 'acompanhamento'),
    path('acompanhamento/adicionarCarga/', views.add_Carga, name = 'adicionar-carga'),
    path('acompanhamento/adicionarCarga/submit',views.set_carga, name = 'set-carga'),
    path('acompanhamento/liberarCarga/<str:id>/',views.liberarCarga),
    path('liberar',views.liberar_carga, name = 'liberar-carga'),
    path('liberar/<str:id>/',views.liberar, name = 'liberar'),
    path('login/submit',views.login_autentificacao),
    path('', views.login_pag, name = 'login'), #Tela home
    path('acompanhamento/historico/', views.historico_cargas_liberadas, name = 'historico')
]