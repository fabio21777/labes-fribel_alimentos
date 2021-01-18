from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('acompanhamento/<str:usuario>', views.acompanhamento_carga,
         name='acompanhamento'),
    path('acompanhamento/adicionarCarga/', views.add_Carga,
         name='adicionar-carga'),
    path('acompanhamento/adicionarCarga/submit', views.set_carga,
         name='set-carga'),
    path('acompanhamento/liberarCarga/<str:id>/', views.liberarCarga),
    path('liberar', views.liberar_carga_box, name='liberar-carga-box'),
    path('liberar/<str:id>/', views.reservar_box, name='reservar-box'),
    path('login/submit', views.login_autentificacao),
    path('', views.login_pag, name='login'), # Tela home
    path('acompanhamento/historico/', views.historico_cargas_liberadas,
         name='historico'),
    path('acompanhamento/informacoes_cargas/<str:id>', views.informacoes_cargas),
    path('logout_user',views.logout_user),
    path('excluirCarga/<str:id>', views.excluir_carga, name="excluir_carga")
]