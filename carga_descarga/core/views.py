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
    return redirect('/acompanhamento/fsm')#temporario

def liberarCarga(request,id):
    carga = Carga.objects.get(pk = id)
    carga.status = 'liberado'
    carga.save()

    return redirect('/acompanhamento/admin-fribel')

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


def login(request):
    return render(request,'core/login.html')
