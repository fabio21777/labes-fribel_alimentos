from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Carga, Carga_Liberada, Box, Tipo_user,Itens_carga
from django.contrib.auth.models import User
from datetime import datetime,date
from .forms import libera_box_Form
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
from .conection_bd import inf_carga_erp
from .whatsapp import newbot
import cx_Oracle
from datetime import datetime, timedelta
import re
# Importar a classe que contém as funções e aplicar um alias

def return_usuario(request):
    if request.user.is_authenticated:
        id_user = request.user.id
    usuario = User.objects.get(pk=id_user)
    return(usuario)

def get_inf_carga_erp(request,carga):
    ids=[]
    if carga.is_ERP == True and len(Itens_carga.objects.filter(carga__numero_transacao=carga.numero_transacao))==0 :
        inf_cargas = inf_carga_erp(carga.numero_nf)
        for inf_carga in inf_cargas:
            numero_pedido = inf_carga['NUMPED']
            cod_prod = inf_carga['CODPROD']
            descricao = inf_carga['DESCRICAO']
            tipo_embalagem = inf_carga['TIPOEMBALAGEMPEDIDO']
            embalagem = inf_carga['EMBALAGEM']
            unidade = inf_carga['UNIDADE']
            departamento = inf_carga['DEPARTAMENTO']
            QTD_unitaria =  inf_carga['QTUNIT']
            QTD_caixa = inf_carga['QTUNITCX']
            QTD_pedida = inf_carga['QTPEDIDA']
            QTD_reservada = inf_carga['QTRESERV']
            QTD_ult_entrada = inf_carga['QTULTENT']
            data_ultima_entrada = inf_carga['DTULTENT']
            carga = carga
            item_carga = Itens_carga.objects.create(numero_pedido=numero_pedido,
                                    cod_prod=cod_prod,
                                    descricao=descricao,
                                    tipo_embalagem=tipo_embalagem,
                                    embalagem=embalagem,
                                    unidade=unidade,
                                    departamento=departamento,
                                    QTD_unitaria=QTD_unitaria,
                                    QTD_caixa=QTD_caixa,
                                    QTD_pedida=QTD_pedida,
                                    QTD_reservada=QTD_reservada,
                                    QTD_ult_entrada=QTD_ult_entrada,
                                    data_ultima_entrada=data_ultima_entrada,
                                    carga=carga )
        itens_carga=Itens_carga.objects.filter(carga__numero_transacao=carga.numero_transacao)
        for item in itens_carga:
            print('teste')
            ids.append(int(re.sub('[^0-9]','',str(item))))
            print('------------->',int(re.sub('[^0-9]','',str(item))))
        return(ids)
    else:
        itens_carga=Itens_carga.objects.filter(carga__numero_transacao=carga.numero_transacao)
        for item in itens_carga:
            ids.append(int(re.sub('[^0-9]','',str(item))))
            print('------------->',int(re.sub('[^0-9]','',str(item))))
        return(ids)

 
def criar_carga_bd(numero_nf, industria, numero_transacao, valor_carga, dia_chegada, user, user_erp, status, tipo_entrada, produto, 
    QTD, UN, movimentacao, frete, observacao):
    if len(Carga.objects.filter(numero_nf = numero_nf)) == 0:
        Carga.objects.create(numero_nf = numero_nf,
                             industria = industria,
                             numero_transacao = numero_transacao,
                             valor_carga = valor_carga,
                             dia_chegada = dia_chegada,
                             dia_descarga = dia_chegada,
                             user = user,
                             user_ERP = user_erp,
                             status = status,
                             tipo_entrada = tipo_entrada,
                             Produto = produto, QTD = QTD, 
                             UN = UN,
                             is_ERP = True,
                             movimentacao = movimentacao,
                             frete = frete, 
                             observacao = observacao)

def definir_valores_variaveis_erp(carga, variavel):
    if  variavel == 'status':
        if  carga['STATUS'] == 'L':
            return 'liberado'
        else:
            return 'aguardando'
    elif variavel == 'tipo_entrada':
        if carga['TIPODESCARGA']== '1':
            return 'Entrada Normal'
        else:
            return 'Entrada Bonificada'
    else: 
        if carga['TIPOFRETE'] == 'C': 
            return 'CIF'
        else:
            return 'FOB'

