from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def espera_alert(browser):
    try:
        WebDriverWait(browser, 3).until(EC.alert_is_present(),'Timed out waiting for PA creation ' +'confirmation popup to appear.')
        alert = browser.switch_to.alert
        alert.accept()
        print("alert accepted")
    except TimeoutException:
        print("no alert")
    
def teste_selenium_add_carga(ind='teste_selenium_add_carga_default',nf='03459875631475_selenium_default',tpentrada='Entrada Normal_selenium_default',previsão='20-01-2020',produto='carne_selenium_default',qtd='10000',un='CX',movimentacao='Carga batida',frete='FOB',observacao ='teste_selenium_add_carga_default'):
    browser = webdriver.Chrome()
    browser.maximize_window ()
    browser.get('http://127.0.0.1:8000/acompanhamento/adicionarCarga/')
    inputElement_ind = browser.find_element_by_id("industria")
    inputElement_ind.send_keys(ind)
        #####################################################
    inputElement_nf=browser.find_element_by_id("NF")
    inputElement_nf.send_keys(nf)
        #####################################################
    inputElement_tpentrada=browser.find_element_by_id("tipo_entrada")
    inputElement_tpentrada.send_keys(tpentrada)
        ######################################################
    inputElement_previsão=browser.find_element_by_id("previsao")
    inputElement_previsão.send_keys(previsão)
        ######################################################
    inputElement_produto=browser.find_element_by_id("Produto")
    inputElement_produto.send_keys(produto)
        ########################################################
    inputElement_qtd=browser.find_element_by_id("QTD")
    inputElement_qtd.send_keys(qtd)
        ##########################################################
    inputElement_un=browser.find_element_by_id("un")
    inputElement_un.send_keys(un)
        #############################################################
    inputElement_movimentacao=browser.find_element_by_id("movimentacao")
    inputElement_movimentacao.send_keys(movimentacao)
        ##############################################################
    inputElement_frete=browser.find_element_by_id("frete")
    inputElement_frete.send_keys(frete)
        ###############################################################
    inputElement_observacao=browser.find_element_by_id("observacao")
    inputElement_observacao.send_keys(observacao)
        ################################################################
    inputElement_btadd=browser.find_element_by_id("btadd").click()
    espera_alert(browser)
    espera_alert(browser)
    url=browser.current_url
    time.sleep(5)
    browser.close()
    return(url)
   
def validar_teste(teste):
    if teste == 'http://127.0.0.1:8000/acompanhamento/adicionarCarga/':
        return (True)
    else:
        return (False)
def selenium_Campo_Indústria():
    resultado=[]
    teste1=teste_selenium_add_carga(ind='1234567899874563214569874125896321458796',nf='034598756314758',tpentrada='Entrada Normal',previsão='22-01-2021',produto='chaque',qtd='10000',un='KG',movimentacao='Carga Paletizada',frete='CIF',observacao ='teste campo industria')
    teste2=teste_selenium_add_carga(ind='123456789987456321456987412589632145879656942',nf='03459875639958',tpentrada='Entrada Normal',previsão='22-01-2021',produto='chaque',qtd='10000',un='KG',movimentacao='Carga Paletizada',frete='CIF',observacao ='teste campo industria')
    teste3=teste_selenium_add_carga(ind=' 234567899874563214569874125896321458796',nf='034598756634758',tpentrada='Entrada Normal',previsão='22-01-2021',produto='chaque',qtd='10000',un='KG',movimentacao='Carga Paletizada',frete='CIF',observacao ='teste campo industria')
    if validar_teste(teste1)==True:
        resultado.append('teste1 Fail')
    else:
        resultado.append('teste1 Pass')
    if validar_teste(teste2)==True:
        print(teste2)
        resultado.append('teste2 Pass')
    else:
        resultado.append('teste2 Fail')
    if validar_teste(teste3)==True:
        resultado.append('teste3 Pass')
    else:
        resultado.append('teste3 Fail')
    return (resultado)

def selenium_Campo_Nota_Fiscal():
    resultado=[]
    teste4=teste_selenium_add_carga(ind='1234567899874563214569874125896321458796',nf='51080701212344000127550010000000981364117781',tpentrada='Entrada Normal',previsão='22-01-2021',produto='chaque',qtd='10000',un='KG',movimentacao='Carga Paletizada',frete='CIF',observacao ='Campo_Nota_Fiscal')
    teste5=teste_selenium_add_carga(ind='1234567899874563214569874125896321458796',nf='5108070121234400012755001@#00000981364117781',tpentrada='Entrada Normal',previsão='22-01-2021',produto='chaque',qtd='10000',un='KG',movimentacao='Carga Paletizada',frete='CIF',observacao ='Campo_Nota_Fiscal')
    teste6=teste_selenium_add_carga(ind='1234567899874563214569874125896321458796',nf='510807012123440',tpentrada='Entrada Normal',previsão='22-01-2021',produto='chaque',qtd='10000',un='KG',movimentacao='Carga Paletizada',frete='CIF',observacao ='Campo_Nota_Fiscal')
    if validar_teste(teste4)==True:
        resultado.append('teste4 Fail')
    else:
        resultado.append('teste4 Pass')
    if validar_teste(teste5)==True:
        resultado.append('teste5 Pass')
    else:
        resultado.append('teste5 Fail')
    if validar_teste(teste6)==True:
        resultado.append('teste6 Pass')
    else:
        resultado.append('teste6 Fail')
    return (resultado)
