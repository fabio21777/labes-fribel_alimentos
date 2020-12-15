from django.test import TestCase
from .models import Carga
import datetime
from datetime import date
from django.contrib.auth.models import User

# Create your tests here.
class Cargatestecase(TestCase):
    def setUp(self):
        Carga.objects.create(numero_nf= '51080701212344000127550010000000981364117781',industria='123456789987456321456987412589632145870',dia_descarga='2020-12-15',user=User.objects.get(pk=1),status='aguardando',tipo_entrada='paletizada',Produto='refrigerante',QTD='10000000',UN='kg',movimentacao='normal',frete='fob',observacao='teste')#teste industria
        Carga.objects.create(numero_nf= '51080701212344000127550010000000981364117781',industria='   123456789987456321456987412589632145',dia_descarga='2020-12-15',user=User.objects.get(pk=1),status='aguardando',tipo_entrada='paletizada',Produto='refrigerante',QTD='10000000',UN='kg',movimentacao='normal',frete='fob',observacao='teste')#teste industria
        Carga.objects.create(numero_nf= '51080701212344000127550010000000981364117781',industria='123456789987456321456987412589632145',dia_descarga='2020-12-15',user=User.objects.get(pk=1),status='aguardando',tipo_entrada='paletizada',Produto='refrigerante',QTD='10000000',UN='kg',movimentacao='normal',frete='fob',observacao='teste') #NF
        Carga.objects.create(numero_nf= '51080701212344000127550010000364117781',industria='123456789987456321456987412589632145',dia_descarga='2020-12-15',user=User.objects.get(pk=1),status='aguardando',tipo_entrada='paletizada',Produto='refrigerante',QTD='10000000',UN='kg',movimentacao='normal',frete='fob',observacao='teste') #NF
        Carga.objects.create(numero_nf= '51080701212344000127550010000364117781101010',industria='123456789987456321456987412589632145',dia_descarga='2020-12-15',user=User.objects.get(pk=1),status='aguardando',tipo_entrada='paletizada',Produto='refrigerante',QTD='10000000',UN='kg',movimentacao='normal',frete='fob',observacao='teste') #data
        Carga.objects.create(numero_nf= '51080701212344000127550010000364117781101010',industria='123456789987456321456987412589632145',dia_descarga='2020-12-10',user=User.objects.get(pk=1),status='aguardando',tipo_entrada='paletizada',Produto='refrigerante',QTD='10000000',UN='kg',movimentacao='normal',frete='fob',observacao='teste') #data



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
    def test_Cargas_previsao_entrada_invalida(self):
        carga6=Carga.objects.get(dia_descarga='2020-12-15')
        dia_descarga=carga5.dia_descarga.split('-')
        dia_descarga=datetime.datetime(dia_descarga[0],dia_descarga[1],dia_descarga[2])
        if (dia_descarga>date.today()):
            invalido=True
        else:
            invalido=False

    