def cargas_erp(usuario):
    try:
        cargas = consulta_bd_cargas_em_aberto()
        for carga in cargas:
            numero_transacao = carga['NUMTRANSENT']
            industria = carga['FORNECEDOR']
            numero_nf = str(carga['NUMNOTA'])
            valor_carga = carga['VLTOTAL']
            dia_chegada = carga['DTACHEGADA']
            user = usuario
            user_erp = carga['FUNCLANC']
            status = definir_valores_variaveis_erp(carga, 'status')
            tipo_entrada = definir_valores_variaveis_erp(carga, 'tipo_entrada')
            produto = ''
            QTD = carga['QTITENS']
            movimentacao = '' 
            frete = definir_valores_variaveis_erp(carga, 'frete') 
            observacao = str(carga['OBS'])
            UN = ''
            print('Nota Fiscal >>>>>>> ', numero_nf)

            criar_carga_bd(numero_nf, industria, numero_transacao, valor_carga, dia_chegada, user, user_erp, status, tipo_entrada, produto, QTD, UN, movimentacao, frete, observacao)   
    except:
      print(" ERRO FATAL! Não foi carregada nenhuma carga do ERP por conta da conexão do banco só ser possivel acessar na intranet.")


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
        cargas = Carga.objects.filter(industria__icontains=search.strip())
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
    itens_carga=[]
    carga=Carga.objects.get(pk=id)
    ids=get_inf_carga_erp(request,carga)
    print('------>id',ids)
    for i in ids:
        itens_carga.append(Itens_carga.objects.get(id=i))
    user = return_usuario(request)
    return render(request, 'core/informacoes_cargas.html',{'carga':carga,'user':user,'itens_carga':itens_carga})

