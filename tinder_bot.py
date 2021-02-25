import os
import random
import requests
import shutil

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
from dotenv import load_dotenv

from use_model import predict_from_img_path

load_dotenv()

def random_delay():
    return random.randint(2,8)

def parse_img_url_from_inline_style(style_string):
    if 'background-image' in style_string:
        style_string = style_string.split(' url("')[1].replace('");', '')
        style_strings = style_string.split(' ')

        if style_strings[0].startswith('https://'):
            return style_strings[0]

    return None

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

    def smart_swipe(self):
        driver = self.driver

        parent_xpath = '//*[@id="t-1801132545"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/span[1]'
        candidate_xpath = '//*[@id="t-1801132545"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/span[1]/div'

        while True:
            WebDriverWait(driver, 200).until(
                EC.visibility_of_element_located((By.XPATH, parent_xpath))
            )

            WebDriverWait(driver, 200).until(
                EC.visibility_of_element_located((By.XPATH, candidate_xpath))
            )

            # Get parent span
            parent_span = driver.find_element_by_xpath(parent_xpath)

            # Get candidate element
            candidate_element = parent_span.find_element_by_xpath(candidate_xpath)
            self.rate_candidate(candidate_element)


    def rate_candidate(self, candidate_element):
        driver = self.driver

        candidate_name = candidate_element.get_attribute('aria-label')

        # Read candidate inline style
        candidate_inline_style = candidate_element.get_attribute('style')

        candidate_image_url = parse_img_url_from_inline_style(candidate_inline_style)

        # Download image
        response = requests.get(candidate_image_url, stream=True)

        candidate_img_filename = f"{candidate_name.replace(' ','_').lower()}.webp"

        with open(f'images/{candidate_img_filename}', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

        img_filename, prediction = predict_from_img_path(img_filename=candidate_img_filename)

        print(f"\n\n[*] Puntuacion de {candidate_name}: {prediction}")

        if prediction > 2.9:
            # Like
            print("[+++] LIKE <3 ")
            driver.find_element_by_xpath('//*[@id="t-1801132545"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button').click()
            sleep(random_delay())

        else:
            # Nope
            print("[----] NOPEEEE D:")
            driver.find_element_by_xpath('//*[@id="t-1801132545"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button').click()
            sleep(random_delay())