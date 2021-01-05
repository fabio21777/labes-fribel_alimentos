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
import cx_Oracle
from .teste_selenium import *
# Importar a classe que contém as funções e aplicar um alias


def acomp(request, usuario):
    print(usuario)
    acomp = 'acomp'
    search = request.GET.get('search')
    usuario = User.objects.get(username=usuario)
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


def addCarga(request):
    return render(request, 'core/adicionar_carga.html')


def set_carga(request):
    industria = request.POST.get('industria')
    numero_nf = request.POST.get('NF')
    dia_descarga = datetime.fromisoformat(request.POST.get('previsao'))
    # É so pra não da erro
    user = User.objects.get(pk=1)
    tipo_entrada = request.POST.get('tipo_entrada')
    Produto = request.POST.get('Produto')
    QTD = request.POST.get('QTD')
    UN = request.POST.get('un')
    movimentacao = request.POST.get('movimentacao')
    frete = request.POST.get('frete')
    observacao = request.POST.get('observacao')
    carga = Carga.objects.create(numero_nf=numero_nf, industria=industria,
                                 dia_descarga=dia_descarga, user=user,
                                 status='aguardando',
                                 tipo_entrada=tipo_entrada,
                                 Produto=Produto, QTD=QTD, UN=UN,
                                 movimentacao=movimentacao,
                                 frete=frete, observacao=observacao)
    # Temporario
    return redirect('/acompanhamento/admin-fribel')


def liberarCarga(request, id):
    carga = Carga.objects.get(pk=id)
    carga.status = 'liberado'
    carga.save()
    # Tenporario
    return redirect('/acompanhamento/admin-fribel')


def liberar_carga(request):
    cargas_liberadas = Carga.objects.filter(status='liberado', box='')
    box = BoxForm
    return render(request, 'core/liberar_carga.html',
                  {'boxs': box, 'cargas': cargas_liberadas})


def liberar(request, id):
    carga = Carga.objects.get(id=id)
    if request.method == 'POST':
        box_escolhido = BoxForm(request.POST)
        if box_escolhido.is_valid():
            box_escolhido = box_escolhido.cleaned_data['box']
            box = Box.objects.get(id=box_escolhido)
            carga.box = box.name
            carga.save()
    return redirect('liberar-carga')


def login_pag(request):
    login = 'login'
    validação = selenium_Campo_Indústria()
    for i in validação:
        print(i)
    # Consulta_bd_cargas_em_aberto()
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


def conexao_bd():
    connection = cx_Oracle.connect("FRIBEL", "123456789",
                                   "(DESCRIPTION =(ADDRESS_LIST =(ADDRESS = \
                                    (PROTOCOL = TCP)(HOST = 192.168.0.150) \
                                    (PORT = 1521))) \
                                    (CONNECT_DATA =(SID = WINT)))")
    return(connection)


