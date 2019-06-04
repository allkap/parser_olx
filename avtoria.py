from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import telebot
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from olx_tel import add_to_db

from config import token
from random import randint, random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver.support import expected_conditions as EC

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

client = gspread.authorize(creds)

sheet = client.open('testsheets').sheet1

PATH = os.path.abspath('chromedriver.exe')

# state = str(input("Введите название региона: "))
state_dict = {'Киев':'kiev','Херсон':'kherson','Одесса':'odessa'}



class Bot:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        self.driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=options)
        self.navigate()

    def navigate(self):
        wait = WebDriverWait(self.driver, 5)


        for k in range(1,20):
            main_link = 'https://auto.ria.com/state/kiev/?page={}'.format(k)
            self.driver.get(main_link)
            time.sleep(2)
            links= self.driver.find_elements_by_xpath("//a[@data-template-v='6']")
            self.driver.execute_script("window.scrollTo(0, 2950)")





            for i in range(len(links)-1):
                self.driver.implicitly_wait(randint(2, 4))
                linkk = self.driver.find_elements_by_xpath("//a[@data-template-v='6']")[i]
                self.driver.execute_script("arguments[0].click();", linkk)
                self.driver.implicitly_wait(randint(1,3))

                try:
                    try:
                        number = self.driver.find_element_by_xpath('//span[@title="Перевірений телефон"]').get_attribute('data-phone-number')
                    except:
                        number = self.driver.find_element_by_xpath('//span[@title="Проверенный телефон"]').get_attribute('data-phone-number')

                    try:
                        name = self.driver.find_element_by_xpath('//h4[@class="seller_info_name bold"]').text
                    except:
                        name = 'Без имени'
                    add_to_db(number,name)
                    self.driver.implicitly_wait(randint(1,3))

                    self.driver.back()
                    self.driver.implicitly_wait(randint(2, 4))

                except:
                    self.driver.back()
                    self.driver.implicitly_wait(randint(2, 4))





if __name__=='__main__':
    Bot()