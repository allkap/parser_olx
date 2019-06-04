from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import telebot
import time
import os
from selenium.webdriver.support.ui import WebDriverWait

from config import token
from random import randint, random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver.support import expected_conditions as EC

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

client = gspread.authorize(creds)

sheet = client.open('testsheets').sheet1

bot = telebot.TeleBot(token)

rubrick_url ={'Транспорт':'transport','Автобусы':'avtobusy','Прицепы / дома на колесах':'pritsepy-doma-na-kolesah','Автозапчасти и аксессуары':'avtozapchasti-i-aksessuary','Мотозапчасти и аксессуары':'motozapchasti-i-aksessuary','Шины, диски и колёса':'shiny-diski-i-kolesa','Запчасти для спец техники':'zapchasti-dlya-spets-sh-tehniki','Прочие запчасти':'prochie-zapchasti','Сельхозтехника':'selhoztehnika','Автомобили из Польши':'avtomobili-iz-polshi','Водный Транспорт':'vodnyy-transport','Грузовые автомобили':'gruzovye-avtomobili','Спецтехника':'spetstehnika','Мото':'moto','Недвижемость':'nedvizhimost', 'Услуги':'uslugi','Запчасти для транспорта':'zapchasti-dlya-transporta','Электроника':'elektronika'}
region_url ={"Херсон":'khe', 'Одесса':'od','Винница':'vin','Волынская область':'vol','Днепропетровск':'dnp','Житомир':'zht','Ивано-Франковск':'if','Киев':'ko','Николаев':'nikolaev_106'}

rubrick_rus = {'Транспорт':
                ['Сельхозтехника','Автобусы','Прицепы/домы на колесах','Автомобили из Польши','Водный транспорт','Другой транспорт','Грузовые автомобили','Спецтехника','Воздушный транспорт','Запчасти для транспорта'],
                'Запчасти для транспорта':
                ['Автозапчасти и аксессуары','Мотозапчасти и аксессуары','Шины, диски и колёса','Прочие запчасти','Транспорт','Запчасти для спец техники'],
               'Недвижемость':
               ['Квартиры, комнаты','Коммерческая недвижимость','Предложения от застройщиков','Дома','Гаражи, парковки','Недвижимость за рубежом','Земля','Посуточная аренда жилья'],

                }

region_rus = ['Херсон', 'Одесса','Винница','Днепропетровск','Киев','Николаев','Житомир','Волынская область','Ивано-Франковск']

choosen_rubrick = ''
choosen_region = ''
PATH = os.path.abspath('chromedriver.exe')




@bot.message_handler(commands=['start_new_search'])
def choose_rubr(message):
    bot.send_message(message.chat.id, text='Напишите название рубрики из перечисленных: ' +', '.join([r for r in rubrick_rus.keys()]))
    bot.register_next_step_handler(message, choose_region)

def choose_pod_rubr(message):
    bot.send_message(message.vhat.id, 'Выбирите подрубрику из перечисленных: ')

def choose_region(message):
    global choosen_rubrick
    choosen_rubrick=message.text
    bot.send_message(message.chat.id, text='Напишите название региона из перечисленных: ' + ' ,'.join([r for r in region_rus]))
    bot.register_next_step_handler(message, to_end)
def to_end(message):
    try:
        global choosen_region
        choosen_region=message.text
        bot.send_message(message.chat.id, 'Вы выбрали рубрику - '+choosen_rubrick+' и регион - '+choosen_region)
        bot.send_message(message.chat.id, 'Начинаю сбор данных ...')
        global choosen_rubrick_url, choosen_region_url
        choosen_rubrick_url = rubrick_url[choosen_rubrick]
        choosen_region_url = region_url[choosen_region]
        b = Bot()
    except Exception as e:
        bot.send_message(message.chat.id, 'yyyyyyy'+str(e))



class Bot:
    def __init__(self):


        PROXY = '185.86.76.225:1080'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=socks5://%s' % PROXY)


        self.driver = webdriver.Chrome(executable_path=PATH, chrome_options=chrome_options)
        self.navigate()


    def navigate(self):
        list_links = []
        actions = ActionChains(driver=self.driver)
        imwait = self.driver.implicitly_wait(randint(2, 4))

        main_link = 'https://www.olx.ua/'+str(choosen_rubrick_url)+'/'+str(choosen_region_url)+'/'
        self.driver.get(main_link)

        pages = self.driver.find_elements_by_xpath('//a[@class="block br3 brc8 large tdnone lheight24"]')
        wait = WebDriverWait(self.driver, 5)
        pages_list = []
        for page in pages:
            pages_list.append(page.get_property('href'))
        count_pages = len(pages_list)+1
        print(count_pages)
        for i in range(1,count_pages):
            self.driver.get(main_link+'?page={}'.format(i))
            offers = self.driver.find_elements_by_xpath('//a[@class="marginright5 link linkWithHash detailsLink"]')
            for link in offers:
                list_links.append(link.get_attribute('href'))
            for link in list_links:
                self.driver.execute_script("window.scrollTo(0, 150)")
                self.driver.get(link)
                time.sleep(randint(2,4))
                print('Перешли по ссылке')

#                   print('прокрутим страницу')
                self.driver.execute_script("window.scrollTo(0, 300)")
                print('прокрутили')
                try:
                    time.sleep(randint(2,4))

                    print('найдем кнопку')
                    but_w = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-rel="phone"]')))
                    but = self.driver.find_element_by_xpath('//div[@data-rel="phone"]')
                    self.driver.execute_script("arguments[0].click();", but)
                    but.click()
                    print('Нажали на кнопку')


                    self.driver.execute_script("window.scrollTo(0, 150)")
                    time.sleep(randint(2,4))



                    number = self.driver.find_element_by_xpath('//strong[@class="xx-large"]').text
                    name = self.driver.find_element_by_tag_name('h4').text
                    add_to_db(number, name)
                    time.sleep(randint(2,4))

                    self.driver.execute_script("window.scrollTo(0, 350)")
                    print('Добавили в БД сделали скролл ')


    #
                    print('Еще не вернулись назад')
                    self.driver.execute_script("window.scrollTo(0, 350)")
                    self.driver.back()
                    print('вернулись назад')
                    time.sleep(randint(2,4))

                    self.driver.execute_script("window.scrollTo(0, 350)")
                except:
                    time.sleep(3)
                    self.driver.back()
            print('tut vse rabotaet')
        print('собрал 1 номер')

def in_db(number):
    try:
        sheet.find(number)

        return True
    except:
        return False
def add_to_db(number, name):
    if in_db(number):
        pass
    else:
        user_info = [number, name]
        sheet.insert_row(user_info)





if __name__=='__main__':

    bot.polling(none_stop=True)