def consulta_bd_cargas_em_aberto():
    cursor=conexao_bd().cursor()
    cursor.execute("""SELECT PCNFENTPREENT.CODFILIAL                                                        
      , PCFILIAL.RAZAOSOCIAL                                                           
      , PCNFENTPREENT.NUMNOTA                                                          
      , PCNFENTPREENT.SIMPLESNACIONAL                                                  
      , PCNFENTPREENT.SERIE                                                            
      , PCNFENTPREENT.DTEMISSAO                                                        
      , PCNFENTPREENT.NUMTRANSENT                                                      
      , PCNFENTPREENT.TIPOFRETE                                                        
      , PCNFENTPREENT.CODTRANSP                                                        
      , PCNFENTPREENT.CODFORNEC                                                        
      , PCFORNEC.FORNECEDOR                                                            
      , NVL(PCFORNEC.CODFORNECPRINC, PCFORNEC.CODFORNEC ) CODFORNECPRINC               
      , PCFORNEC.CODCOMPRADOR                                                          
      , PCNFENTPREENT.CODFUNCLANC                                                      
      , PCNFENTPREENT.DTENT                                                            
      , PCNFENTPREENT.TIPODESCARGA                                                     
      , PCNFENTPREENT.NUMPEDPREENT                                                     
      , PCNFENTPREENT.HORALANC                                                         
      , PCNFENTPREENT.MINUTOLANC                                                       
      , PCNFENTPREENT.FUNCLANC                                                         
      , NVL(PCNFENTPREENT.VLTOTALITENS, 0) VLTOTALITENS                                
      , NVL(PCNFENTPREENT.VLFRETE,      0) VLFRETE                                     
      , CASE WHEN (NVL(PCNFENTPREENT.VLTOTAL, 0) >= NVL(PCNFENTPREENT.VLTOTALNOTA, 0)) 
             THEN  NVL(PCNFENTPREENT.VLTOTAL, 0)                                       
             ELSE  NVL(PCNFENTPREENT.VLTOTALNOTA, 0)                                   
        END VLTOTAL                                                                    
      , NVL(PCNFENTPREENT.STATUS, 'E0') STATUS                                       
      , PCFORNEC.FORNECEDOR                                                            
      , PCENTVEICULO.PLACA                                                             
      , PCENTVEICULO.DATA DTACHEGADA                                                   
      , NVL((SELECT COUNT(CODPROD)                                                     
               FROM PCMOVPREENT                                                        
              WHERE PCMOVPREENT.CODFILIAL   = PCNFENTPREENT.CODFILIAL                  
                AND PCMOVPREENT.NUMTRANSENT = PCNFENTPREENT.NUMTRANSENT), 0) QTITENS   
      , (SELECT COUNT(PCLANCPREENT.DTVENC)                                             
           FROM PCLANCPREENT                                                           
          WHERE PCLANCPREENT.NUMTRANSENT = PCNFENTPREENT.NUMTRANSENT                   
            AND PCLANCPREENT.DTVENC <= TRUNC(SYSDATE)) TITULOVENCIDO                   
      , CASE WHEN NVL((SELECT SUM((NVL(PCITEM.QTPEDIDA,0) - NVL(PCITEM.QTENTREGUE,0)) -
 DECODE(NVL(PCMOVPREENT.TIPOEMBALAGEMPEDIDO, PCNFENTPREENT.TIPOEMBALAGEMPEDIDO), 'M', (NVL(PCMOVPREENT.QT,0) * NVL(PCPRODUT.QTUNITCX,1)), NVL(PCMOVPREENT.QT,0)))                                 
                     FROM PCMOVPREENT                                                  
                        , PCITEM                                                       
                        , PCPRODUT                                                     
                    WHERE PCMOVPREENT.NUMTRANSENT = PCNFENTPREENT.NUMTRANSENT          
                      AND PCMOVPREENT.CODFILIAL   = PCNFENTPREENT.CODFILIAL            
                      AND PCMOVPREENT.NUMSEQPED   = PCITEM.NUMSEQ                      
                      AND PCMOVPREENT.CODPROD     = PCITEM.CODPROD                     
                      AND PCMOVPREENT.NUMPED      = PCITEM.NUMPED                      
                      AND PCPRODUT.CODPROD        = PCITEM.CODPROD                     
                    GROUP                                                              
                       BY PCMOVPREENT.NUMTRANSENT),0) >= -0.01                         
             THEN 'S'                                                                
             ELSE 'N'                                                                
        END TEMSALDO                                                                   
      , PCEMPR.NOME COMPRADOR                                                          
      , TRUNC(SYSDATE) DTAPRIMEIROVENCTO                                               
      , NVL(PCNFENTPREENT.DEDFRETECIFCREDPRESICMS, 'N') DEDFRETECIFCREDPRESICMS      
      , NVL(PCNFENTPREENT.TIPOPREENT, 'N') TIPOPREENT                                
      , NVL(PCNFENTPREENT.IMPORTADOXML, 'N') IMPORTADOXML                            
      , PCNFENTPREENT.OBS                                                              
      , PCNFENTPREENT.NUMTRANSVENDAORIG                                                
      , NVL(PARAMFILIAL.OBTERCOMOBOOLEAN('USAPISCOFINSPEDIDOXML', PCNFENTPREENT.CODFILIAL), 'E') USAPISCOFINSPEDIDOXML 
      , NVL(PARAMFILIAL.OBTERCOMOBOOLEAN('USAICMSPEDIDOXML', PCNFENTPREENT.CODFILIAL), 'E') USAICMSPEDIDOXML           
      , NVL(PARAMFILIAL.OBTERCOMOBOOLEAN('CARREGARSTGUIADOPEDIDOCOMPRA', PCNFENTPREENT.CODFILIAL), 'E') CARREGARSTGUIADOPEDIDOCOMPRA 
      , NVL(PCNFENTPREENT.TIPOMOVGARANTIA,0) TIPOMOVGARANTIA                           
      , PCNFENTPREENT.RESULTADOLAUDO                                                   
      , PCNFENTPREENT.NUMBONUS                                                         
      , PCNFENTPREENT.DTDESCARGA                                                       
   FROM PCNFENTPREENT                                                                  
      , PCFORNEC                                                                       
      , PCENTVEICULO                                                                   
      , PCFILIAL                                                                       
      , PCEMPR                                                                         
  WHERE PCNFENTPREENT.CODFORNEC     = PCFORNEC.CODFORNEC         (+)                   
    AND NVL(PCNFENTPREENT.STATUS, 'L') NOT IN ('E','E7')                         
    AND PCNFENTPREENT.CODENTVEICULO = PCENTVEICULO.CODENTVEICULO (+)                   
    AND PCFORNEC.CODCOMPRADOR       = PCEMPR.MATRICULA           (+)                   
    AND PCNFENTPREENT.CODFILIAL     = PCFILIAL.CODIGO            (+)                   
    AND PCNFENTPREENT.DTEMISSAO BETWEEN         TO_DATE('01122020', 'DD-MM-YYYY') AND         TO_DATE('31122020', 'DD-MM-YYYY') 
  AND PCNFENTPREENT.CODFILIAL     IN ( '1', '2' )               
   AND NVL(REGEXP_REPLACE(PCNFENTPREENT.ROTINALANC, '[^0-9]'), '1308') IN ('1301','1321')
 """)
    for i in cursor:
        print(i)
    cursor.close

