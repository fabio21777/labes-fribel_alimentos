import cx_Oracle
from datetime import datetime, timedelta

def conexao_bd():
    connection = cx_Oracle.connect("FRIBEL", "FG2hu3DV4T",
                                   "(DESCRIPTION =(ADDRESS_LIST =(ADDRESS = \
                                    (PROTOCOL = TCP)(HOST = 192.168.0.150) \
                                    (PORT = 1521))) \
                                    (CONNECT_DATA =(SID = WINT)))")
    return(connection)


def consulta_bd_cargas_em_aberto():
    data = []
    data_e_hora_atuais = datetime.now()
    date_inicial = data_e_hora_atuais - timedelta(days=30)
    date_final = data_e_hora_atuais.strftime('%d/%m/%Y')
    date_inicial=date_inicial.strftime('%d/%m/%Y')
    cursor = conexao_bd().cursor()
    try:
      cursor.execute(""" SELECT PCNFENTPREENT.NUMNOTA                                                                                                                                                                    
        , PCNFENTPREENT.DTEMISSAO     
        , PCNFENTPREENT.NUMTRANSENT                                                    
        , PCNFENTPREENT.TIPOFRETE                                                                                                                                                                     
        , PCFORNEC.FORNECEDOR                                                            
        , NVL(PCFORNEC.CODFORNECPRINC, PCFORNEC.CODFORNEC ) CODFORNECPRINC                                                                                                                                                                                       
        , PCNFENTPREENT.TIPODESCARGA                                                                                                                                                                
        , PCNFENTPREENT.FUNCLANC                                                         
        , NVL(PCNFENTPREENT.VLTOTALITENS, 0) VLTOTALITENS                                
        , NVL(PCNFENTPREENT.VLFRETE,      0) VLFRETE                                     
        , CASE WHEN (NVL(PCNFENTPREENT.VLTOTAL, 0) >= NVL(PCNFENTPREENT.VLTOTALNOTA, 0)) 
              THEN  NVL(PCNFENTPREENT.VLTOTAL, 0)                                       
              ELSE  NVL(PCNFENTPREENT.VLTOTALNOTA, 0)                                   
          END VLTOTAL                                                                    
        , NVL(PCNFENTPREENT.STATUS, 'E0') STATUS                                                                                                   
        , PCENTVEICULO.DATA DTACHEGADA                                                   
        , NVL((SELECT COUNT(CODPROD)                                                     
               FROM PCMOVPREENT                                                        
              WHERE PCMOVPREENT.CODFILIAL   = PCNFENTPREENT.CODFILIAL                  
                AND PCMOVPREENT.NUMTRANSENT = PCNFENTPREENT.NUMTRANSENT), 0) QTITENS                                                                                                                                                             
        , PCNFENTPREENT.OBS                                                                                                                                                                                         
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
      AND PCNFENTPREENT.DTEMISSAO BETWEEN         TO_DATE('"""+date_inicial+"""',\
                                                        'DD-MM-YYYY') AND\
                                                        TO_DATE('"""+date_final+"""', 'DD-MM-YYYY')
      AND PCNFENTPREENT.CODFILIAL     IN ( '1', '2' )               
      AND NVL
      (REGEXP_REPLACE(PCNFENTPREENT.ROTINALANC, '[^0-9]'), '1308') 
      IN ('1301','1321')
      """)
      columns = [col[0] for col in cursor.description]
      cursor.rowfactory = lambda *args: dict(zip(columns, args))
      cursor.fetchone()
      for i in cursor:
        data.append(i)
        #print(i,'\n\n')
      cursor.close()
      return(data)
    except:
      print("não foi carregada nenhuma carga do ERP")
      cursor.close()
      return(data)


