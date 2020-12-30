from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from .models import Carga,Box
from .models import Tipo_user
from django.contrib.auth.models import User
from datetime import datetime
from .forms import BoxForm
from django import forms
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
def teste_selenium():
    try:
        browser = webdriver.Chrome()
        browser.get('http://127.0.0.1:8000/acompanhamento/adicionarCarga/')
        inputElement = browser.find_element_by_id("industria")
        inputElement.send_keys('teste')
        driver.quit()
    except:
        print("erro")
def acomp(request, usuario):
    print(usuario)
    acomp='acomp'
    search = request.GET.get('search')
    usuario = User.objects.get(username = usuario)
    tipo_user = Tipo_user.objects.get(user_tipo = int(usuario.id))
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

    return render(request,'core/acomp.html', {'usuario': usuario,'acomp':acomp, 'cargas': cargas, 'tamanho': len(cargas), 'tipo_user':tipo_user})

def addCarga(request):
    return render(request,'core/adicionar_carga.html')
def set_carga(request):
    industria=request.POST.get('industria')
    numero_nf=request.POST.get('NF')
    dia_descarga=datetime.fromisoformat(request.POST.get('previsao'))
    user=Chamado=User.objects.get(pk=1)#é so pra não da erro
    tipo_entrada=request.POST.get('tipo_entrada')
    Produto=request.POST.get('Produto')
    QTD=request.POST.get('QTD')
    UN=request.POST.get('un')
    movimentacao=request.POST.get('movimentacao')
    frete=request.POST.get('frete')
    observacao=request.POST.get('observacao')
    carga=Carga.objects.create(numero_nf= numero_nf,industria=industria,dia_descarga=dia_descarga,user=user,status='aguardando',tipo_entrada=tipo_entrada,Produto=Produto,QTD=QTD,UN=UN,movimentacao=movimentacao,frete=frete,observacao=observacao)
    return redirect('/acompanhamento/admin-fribel')#temporario

def liberarCarga(request,id):
    carga = Carga.objects.get(pk = id)
    carga.status = 'liberado'
    carga.save()

    return redirect('/acompanhamento/admin-fribel')#tenporario

def liberar_carga(request):
    cargas_liberadas = Carga.objects.filter(status='liberado',box='')
    box = BoxForm
    print('teste',cargas_liberadas)
    return render(request, 'core/liberar_carga.html', {'boxs': box,'cargas': cargas_liberadas})

def liberar(request,id):
    teste= 'teste'
    carga = Carga.objects.get(id=id)
    if request.method == 'POST':
        box_escolhido = BoxForm(request.POST)
        if box_escolhido.is_valid():
            box_escolhido = box_escolhido.cleaned_data['box']
            box = Box.objects.get(id=box_escolhido)
            carga.box = box.name
            carga.save()
            teste= carga.box
    return redirect ('liberar-carga')


def login_pag(request):
    login='login'
    teste_selenium()
    return render(request,'core/login.html',{login:'login'})
@csrf_protect
def login_autentificacao(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            url='/acompanhamento/'+username
            return redirect(url)
        else:
            messages.error(request, 'Usuário/Senha inválidos. Por Favor Tente novamente ou entre em contato com o suporte')
    return redirect('/')
@login_required(login_url='/')
def logout_user(request):
    logout(request)
    return redirect('/')