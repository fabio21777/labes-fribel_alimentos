import cx_Oracle
from datetime import datetime, timedelta

def conexao_bd():
    connection = cx_Oracle.connect("FRIBEL", "1234569874",
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
        print(i,'\n\n')
      cursor.close()
      return(data)
    except:
      print("não foi carregada nenhuma carga do ERP")
      cursor.close()
      return(data)




#saida do select
"""{'NUMNOTA': 2688, 'DTEMISSAO': datetime.datetime(2020, 12, 28, 0, 0), 'TIPOFRETE': 'C', 'FORNECEDOR': 'LATICINIO SANTA CLARA', 'CODFORNECPRINC': 193, 'TIPODESCARGA': '5', 'FUNCLANC': 'ANTONIA', 'VLTOTALITENS': 150, 'VLFRETE': 0, 'VLTOTAL': 155.1, 'STATUS': 'L', 'DTACHEGADA': datetime.datetime(2020, 12, 29, 9, 29, 34), 'QTITENS': 1, 'OBS': 'N 
Brinde: 74 EMPRESA OPTANTE PELO BENEFICIO FISCAL RICMS DECRETO 4676/01 ART 145 REFERENTE A NOTA FISCAL DE DEVOLUCAO N 3154124 EMITIDA DIA 19/12/2020 Impresso por: VANIA Transportador: LATICINIOS SANTA CLARA Frete por Conta: 0 - Contratacao do Frete por'}


{'NUMNOTA': 454721, 'DTEMISSAO': datetime.datetime(2021, 1, 7, 0, 0), 'TIPOFRETE': 'C', 'FORNECEDOR': 'ABATEDOURO SOLON LTDA', 'CODFORNECPRINC': 1981, 'TIPODESCARGA': '1', 
'FUNCLANC': 'ANTONIA', 'VLTOTALITENS': 31258, 'VLFRETE': 0, 'VLTOTAL': 31258, 'STATUS': 'D', 'DTACHEGADA': datetime.datetime(2021, 1, 7, 11, 47, 41), 'QTITENS': 3, 'OBS': 'Produto isento de ICMS, cfe Anexo II, Art.23, Inciso III e com altera  es dada pelo Decreto 1.383/15 com efeitos a partir de 04/09/2015 do RICMS/PA. Venda com al quota zero do PIS/COFINS, cfe. Lei 12.839 de 09/ 07/2013. Pedido:406958'}


{'NUMNOTA': 1914788, 'DTEMISSAO': datetime.datetime(2020, 12, 29, 0, 0), 'TIPOFRETE': 'C', 'FORNECEDOR': 'COOPERATIVA DALIA ALIMENTOS LTDA', 'CODFORNECPRINC': 8, 'TIPODESCARGA': '1', 'FUNCLANC': 'ANTONIA', 'VLTOTALITENS': 28839.62, 'VLFRETE': 0, 'VLTOTAL': 28839.62, 'STATUS': 'D', 'DTACHEGADA': datetime.datetime(2020, 12, 31, 12, 52, 40), 'QTITENS': 2, 'OBS': 'PEDIDO: 9395343 RESUMO: 1 COND. PGTO: 28 DD LACRE: 0017952 TEMP.: -12 GRAUS OU MAIS CONGELADOS ICMS S/SERVICO DE TRANSPORTE RICMS LIVRO III ARTIGO 54 DO 
DECRETO 37699/97.VALOR DO FRETE - R$ 1.057,14- VALOR DA BASE DE CALCULO - R$ 1.057,14 - VALOR DO ICMS'}


{'NUMNOTA': 1914789, 'DTEMISSAO': datetime.datetime(2020, 12, 29, 0, 0), 'TIPOFRETE': 'C', 'FORNECEDOR': 'COOPERATIVA DALIA ALIMENTOS LTDA', 'CODFORNECPRINC': 8, 'TIPODESCARGA': '5', 'FUNCLANC': 'ANTONIA', 'VLTOTALITENS': 9992.11, 'VLFRETE': 0, 'VLTOTAL': 9992.11, 'STATUS': 'D', 'DTACHEGADA': datetime.datetime(2020, 12, 31, 12, 53, 4), 'QTITENS': 1, 'OBS': 'PEDIDO: 9395345 RESUMO: 2 ICMS S/SERVICO DE TRANSPORTE RICMS LIVRO III ARTIGO 54 DO DECRETO 37699/97.VALOR DO FRETE - R$ 314,29 - VALOR DA BASE DE CALCULO - R$ 314,29 - VALOR DO ICMS S/FRETE - R$ 22,00 Placas: MFB4366 e SCTransp. Redespa:C L KLOSS E CIA L'}"""