def inf_carga_erp(nf):
  data=[]
  cursor = conexao_bd().cursor()
  cursor.execute("""SELECT PCITEM.NUMPED
     , PCPEDIDO.CODFILIAL
     , PCITEM.NUMSEQ
     , PCPRODUT.CODPROD
     , PCPRODUT.EMBALAGEMMASTER
     , PCPRODUT.EMBALAGEM
     , PCPRODUT.UNIDADE
     , DECODE(PCPRODUT.OBS2, 'FL', 'S', PCPRODFILIAL.FORALINHA) FORALINHA
     , PCPRODUT.NBM
     , PCPRODUT.CODSEC
     , PCPRODUT.DESCRICAO
     , PCPRODUT.CODEPTO
     , PCDEPTO.DESCRICAO DEPARTAMENTO
     , PCPRODUT.CODFORNEC
     , PCFORNEC.FORNECEDOR
     , PCPRODUT.CODPRODPRINC
     , NVL(PCFORNEC.PRAZOENTREGA, 0) PRAZOENTREGA
     , PCEST.DTULTENT
     , NVL(PCPRODUT.QTUNIT, 0) QTUNIT
     , NVL(PCPRODUT.QTUNITCX, 0) QTUNITCX
     , NVL(PCEST.CUSTOREP, 0) CUSTOREP
     , NVL(PCITEM.PCOMPRA, 0) PCOMPRA
     , NVL(PCEST.QTINDENIZ, 0) QTINDENIZ
     , NVL(PCEST.QTBLOQUEADA, 0) QTBLOQUEADA
     , NVL(PCITEM.QTPEDIDA, 0) QTPEDIDA
     , NVL(PCEST.QTRESERV, 0) QTRESERV
     , NVL(PCEST.QTULTENT, 0) QTULTENT
     , NVL(PCMOVPREENT.TIPOEMBALAGEMPEDIDO, NVL(PCITEM.TIPOEMBALAGEMPEDIDO, PCPEDIDO.TIPOEMBALAGEMPEDIDO)) TIPOEMBALAGEMPEDIDO
     , NVL(PCITEM.MULTIMPLOUNIDADEMASTER, PCPEDIDO.MULTIMPLOUNIDADEMASTER) MULTIMPLOUNIDADEMASTER ,
      NVL(PCNFENTPREENT.STATUS, 'E0') STATUS
  FROM PCPEDIDO
     , PCITEM
     , PCFORNEC
     , PCPRODUT
     , PCEST
     , PCPRODFILIAL
     , PCDEPTO
     , PCMOVPREENT,
     PCNFENTPREENT
 WHERE PCPEDIDO.NUMPED    = PCITEM.NUMPED
   AND PCPEDIDO.CODFILIAL = '1'
   AND PCITEM.CODPROD     = PCPRODUT.CODPROD
   AND PCPEDIDO.CODFILIAL = PCEST.CODFILIAL
   AND PCITEM.CODPROD     = PCEST.CODPROD
   AND PCPEDIDO.CODFORNEC = PCFORNEC.CODFORNEC
   AND PCEST.CODPROD      = PCPRODFILIAL.CODPROD
   AND PCEST.CODFILIAL    = PCPRODFILIAL.CODFILIAL
   AND PCPRODUT.CODEPTO   = PCDEPTO.CODEPTO
   AND PCMOVPREENT.CODPROD = PCITEM.CODPROD
   AND PCMOVPREENT.NUMSEQPED  = PCITEM.NUMSEQ
   AND PCMOVPREENT.NUMPED  = PCITEM.NUMPED
   and pcmovpreent.numnota =    PCNFENTPREENT.Numnota
   and pcmovpreent.numnota = '"""+nf+"'" )
  columns = [col[0] for col in cursor.description]
  cursor.rowfactory = lambda *args: dict(zip(columns, args))
  #cursor.fetchone()
  for i in cursor:
    data.append(i)
  cursor.close()
  return(data)
#select inf carga saida

