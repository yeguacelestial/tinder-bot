import os
import random
from time import sleep

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from use_model import predict_from_img_path, predict_from_url_path

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

        # Get elements IDs
        self.main_div_id = driver.find_element_by_xpath('//body/div[1]').get_attribute('id')
        self.alert_div_id = driver.find_element_by_xpath('//body/div[2]').get_attribute('id')

        # Accept terms
        driver.find_element_by_xpath(f'//*[@id="{self.main_div_id}"]/div/div[2]/div/div/div[1]').click()
        sleep(random_delay())

        # Login button
        driver.find_element_by_xpath(f'//*[@id="{self.main_div_id}"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a').click()
        sleep(random_delay())

        # Login with phone number
        driver.find_element_by_xpath(f'//*[@id="{self.alert_div_id}"]/div/div/div[1]/div/div[3]/span/div[2]/button').click()
        sleep(random_delay())

        # Try to wait for captcha modal to appear...
        try:
            WebDriverWait(driver, 200).until(
                EC.invisibility_of_element_located((By.ID, "arkoseInlineAnchor"))
            )
        except:
            pass
        
        # Introduce phone number
        driver.find_element_by_xpath(f'//*[@id="{self.alert_div_id}"]/div/div/div[1]/div[2]/div/input').send_keys(os.getenv('PHONE_NUMBER'))
        sleep(random_delay())

        # Button "Continue"
        driver.find_element_by_xpath(f'//*[@id="{self.alert_div_id}"]/div/div/div[1]/button/span').click()
        sleep(random_delay())

        # Ask for phone code
        sms_code = input("[*********] SMS Code -> ")

        # SMS code inputs on each case
        for i in range(0,6):
            driver.find_element_by_xpath(f'//*[@id="{self.alert_div_id}"]/div/div/div[1]/div[3]/input[{i+1}]').send_keys(sms_code[i])

        sleep(random_delay())

        # Continue button
        driver.find_element_by_xpath(f'//*[@id="{self.alert_div_id}"]/div/div/div[1]/button').click()
        sleep(random_delay())

        # Email code handling
        email_code = input("[**********] Email code -> ")

        for i in range(0,6):
            driver.find_element_by_xpath(f'//*[@id="{self.alert_div_id}"]/div/div/div[1]/div[3]/input[{i+1}]').send_keys(email_code[i])
        
        sleep(random_delay())

        # Next button
        driver.find_element_by_xpath(f'//*[@id="{self.alert_div_id}"]/div/div/div[1]/button').click()
        sleep(random_delay())

        # Try to accept notifications and stuff
        try:
            driver.find_element_by_xpath(f'//*[@id="{self.alert_div_id}"]/div/div/div/div/div[3]/button[1]').click()
            sleep(random_delay())
            
            driver.find_element_by_xpath(f'//*[@id="{self.alert_div_id}"]/div/div/div/div/div[3]/button[2]').click()
            sleep(random_delay())

        except:
            pass

    def smart_swipe(self):
        driver = self.driver

        parent_xpath = f'//*[@id="{self.main_div_id}"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/span[1]'
        candidate_xpath = f'//*[@id="{self.main_div_id}"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/span[1]/div'

        while True:
            WebDriverWait(driver, 200).until(
                EC.visibility_of_element_located((By.XPATH, parent_xpath))
            )

            WebDriverWait(driver, 200).until(
                EC.visibility_of_element_located((By.XPATH, candidate_xpath))
            )

            self.handle_alerts()

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

        prediction = predict_from_url_path(URL=candidate_image_url)

        print(f"\n\n[*] Puntuacion de {candidate_name}: {prediction}")

        if prediction > 2.9:
            # Like
            print("[<3] LIKE ")
            driver.find_element_by_xpath(f'//*[@id="{self.main_div_id}"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button').click()
            sleep(random_delay())

        else:
            # Nope
            print("[D:] NOPE")
            driver.find_element_by_xpath(f'//*[@id="{self.main_div_id}"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button').click()
            sleep(random_delay())

    def handle_alerts(self):
        driver = self.driver

        # Tinder Passport alert - No thanks
        passport_alert_nothanks_xpath = f'//*[@id="{self.alert_div_id}"]/div/div/div[1]/button/span'
        
        # UPGRADE YOUR LIKE - You just liked a popular profile...'No thanks' button
        upgrade_like_nothanks_xpath = '/html/body/div[2]/div/div/button[2]'

        if self.element_exists_by_xpath(passport_alert_nothanks_xpath):
            driver.find_element_by_xpath(passport_alert_nothanks_xpath).click()
            sleep(random_delay())

        elif self.element_exists_by_xpath(upgrade_like_nothanks_xpath):
            driver.find_element_by_xpath(upgrade_like_nothanks_xpath).click()
            sleep(random_delay())

        else:
            pass

    def element_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False

        return True
