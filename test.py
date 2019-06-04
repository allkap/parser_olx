from selenium import webdriver
import os
import time
from selenium.webdriver.common.action_chains import ActionChains


PATH = os.path.abspath('chromedriver')


class Bot:
    def __init__(self):




        self.driver = webdriver.Chrome()
        self.navigate()

    def navigate(self):
        list_links = []
        actions = ActionChains(driver=self.driver)


        main_link = 'https://www.olx.ua/transport/vodnyy-transport/'
        self.driver.get(main_link)

        obyavi_vse = len(self.driver.find_elements_by_xpath('//div[@class="offer   "]'))
        for i in range(obyavi_vse):
            oby = self.driver.find_elements_by_xpath('//div[@class="offer"]')[i]
            print(oby.text)
            time.sleep(3)
            link = oby.find_element_by_xpath('//a[@class="thumb vtop inlblk rel tdnone linkWithHash scale4 detailsLink "]')
            actions.move_to_element(link).perform()
            self.driver.execute_script("arguments[0].click();", link)
            time.sleep(50)







if __name__=='__main__':
    Bot()