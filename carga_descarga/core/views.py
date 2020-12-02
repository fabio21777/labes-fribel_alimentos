from django.shortcuts import render
from django.shortcuts import redirect
from .models import Carga
from .models import Tipo_user
from django.contrib.auth.models import User
from datetime import datetime

def acomp(request, usuario):
    print(usuario)
    usuario = User.objects.get(username = usuario)
    tipo_user = Tipo_user.objects.get(user_tipo = int(usuario.id))
    filter = request.GET.get('filter')
    ordenador = request.GET.get('ordenador')

    if filter:
        cargas = Carga.objects.filter(status = filter, user = request.user) 
    elif ordenador:
        cargas = Carga.objects.all().order_by(ordenador).filter(user = request.user)
    else: 
        cargas = Carga.objects.all().order_by('-created_at')

    return render(request,'core/acomp.html', {'usuario': usuario, 'cargas': cargas, 'tamanho': len(cargas), 'tipo_user':tipo_user})

def addCarga(request):
    return render(request,'core/adicionar_carga.html')

def set_carga(request):
    industria = request.POST.get('industria')
    numero_nf = request.POST.get('NF')
    dia_descarga = datetime.fromisoformat(request.POST.get('previsao'))
    user=Chamado = User.objects.get(pk=1)#é so pra não da erro
    tipo_entrada = request.POST.get('tipo_entrada')
    Produto = request.POST.get('Produto')
    QTD = request.POST.get('QTD')
    UN = request.POST.get('un')
    movimentacao = request.POST.get('movimentacao')
    frete = request.POST.get('frete')
    observacao = request.POST.get('observacao')
    carga = Carga.objects.create(numero_nf = numero_nf, industria = industria, dia_descarga = dia_descarga, user = user, status = 'Aguardando', tipo_entrada = tipo_entrada, Produto = Produto, QTD = QTD, UN = UN, movimentacao = movimentacao, frete = frete, observacao = observacao)
 
    return redirect('/acompanhamento/fsm')#temporario

def liberarCarga(request,id):
    carga = Carga.objects.get(pk = id)
    carga.status = 'liberado'
    carga.save()

    return redirect('/acompanhamento/admin-fribel')

def login(request):
    return render(request,'core/login.html')