def set_carga(request):
    industria = request.POST.get('industria')
    numero_nf = request.POST.get('NF')
    valor_carga = request.POST.get('valor')
    dia_descarga = datetime.fromisoformat(request.POST.get('previsao'))
    dia_chegada = datetime.fromisoformat(request.POST.get('previsao'))
    user = return_usuario(request)
    tipo_entrada = request.POST.get('tipo_entrada')
    Produto = request.POST.get('Produto')
    QTD = request.POST.get('QTD')
    UN = request.POST.get('un')
    movimentacao = request.POST.get('movimentacao')
    frete = request.POST.get('frete')
    observacao = request.POST.get('observacao')
    cont=request.POST.get('cont')
    print('----------->>',cont)
    carga = Carga.objects.update_or_create(numero_nf=numero_nf.strip(),
                                 industria=industria.strip(),
                                 valor_carga=valor_carga.strip(),
                                 dia_descarga=dia_descarga,
                                 dia_chegada=dia_chegada,
                                 user=user,
                                 status='aguardando',
                                 tipo_entrada=tipo_entrada,
                                 Produto=Produto.strip(), QTD=QTD.strip(), UN=UN,
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
def liberar_para_box(request):
    box = Box.objects.all()
    cargas_liberadas = libera_box_Form
    user = return_usuario(request)
    return render(request, 'core/liberar_carga_box.html',
                  {'boxs': box, 'cargas': cargas_liberadas, 'user': user})


def reservar_box(request, id):
    box = Box.objects.get(id=id)
    if request.method == 'POST':
        carga_escolhida = request.POST.get('carga')
        carga = Carga.objects.get(id=carga_escolhida)
        box.is_free = False
        carga.box = box.name
        carga.save()
        box.save()
        bott = newbot()
        bott.EnviarMensagens_grupo('Teste',str(carga.industria)+'Liberada')
    return redirect('liberar-para-box')


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

#HISTÓRICO DE CARGAS LIBERADAS
@login_required(login_url='/')
def historico_cargas_liberadas(request):
    #usuario = User.objects.get(username=usuario)
    #cargas_erp(usuario)
    #acomp = 'acomp'
    #tipo_user = Tipo_user.objects.get(user_tipo=int(usuario.id))
    search = request.GET.get('search')
    ordenador = request.GET.get('ordenador')
    lista_cargas = Carga.objects.all()

    for carga_liberada in lista_cargas:
        if carga_liberada.status == 'liberado':
            try:
                Carga_Liberada.objects.create(numero_nf=carga_liberada.numero_nf,
                                    industria=carga_liberada.industria,
                                    valor_carga=carga_liberada.valor_carga,
                                    dia_descarga=date.today(),
                                    user=carga_liberada.user,
                                    status='liberado',
                                    tipo_entrada=carga_liberada.tipo_entrada,
                                    Produto=carga_liberada.Produto, 
                                    QTD=carga_liberada.QTD, UN=carga_liberada.UN,
                                    movimentacao=carga_liberada.movimentacao,
                                    frete=carga_liberada.frete, 
                                    observacao=carga_liberada.observacao,
                                    id = carga_liberada.pk)
            except:
                print('Carga liberada já adicionada!')
    
    if ordenador:
        cargas = Carga_Liberada.objects.all().order_by(ordenador)
    elif search:
        cargas = Carga_Liberada.objects.filter(industria__icontains=search.strip())
    else:
        cargas = Carga_Liberada.objects.all().order_by('-created_at')

    user = return_usuario(request)
    return render(request, 'core/historico.html', {'cargas': cargas,'user':user})

#ADIÇÃO, EXCLUSÃO E EDIÇÃO DE CARGAS
@login_required(login_url='/')
def excluir_carga(request, id):
    user = return_usuario(request)
    carga = get_object_or_404(Carga, pk = id)

    if request.method == 'POST':
        try:
            carga.delete()
        except:
            print('Erro ao excluir carga!')

        return redirect('/acompanhamento/'+user.username)
    
    return render(request, 'core/confirmar_exclusao.html', {'carga': carga})

@login_required(login_url='/')
def excluir_carga_historico(request, id):
    user = return_usuario(request)
    carga = get_object_or_404(Carga_Liberada, pk = id)
        
    if request.method == 'POST':
        try:
            carga.delete()
        except:
            print('Erro ao excluir carga!')

        return redirect('/acompanhamento/historico/')
    
    return render(request, 'core/confirmar_exclusao.html', {'carga': carga})
def zap():
    print(teste)
    
#Editar Cargas
@login_required(login_url='/')
def editar_cargas(request, id, template_name='core\editar-carga.html' ):
    carga = Carga.objects.get(pk=id)

    return render(request,template_name, {'carga':carga})

@login_required(login_url='/')  
def set_edit(request, id):

    if request.method == "POST":
        industria = request.POST('industria')
        numero_nf = request.POST('NF')
        valor_carga = request.POST('valor')
        dia_descarga = datetime.fromisoformat(request.POST('previsao'))
        dia_chegada = datetime.fromisoformat(request.POST('previsao'))
        user = return_usuario(request)
        tipo_entrada = request.POST('tipo_entrada')
        Produto = request.POST('Produto')
        QTD = request.POST('QTD')
        UN = request.POST('un')
        movimentacao = request.POST('movimentacao')
        frete = request.POST('frete')
        observacao = request.POST('observacao')

        carga1 = Carga.objects.get(pk=id)

        carga1.industria = industria
        carga1.numero_nf = NF
        carga1.valor_carga = valor
        carga1.dia_descarga = dia_descarga
        carga1.dia_chegada = dia_chegada
        carga1.tipo_entrada = tipo_entrada
        carga1.Produto = Produto
        carga1.QTD = QTD
        carga1.UN = un
        carga1.movimentacao = movimentacao
        carga1.frete = frete
        carga1.observacao = observacao
        carga1.status = 'liberado'
        carga1.save()

        return redirect('/acompanhamento/'+user.username)
        
    else:
        try:
            carga = Carga.objects.get(pk=id)

        except crud.DoesNotExist:
            carga = None
        
        return render(request, '/acompanhamento/'+user.username)