#saida do select
"""('1', 'FRIBEL COMERCIO DE ALIMENTOS LTDA', 77326, 'N', '1', datetime.datetime(2020, 12, 31, 0, 0), 243521, 'C', 0, 2795, 'I C MELO & CIA LTDA ', 21, 133, 19, datetime.datetime(2020, 12, 31, 0, 0), '1', 0, '9', '10', 'ANTONIA', 120821.5, 0, 120821.5, 'L', 'I C MELO & CIA LTDA ', None, datetime.datetime(2020, 12, 31, 8, 58, 38), 54, 0, 'S', 'TIAGO SILVA DE SA', datetime.datetime(2020, 12, 31, 0, 0), 'N', 'X', 'S', None, 0, 'S', 'S', 'E', 0, None, None, None)

('1', 'FRIBEL COMERCIO DE ALIMENTOS LTDA', 56789, 'N', '2', datetime.datetime(2020, 12, 30, 0, 0), 243507, 'F', 0, 2730, 'ALIMENTOS ESTRELA LTDA', 2730, 133, 19, datetime.datetime(2020, 12, 30, 0, 0), '1', 0, '16', '50', 'ANTONIA', 355200, 0, 355200, 'L', 'ALIMENTOS ESTRELA LTDA', None, datetime.datetime(2020, 12, 30, 16, 39, 30), 1, 1, 'S', 'TIAGO SILVA DE SA', datetime.datetime(2020, 12, 31, 0, 0), 'N', 'X', 'S', 'Carga:    70 /   1. ALIQUOTA DE IPI REDUZIDA A ZERO CONF  CODIGO DE CLASSIFICACAO FISCAL NR  1601 00 00  . N A O  
 A C E I T A R E M O S   R E C L A M A C O E S   P O S T E R I O R E S. LACRE: 0000891Placa do Veiculo: IWL-2031 - Reboque: ITS-3822', 0, 'S', 'S', 'E', 0, None, None, None)     

('1', 'FRIBEL COMERCIO DE ALIMENTOS LTDA', 2688, 'N', '1', datetime.datetime(2020, 12, 28, 0, 0), 243440, 'C', 0, 193, 'LATICINIO SANTA CLARA', 193, 133, 19, datetime.datetime(2020, 12, 29, 0, 0), '5', 0, '9', '40', 'ANTONIA', 150, 0, 155.1, 'L', 'LATICINIO SANTA CLARA', None, datetime.datetime(2020, 12, 29, 9, 29, 34), 1, 0, 'S', 'TIAGO SILVA DE SA', datetime.datetime(2020, 12, 31, 0, 0), 'N', 'X', 'S', 'N Brinde: 74 EMPRESA OPTANTE PELO BENEFICIO FISCAL RICMS DECRETO 4676/01 ART 145 REFERENTE A NOTA FISCAL DE DEVOLUCAO N 3154124 EMITIDA DIA 19/12/2020 Impresso por: VANIA Transportador: LATICINIOS SANTA CLARA Frete por Conta: 0 - Contratacao do Frete por', 0, 'S', 'S', 'E', 0, None, None, None)        

('1', 'FRIBEL COMERCIO DE ALIMENTOS LTDA', 686615, 'N', '1', datetime.datetime(2020, 12, 29, 0, 0), 243520, 'C', 0, 541, 'GOIASMINAS INDUSTRIA DE LATICINIOS LTDA', 541, 133, 19, 
datetime.datetime(2020, 12, 31, 0, 0), '1', 0, '8', '48', 'ANTONIA', 72444, 0, 72444, 'L', 'GOIASMINAS INDUSTRIA DE LATICINIOS LTDA', None, datetime.datetime(2020, 12, 31, 8, 36, 55), 4, 0, 'S', 'TIAGO SILVA DE SA', datetime.datetime(2020, 12, 31, 0, 0), 'N', 'X', 'S', 'Em caso de nao recebimento ou extravio do boleto bancario, devera ser solicito 2 via 
do mesmo ao Depto. Financeiro desta empresa, atraves do telefone (11) 2889-5959 e via e-mail para cobranca@italac.com.br.;A solicitacao devera ocorrer com antecedencia mi', 0, 'S', 'S', 'E', 0, None, None, None)

('1', 'FRIBEL COMERCIO DE ALIMENTOS LTDA', 686613, 'N', '1', datetime.datetime(2020, 12, 29, 0, 0), 243519, 'C', 0, 541, 'GOIASMINAS INDUSTRIA DE LATICINIOS LTDA', 541, 133, 19, 
datetime.datetime(2020, 12, 31, 0, 0), '1', 0, '8', '47', 'ANTONIA', 87091.2, 0, 87091.2, 'L', 'GOIASMINAS INDUSTRIA DE LATICINIOS LTDA', None, datetime.datetime(2020, 12, 31, 8, 36, 26), 1, 0, 'S', 'TIAGO SILVA DE SA', datetime.datetime(2020, 12, 31, 0, 0), 'N', 'X', 'S', 'Em caso de nao recebimento ou extravio do boleto bancario, devera ser solicito 2 
via do mesmo ao Depto. Financeiro desta empresa, atraves do telefone (11) 2889-5959 e via e-mail para cobranca@italac.com.br.;A solicitacao devera ocorrer com antecedencia mi', 0, 'S', 'S', 'E', 0, None, None, None)"""