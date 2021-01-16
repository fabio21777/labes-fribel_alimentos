from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from .models import Carga,Box
from .models import Tipo_user
from django.contrib.auth.models import User
from datetime import datetime,date
from .forms import BoxForm
from django import forms
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from .teste_selenium import *
from .conection_bd import consulta_bd_cargas_em_aberto
from .conection_bd import conexao_bd
import cx_Oracle
from datetime import datetime, timedelta
# Importar a classe que contém as funções e aplicar um alias

def return_usuario(request):
    if request.user.is_authenticated:
        id_user = request.user.id
    usuario = User.objects.get(pk=id_user)
    return(usuario)


def cargas_erp(usuario):
    try:
        cargas = consulta_bd_cargas_em_aberto()
        for carga in cargas:
            industria = carga['FORNECEDOR']
            numero_nf = carga['NUMNOTA']
            valor_carga = carga['VLTOTAL']
            dia_descarga = carga['DTACHEGADA']
            user = usuario
            user_ERP = carga['FUNCLANC']
            if  carga['STATUS'] == 'L':
                status='liberado'
            else:
                status='aguardando'
            if carga['TIPODESCARGA']== '1':
                tipo_entrada='Entrada Normal'
            else:
                tipo_entrada='Entrada Bonificada'
            Produto = ' '
            QTD = carga['QTITENS']
            movimentacao = '    '
            if carga['TIPOFRETE'] == 'C': 
                frete = 'CIF'
            else:
                frete ='FOB' 
            observacao = str(carga['OBS'])
            if len(Carga.objects.filter(numero_nf=numero_nf)) == 0:
                Carga.objects.create(numero_nf=numero_nf,
                                 industria=industria,
                                 valor_carga=valor_carga,
                                 dia_descarga=dia_descarga,
                                 user=user,
                                 user_ERP=user_ERP,
                                 status=status,
                                 tipo_entrada=tipo_entrada,
                                 Produto=Produto, QTD=QTD, 
                                 UN=' ',
                                 movimentacao=movimentacao,
                                 frete=frete, 
                                 observacao=observacao)
                            
    except:
      print(" ERRO FATAL,-------------->não foi carregada nenhuma carga do ERP é por conta da conexão do banco so é possivel acessa na intranet")


@login_required(login_url='/')
def acompanhamento_carga(request, usuario):
    print(usuario)
    usuario = User.objects.get(username=usuario)
    cargas_erp(usuario)
    acomp = 'acomp'
    search = request.GET.get('search')
    tipo_user = Tipo_user.objects.get(user_tipo=int(usuario.id))
    filter = request.GET.get('filter')
    ordenador = request.GET.get('ordenador')
    if filter:
        cargas = Carga.objects.filter(status=filter)
    elif ordenador:
        cargas = Carga.objects.all().order_by(ordenador)
    elif search:
        cargas = Carga.objects.filter(industria__icontains=search)
    else:
        cargas = Carga.objects.all().order_by('-created_at')

    return render(request, 'core/acomp.html', {'usuario': usuario,
                                               'acomp': acomp,
                                               'cargas': cargas,
                                               'tamanho': len(cargas),
                                               'tipo_user': tipo_user})

@login_required(login_url='/')
def add_Carga(request):
    user = return_usuario(request)
    return render(request, 'core/adicionar_carga.html',{"user":user})




def informacoes_cargas(request,id):
    carga=Carga.objects.get(pk=id)
    user = return_usuario(request)
    return render(request, 'core/informacoes_cargas.html',{'carga':carga,'user':user})

def set_carga(request):
    industria = request.POST.get('industria')
    numero_nf = request.POST.get('NF')
    valor_carga = request.POST.get('valor')
    dia_descarga = datetime.fromisoformat(request.POST.get('previsao'))
    user = return_usuario(request)
    tipo_entrada = request.POST.get('tipo_entrada')
    Produto = request.POST.get('Produto')
    QTD = request.POST.get('QTD')
    UN = request.POST.get('un')
    movimentacao = request.POST.get('movimentacao')
    frete = request.POST.get('frete')
    observacao = request.POST.get('observacao')
    carga = Carga.objects.create(numero_nf=numero_nf,
                                 industria=industria,
                                 valor_carga=valor_carga,
                                 dia_descarga=dia_descarga,
                                 user=user,
                                 status='aguardando',
                                 tipo_entrada=tipo_entrada,
                                 Produto=Produto, QTD=QTD, UN=UN,
                                 movimentacao=movimentacao,
                                 frete=frete, observacao=observacao)
    return redirect('/acompanhamento/'+user.username)




@login_required(login_url='/')
def liberarCarga(request, id):
    carga = Carga.objects.get(pk=id)
    carga.status = 'liberado'
    carga.save()
    user = return_usuario(request)
    return redirect('/acompanhamento/'+user.username)



@login_required(login_url='/')
def liberar_carga_box(request):
    cargas_liberadas = Carga.objects.filter(status='liberado', box='')
    box = BoxForm
    user = return_usuario(request)
    return render(request, 'core/liberar_carga_box.html',
                  {'boxs': box, 'cargas': cargas_liberadas,'user':user})


def reservar_box(request, id):
    carga = Carga.objects.get(id=id)
    if request.method == 'POST':
        box_escolhido = BoxForm(request.POST)
        if box_escolhido.is_valid():
            box_escolhido = box_escolhido.cleaned_data['box']
            box = Box.objects.get(id=box_escolhido)
            carga.box = box.name
            carga.save()
    return redirect('liberar-carga-box')



@login_required(login_url='/')
def historico_cargas_liberadas(request):
    cargas = Carga.objects.filter(status='liberado')
    user = return_usuario(request)
    return render(request, 'core/historico.html', {'cargas': cargas,'user':user})


def login_pag(request):
    login = 'login'
    #  all_teste()
    return render(request, 'core/login.html', {login: 'login'})
    

@csrf_protect
def login_autentificacao(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            url = '/acompanhamento/' + username
            return redirect(url)
        else:
            messages.error(request, 'Usuário/Senha inválidos.Por Favor Tente \
                                     novamente ou entre em contato com o \
                                     suporte')
    return redirect('/')


@login_required(login_url='/')
def logout_user(request):
    logout(request)
    return redirect('/')
