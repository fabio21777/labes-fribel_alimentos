from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from selenium import webdriver
import re
import os
class newbot:
    dir_path = os.getcwd()
    chromedriver = os.path.join(dir_path, "chromedriver.exe")
    profile = os.path.join(dir_path, "profile", "wpp")
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(
            r"user-data-dir={}".format(self.profile))
        self.driver = webdriver.Chrome(
            self.chromedriver, chrome_options=self.options)

    def zap(self,numero,mensagem):
        try:
            part1='https://api.whatsapp.com/send?phone='
            part2=numero
            part3='&text='
            part4=mensagem
            link=part1+part2+part3+part4
            site  = link
            self.driver.get(site)
            self.driver.implicitly_wait(40)
            self.driver.find_element_by_xpath('//*[@id="action-button"]').click()
            self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button').click()
            self.driver.implicitly_wait(40)
            time.sleep(2)
            self.driver.close()
        except:
            self.driver.close()
            self.erro()
	
    def EnviarMensagens_grupo(self,grupos_ou_pessoas,mensagem):
        try:
            print('--->',grupos_ou_pessoas,mensagem)
            self.driver.get('https://web.whatsapp.com')
            time.sleep(5)
            for grupo_ou_pessoa in grupos_ou_pessoas:
                campo_grupo = self.driver.find_element_by_xpath(f"//span[@title='Teste']")
                time.sleep(3)
                campo_grupo.click()
                chat_box = self.driver.find_element_by_class_name('DuUXI')
                time.sleep(3)
                chat_box.click()
                chat_box.send_keys(mensagem+'teste')
                botao_enviar = self.driver.find_element_by_xpath(
                    "//span[@data-icon='send']")
                time.sleep(3)
                botao_enviar.click()
                time.sleep(5)
                self.driver.close()
        except:
            print('errro no selenium zap')
            self.driver.close()
        
#bott = newbot()
#bott.EnviarMensagens_grupo('Teste','teste')