"""{'NUMPED': 29423, 'CODFILIAL': '1', 'NUMSEQ': 1, 'CODPROD': 11182, 'EMBALAGEMMASTER': None, 'EMBALAGEM': '+OU-15,8KG', 'UNIDADE': 'KG', 'FORALINHA': 'N', 'NBM': '02071200', 'CODSEC': 10002, 'DESCRICAO': 'FRANGO CONG DALIA (PV)', 'CODEPTO': 10, 'DEPARTAMENTO': 'CONGELADOS', 'CODFORNEC': 8, 'FORNECEDOR': 'COOPERATIVA DALIA ALIMENTOS LTDA', 'CODPRODPRINC': 11182, 'PRAZOENTREGA': 0, 'DTULTENT': datetime.datetime(2020, 12, 1, 0, 0), 'QTUNIT': 1, 'QTUNITCX': 1, 'CUSTOREP': 7.012613, 'PCOMPRA': 6.1, 'QTINDENIZ': 0, 'QTBLOQUEADA': 0, 'QTPEDIDA': 3200, 'QTRESERV': 0, 'QTULTENT': 4211.49, 'TIPOEMBALAGEMPEDIDO': 'V', 'MULTIMPLOUNIDADEMASTER': 'N', 'STATUS': 'L'}"""




#saida do select

