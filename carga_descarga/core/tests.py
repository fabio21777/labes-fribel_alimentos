from django.test import TestCase
from .models import Carga
import datetime
from datetime import date
from django.contrib.auth.models import User

# Create your tests here.
'''class Cargatestecase(TestCase):
    def setUp(self):
        try:
            Carga.objects.create(numero_nf= '51080701212344000127550010000000981364117781',industria='123456789987456321456987412589632145870',dia_descarga='2020-12-15',user=User.objects.get(pk=1),status='aguardando',tipo_entrada='paletizada',Produto='refrigerante',QTD='10000000',UN='kg',movimentacao='normal',frete='fob',observacao='teste')#teste industria
            Carga.objects.create(numero_nf= '51080701212344000127550010000000981364117781',industria='   123456789987456321456987412589632145',dia_descarga='2020-12-15',user=User.objects.get(pk=1),status='aguardando',tipo_entrada='paletizada',Produto='refrigerante',QTD='10000000',UN='kg',movimentacao='normal',frete='fob',observacao='teste')#teste industria
            Carga.objects.create(numero_nf= '51080701212344000127550010000000981364117781',industria='123456789987456321456987412589632145',dia_descarga='2020-12-15',user=User.objects.get(pk=1),status='aguardando',tipo_entrada='paletizada',Produto='refrigerante',QTD='10000000',UN='kg',movimentacao='normal',frete='fob',observacao='teste') #NF
            Carga.objects.create(numero_nf= '51080701212344000127550010000364117781',industria='123456789987456321456987412589632145',dia_descarga='2020-12-15',user=User.objects.get(pk=1),status='aguardando',tipo_entrada='paletizada',Produto='refrigerante',QTD='10000000',UN='kg',movimentacao='normal',frete='fob',observacao='teste') #NF
            Carga.objects.create(numero_nf= '51080701212344000127550010000364117781101010',industria='123456789987456321456987412589632145',dia_descarga='2020-12-15',user=User.objects.get(pk=1),status='aguardando',tipo_entrada='paletizada',Produto='refrigerante',QTD='10000000',UN='kg',movimentacao='normal',frete='fob',observacao='teste') #data
            Carga.objects.create(numero_nf= '51080701212344000127550010000364117781101010',industria='123456789987456321456987412589632145',dia_descarga='2020-12-10',user=User.objects.get(pk=1),status='aguardando',tipo_entrada='paletizada',Produto='refrigerante',QTD='10000000',UN='kg',movimentacao='normal',frete='fob',observacao='teste') #data
            Carga.objects.create(numero_nf= '51454860701212345054545454554545454545445545',industria='123456789987456321456987412589632145',dia_descarga='2020-12-10',user=User.objects.get(pk=1),status='aguardando',tipo_entrada='paletizada',Produto='refrigerante',QTD='10000000',UN='kg',movimentacao='normal',frete='fob',observacao='teste') #QTD
            Carga.objects.create(numero_nf= '51080701212344000127550021234400012755009864',industria='123456789987456321456987412589632145',dia_descarga='2020-12-10',user=User.objects.get(pk=1),status='aguardando',tipo_entrada='paletizada',Produto='refrigerante',QTD='1000000000000000000000',UN='kg',movimentacao='normal',frete='fob',observacao='teste') #QTD
            Carga.objects.create(numero_nf= '51080701212344000127550021234400012755009864',industria='123456789987456321456987412589632145',dia_descarga='2020-12-10',user=User.objects.get(pk=1),status='aguardando',tipo_entrada='paletizada',Produto='refrigerante',QTD='1000000000000000000000',UN='kg',movimentacao='normal',frete='fob',observacao='teste') #QTD
            Carga.objects.create(numero_nf= '51080701212344000127550021234400012759657895',industria='123456789987456321456987412589632145',dia_descarga='2020-12-10',user=User.objects.get(pk=1),status='aguardando',tipo_entrada='paletizada',Produto='',QTD='100000000',UN='kg',movimentacao='normal',frete='fob',observacao='teste') #prod
            Carga.objects.create(numero_nf= '51080701212344000127550021963214587456987456',industria='123456789987456321456987412589632145',dia_descarga='2020-12-10',user=User.objects.get(pk=1),status='aguardando',tipo_entrada='paletizada',Produto='refrigerante com banana e suco de maracujar com leite em po',QTD='100000000',UN='kg',movimentacao='normal',frete='fob',observacao='teste') #prod
            Carga.objects.create(numero_nf= '51080701212344000127550021963214587456987456',industria='nescal',dia_descarga='2020-12-10',user=User.objects.get(pk=1),status='aguardando',tipo_entrada='paletizada',Produto='refrigerante',QTD='100000000',UN='kg',movimentacao='normal',frete='fob',observacao='teste') #pesquisar

        except:
            print('não foi posivel fazer os setup dos teste')


    def test_Cargas_industria_entrada_valida(self):
        carga1=Carga.objects.get(industria='1234567899874563214569874125896321458796')
        self.assertEqual(len(carga1.industria),len('1234567899874563214569874125896321458796'))

    def test_Cargas_industria_entrada_invalida(self):
        carga2=Carga.objects.get(industria='   123456789987456321456987412589632145')
        self.assertEqual(carga2.industria,'123456789987456321456987412589632145')
    def test_Cargas_NF_entrada_valida(self):
        carga3=Carga.objects.get(numero_nf= '51080701212344000127550010000000981364117781')
        if (len (carga3.numero_nf)==44):
            valido=True
        else:
             valido=False
        self.assertEqual(valido,True)
    def test_Cargas_NF_entrada_invalida(self):
        carga4=Carga.objects.get(numero_nf= '51080701212344000127550010000000981')
        if len (carga4.numero_nf)!=44:
            invalido=True
        else:
            invalido=False
        self.assertEqual(invalido,True)
    def test_Cargas_previsao_entrada_valida(self):
        carga5=Carga.objects.get(dia_descarga='2020-12-10')
        dia_descarga=carga5.dia_descarga.split('-')
        dia_descarga=datetime.datetime(dia_descarga[0],dia_descarga[1],dia_descarga[2])
        if (dia_descarga<date.today()):
            valido=True
        else:
            valido=False
        self.assertEqual(valido,True)
        
    def test_Cargas_previsao_entrada_invalida(self):
        carga6=Carga.objects.get(dia_descarga='2020-12-15')
        dia_descarga=carga5.dia_descarga.split('-')
        dia_descarga=datetime.datetime(dia_descarga[0],dia_descarga[1],dia_descarga[2])
        if (dia_descarga>date.today()):
            invalido=True
        else:
            invalido=False
        self.assertEqual(invalido,True)
    def test_Cargas_QTD_valida(self):
        carga7=Carga.object.get(numero_nf='51454860701212345054545454554545454545445545')
        if len(carga7.QTD)<=40:
            valido=True
        self.assertEqual(valido,True)
    def test_Cargas_QTD_invalida(self):
        carga8=Carga.object.get(numero_nf='51080701212344000127550021234400012755009864')
        if len(carga8.QTD)>40:
            invalido=True
        self.assertEqual(invalido,True)
    def test_Cargas_produto_valida(self):
        carga9=Carga.object.get(numero_nf='51080701212344000127550021234400012759657895')
        if len(carga9.QTD)<=40:
            valido=True
        self.assertEqual(valido,True)
    def test_Cargas_produto_invalida(self):
        carga10=carga.object.get(numero_nf='51080701212344000127550021963214587456987456')
        if len(carga10.QTD)>40:
            invalido=True
        self.assertEqual(invalido,True)
    def Estória_Listar_cargas_Campo_pesquisar_valido(self)
        try:
            carga11=Carga.objects.filter(industria__icontains='123456789987456321456987412589632145')
        except:
            print("erro!!")
        if len(carga11)>0:
            valido=True
        self.assertEqual(valido,True)
    def Estória_Listar_cargas_Campo_pesquisar_invalido(self)
        try:
            carga12=Carga.objects.filter(industria__icontains=' 123456789987456321456987412589632145')
        except:
            print("erro!!")
        if len(carga12)==0:
            invalido=True
        self.assertEqual(valido,True)
    def Estória_Listar_cargas_Campo_pesquisar_case_sensitive_valido(self)
        try:
            carga13=Carga.objects.filter(industria__icontains='Nescal')
        except:
            print("erro!!")
        if len(carga13)>0:
            valido=True
        self.assertEqual(valido,True)'''
    

        




    