def selenium_Campo_Previsão():
    resultado=[]
    teste7=teste_selenium_add_carga(ind='1234567899874563214569874125896321458796',nf='51080701212344000127550010000000981364117781',tpentrada='Entrada Normal',previsão='15-01-2021',produto='nescal',qtd='5000',un='KG',movimentacao='Carga Paletizada',frete='CIF',observacao ='Campo_Previsão')
    teste8=teste_selenium_add_carga(ind='1234567899874563214569874125896321458796',nf='51080701212344000127550010000000981364117781',tpentrada='Entrada Normal',previsão=date.today(),produto='nescal',qtd='5000',un='KG',movimentacao='Carga Paletizada',frete='CIF',observacao ='Campo_Previsão')
    teste9=teste_selenium_add_carga(ind='1234567899874563214569874125896321458796',nf='51080701212344000127550010000000981364117781',tpentrada='Entrada Normal',previsão='15-01-2020',produto='nescal',qtd='5000',un='KG',movimentacao='Carga Paletizada',frete='CIF',observacao ='Campo_Previsão')
    teste10=teste_selenium_add_carga(ind='1234567899874563214569874125896321458796',nf='51080701212344000127550010000000981364117781',tpentrada='Entrada Normal',previsão='15-01-202020',produto='nescal',qtd='5000',un='KG',movimentacao='Carga Paletizada',frete='CIF',observacao ='Campo_Previsão')
    teste11=teste_selenium_add_carga(ind='1234567899874563214569874125896321458796',nf='51080701212344000127550010000000981364117781',tpentrada='Entrada Normal',previsão='15-10',produto='nescal',qtd='5000',un='KG',movimentacao='Carga Paletizada',frete='CIF',observacao ='Campo_Previsão')
    if validar_teste(teste7)==True:
        resultado.append('teste 7 Fail')
    else:
        resultado.append('teste 7 Pass')
    if validar_teste(teste8)==True:
        resultado.append('teste 8 Fail')
    else:
        resultado.append('teste 8 Pass')
    if validar_teste(teste9)==True:
        resultado.append('teste 9 Pass')
    else:
        resultado.append('teste 9 Fail')
    if validar_teste(teste10)==True:
        resultado.append('teste 10 Pass')
    else:
        resultado.append('teste 10 Fail')
    if validar_teste(teste11)==True:
        resultado.append('teste 11 Pass')
    else:
        resultado.append('teste 11 Fail')
    return (resultado)
def selenium_Campo_QTD():
    resultado=[]
    teste12=teste_selenium_add_carga(ind='1234567899874563214569874125896321458796',nf='51080701212344000127550010000000981364117781',tpentrada='Entrada Normal',previsão='15-10-2021',produto='nescal',qtd='10',un='KG',movimentacao='Carga Paletizada',frete='CIF',observacao ='Campo_Previsão')
    teste13=teste_selenium_add_carga(ind='1234567899874563214569874125896321458796',nf='51080701212344000127550010000000981364117781',tpentrada='Entrada Normal',previsão='15-10-2021',produto='nescal',qtd='1000000000000000',un='KG',movimentacao='Carga Paletizada',frete='CIF',observacao ='Campo_Previsão')
    if validar_teste(teste12)==True:
        resultado.append('teste 12 Fail')
    else:
        resultado.append('teste 12 Pass')
    if validar_teste(teste13)==True:
        resultado.append('teste 13 Pass')
    else:
        resultado.append('teste 13 Fail')
    return(resultado)
def  selenium_Produto():
    resultado=[]
    teste14=teste_selenium_add_carga(ind='1234567899874563214569874125896321458796',nf='51080701212344000127550010000000981364117781',tpentrada='Entrada Normal',previsão='15-10-2021',produto='refrigerante',qtd='100000',un='KG',movimentacao='Carga Paletizada',frete='CIF',observacao ='Campo_Previsão')
    teste15=teste_selenium_add_carga(ind='1234567899874563214569874125896321458796',nf='51080701212344000127550010000000981364117781',tpentrada='Entrada Normal',previsão='15-10-2021',produto='"refrigerante leite café suco de laranja energético',qtd='100000',un='KG',movimentacao='Carga Paletizada',frete='CIF',observacao ='Campo_Previsão')
    if validar_teste(teste14)==True:
        resultado.append('teste 14 Fail')
    else:
        resultado.append('teste 14 Pass')
    if validar_teste(teste15)==True:
        resultado.append('teste 15 Pass')
    else:
        resultado.append('teste 15 Fail')
    return(resultado)
def selenium_Tipo_de_Entrada():
    resultado=[]
    teste16=teste_selenium_add_carga(ind='1234567899874563214569874125896321458796',nf='51080701212344000127550010000000981364117781',tpentrada='Entrada errada',previsão='15-10-2021',produto='refrigerante',qtd='100000',un='KG',movimentacao='Carga Paletizada',frete='CIF',observacao ='Campo_Previsão')
    teste17=teste_selenium_add_carga(ind='1234567899874563214569874125896321458796',nf='51080701212344000127550010000000981364117781',tpentrada='Carga batida',previsão='15-10-2021',produto='refrigerante',qtd='100000',un='KG',movimentacao='Carga Paletizada',frete='CIF',observacao ='Campo_Previsão')
    if validar_teste(teste16)==True:
        resultado.append('teste 16 Pass')
    else:
        resultado.append('teste 16 Fail')
    if validar_teste(teste17)==True:
        resultado.append('teste 17 Fail')
    else:
        resultado.append('teste 17 Pass')
    return(resultado)