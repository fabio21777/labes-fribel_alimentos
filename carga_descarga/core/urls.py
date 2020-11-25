from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    #Essa url comentada vai ser a futura tela de acompanhamento com indicação de que tipo de usuário está acessando
    #path('acompanhamento/<boolean:tipo-usuario>', views.acomp, name='acompanhamento'),
    path('', views.acomp, name='acompanhamento'), #Tela home temporária
    path('adicionarCarga/', views.addCarga, name='adicionar-carga'),
    path('login/', views.login, name='login'), #Futura tela home,
]