import os
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
from dotenv import load_dotenv

load_dotenv()

def random_delay():
    return random.randint(4,14)

class TinderBot():

    def __init__(self):
        self.driver = webdriver.Chrome()
    
    def get_driver(self):
        return self.driver

    def login(self):
        driver = self.driver

        driver.get('http://tinder.com')

        # Accept terms
        driver.find_element_by_xpath('//*[@id="t-1801132545"]/div/div[2]/div/div/div[1]/button').click()
        sleep(random_delay())

        # Login button
        driver.find_element_by_xpath('//*[@id="t-1801132545"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/button').click()
        sleep(random_delay())

        # Login with phone number
        driver.find_element_by_xpath('//*[@id="t--239073259"]/div/div/div[1]/div/div[3]/span/div[3]/button').click()
        sleep(random_delay())

        # Try to wait for captcha modal to appear...
        try:
            WebDriverWait(driver, 200).until(
                EC.invisibility_of_element_located((By.ID, "arkoseInlineAnchor"))
            )
        except:
            pass
        
        # Introduce phone number
        driver.find_element_by_xpath('//*[@id="t--239073259"]/div/div/div[1]/div[2]/div/input').send_keys(os.getenv('PHONE_NUMBER'))
        sleep(random_delay())

        # Button "send sms"
        driver.find_element_by_xpath('//*[@id="t--239073259"]/div/div/div[1]/button').click()
        sleep(random_delay())

        # Ask for phone code
        sms_code = input("SMS Code: ")

        # SMS code inputs on each case
        for i in range(0,6):
            driver.find_element_by_xpath(f'//*[@id="t--239073259"]/div/div/div[1]/div[3]/input[{i+1}]').send_keys(sms_code[i])

        sleep(random_delay())

        # Continue button
        driver.find_element_by_xpath('//*[@id="t--239073259"]/div/div/div[1]/button').click()
        sleep(random_delay())

        # Email code handling
        email_code = input("Email code: ")

        for i in range(0,6):
            driver.find_element_by_xpath(f'//*[@id="t--239073259"]/div/div/div[1]/div[3]/input[{i+1}]').send_keys(email_code[i])
        
        sleep(random_delay())

        # Next button
        driver.find_element_by_xpath('//*[@id="t--239073259"]/div/div/div[1]/button').click()
        sleep(random_delay())

        # Try to accept notifications and stuff
        try:
            driver.find_element_by_xpath('//*[@id="t--239073259"]/div/div/div/div/div[3]/button[1]').click()
            sleep(random_delay())
            
            driver.find_element_by_xpath('//*[@id="t--239073259"]/div/div/div/div/div[3]/button[2]').click()
            sleep(random_delay())

        except:
            pass