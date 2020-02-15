from selenium import webdriver
from time import sleep
from data import phone_number, confirmation_code

class TinderBot():

    def __init__(self):
        self.driver = webdriver.Firefox()

    def login(self):
        self.driver.get('http://tinder.com')

        sleep(5)

        phone_number_btn = self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[3]/div[1]/button')
        phone_number_btn.click()
        sleep(5)

        # Phone input
        phone_input = self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div/input')
        phone_input.send_keys(phone_number)

        continue_btn = self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/button/span')
        continue_btn.click()
        sleep(5)

        # Confirmation cells
        cell_1 = bot.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[3]/input[1]')
        cell_2 = bot.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[3]/input[2]')
        cell_3 = bot.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[3]/input[3]')
        cell_4 = bot.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[3]/input[4]')
        cell_5 = bot.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[3]/input[5]')
        cell_6 = bot.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[3]/input[6]')

        cell_1.send_keys(confirmation_code[0])
        cell_2.send_keys(confirmation_code[1])
        cell_3.send_keys(confirmation_code[2])
        cell_4.send_keys(confirmation_code[3])
        cell_5.send_keys(confirmation_code[4])
        cell_6.send_keys(confirmation_code[5])

        continue_btn = self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/button')
        continue_btn.click()