"""{'NUMNOTA': 2688, 'DTEMISSAO': datetime.datetime(2020, 12, 28, 0, 0), 'TIPOFRETE': 'C', 'FORNECEDOR': 'LATICINIO SANTA CLARA',
'CODFORNECPRINC': 193, 'TIPODESCARGA': '5', 'FUNCLANC': 'ANTONIA', 'VLTOTALITENS': 150, 'VLFRETE': 0, 'VLTOTAL': 155.1, 'STATUS': 'L', 'DTACHEGADA': datetime.datetime(2020, 12, 29, 9, 29, 34), 'QTITENS': 1, 'OBS': 'N Brinde: 74 EMPRESA OPTANTE PELO BENEFICIO FISCAL RICMS DECRETO 4676/01 ART 145 REFERENTE A NOTA FISCAL DE DEVOLUCAO N 3154124 EMITIDA DIA 19/12/2020 Impresso por: VANIA Transportador: LATICINIOS SANTA CLARA Frete por Conta: 0 - Contratacao do Frete por'}


{'NUMNOTA': 47865, 'DTEMISSAO': datetime.datetime(2021, 1, 9, 0, 0), 'TIPOFRETE': 'C', 'FORNECEDOR': 'FAVORITO COMERCIO INDUSTRIA CARNES LTDA', 'CODFORNECPRINC': 5, 'TIPODESCARGA': '1', 'FUNCLANC': 'ANTONIA', 'VLTOTALITENS': 257250, 'VLFRETE': 0, 'VLTOTAL': 257250, 'STATUS': 'L', 'DTACHEGADA': datetime.datetime(2021, 1, 11, 11, 21, 10), 'QTITENS': 1, 'OBS': None}


{'NUMNOTA': 265535, 'DTEMISSAO': datetime.datetime(2021, 1, 7, 0, 0), 'TIPOFRETE': 'F', 'FORNECEDOR': 'COOPAVEL COOPERATIVA AGROINDUSTRIAL', 'CODFORNECPRINC': 1910, 'TIPODESCARGA': '1', 'FUNCLANC': 'ANTONIA', 'VLTOTALITENS': 117600, 'VLFRETE': 0, 'VLTOTAL': 117600, 'STATUS': 'L', 'DTACHEGADA': datetime.datetime(2021, 1, 7, 17, 40, 14), 'QTITENS': 1, 'OBS': '|Cad:127710|(Trib. aprox R$15817.20 Federal e R$8232.00 Estadual Fonte:IBPT) PEDIDO : - Num. Ped. do Representante: 26906Login:38roginald-Mtr:44519**BOLETO**ALMEIDA**NJY4H79(CR)/NVX7799(CV)**MOT. WANDERSON**MAPA 29698**LACRE GQ COOPAVEL FRISUINOS 0035786*'}


{'NUMNOTA': 265536, 'DTEMISSAO': datetime.datetime(2021, 1, 7, 0, 0), 'TIPOFRETE': 'F', 'FORNECEDOR': 'COOPAVEL COOPERATIVA AGROINDUSTRIAL', 'CODFORNECPRINC': 1910, 'TIPODESCARGA': '1', 'FUNCLANC': 'ANTONIA', 'VLTOTALITENS': 49728, 'VLFRETE': 0, 'VLTOTAL': 49728, 'STATUS': 'L', 'DTACHEGADA': datetime.datetime(2021, 1, 7, 17, 40, 35), 'QTITENS': 1, 'OBS': '|Cad:127710|(Trib. aprox R$6688.41 Federal e R$3480.96 Estadual Fonte:IBPT) PEDIDO : - Num. Ped. do Representante: 26906Login:38roginald-Mtr:44519**BOLETO**ALMEIDA**NJY4H79(CR)/NVX7799(CV)**MOT. WANDERSON**MAPA 29698**LACRE GQ COOPAVEL FRISUINOS 0035786**'}


{'NUMNOTA': 17177, 'DTEMISSAO': datetime.datetime(2021, 1, 9, 0, 0), 'TIPOFRETE': 'C', 'FORNECEDOR': 'SANTA HELENA INDUSTRIA DE ALIMENTOS S/A', 'CODFORNECPRINC': 219, 'TIPODESCARGA': '1', 'FUNCLANC': 'ANTONIA', 'VLTOTALITENS': 147236.87, 'VLFRETE': 0, 'VLTOTAL': 147991, 'STATUS': 'D', 'DTACHEGADA': datetime.datetime(2021, 1, 9, 9, 11, 52), 'QTITENS': 18, 'OBS': 'CONSIGNATÁRIO Nome: RODOVITOR - TRANSPORTES E LOCACAO Endereço: R PEDRO DE TOLEDO 690 JARDIM SANTA LIDIA CEP: 07140-000 Cidade: GUARULHOS Estado: SP CNPJ: 08408736000296 Pedido: 0000398815 Representante de Vendas: FRIBEL COMERCIO DE ALIMENTOS LTDA - Telef'}


{'NUMNOTA': 1920450, 'DTEMISSAO': datetime.datetime(2021, 1, 11, 0, 0), 'TIPOFRETE': 'C', 'FORNECEDOR': 'COOPERATIVA DALIA ALIMENTOS LTDA', 'CODFORNECPRINC': 8, 'TIPODESCARGA': '1', 'FUNCLANC': 'ANTONIA', 'VLTOTALITENS': 292032, 'VLFRETE': 0, 'VLTOTAL':
292032, 'STATUS': 'L', 'DTACHEGADA': datetime.datetime(2021, 1, 12, 8, 34, 50), 'QTITENS': 1, 'OBS': None}


{'NUMNOTA': 47816, 'DTEMISSAO': datetime.datetime(2021, 1, 8, 0, 0), 'TIPOFRETE': 'C', 'FORNECEDOR': 'COOPERATIVA DALIA ALIMENTOS LTDA', 'CODFORNECPRINC': 8, 'TIPODESCARGA': '1', 'FUNCLANC': 'ANTONIA', 'VLTOTALITENS': 18995.92, 'VLFRETE': 0, 'VLTOTAL': 18995.92, 'STATUS': 'D', 'DTACHEGADA': datetime.datetime(2021, 1, 11, 15, 33, 45), 'QTITENS': 1, 'OBS': 'PEDIDO: SIM6133955F RESUMO: 1 COND. PGTO: 7 DD Pag. exclus. c/ boleto no banco. Nao nos resp. por pag. aos nossos repres., transp. e por deposito bancario. As mercadorias serao retiradas do armazem: Friozem Armazens Frigorificos Ltda, Rod BR 116, no 665,'}"""