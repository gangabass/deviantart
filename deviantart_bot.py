from typing import Optional
import sys
from seleniumbase import Driver
from loguru import logger
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from random_username.generate import generate_username
from password_generator import PasswordGenerator
import random
import time


class DeviantartBot():

    def __init__(self):
        self.REGISTRATION_URL = 'https://www.deviantart.com/join'

        self.WAIT_TIMEOUT = 30
        self.SHORT_TIMEOUT = 3
        pass

    def _get_browser(self, proxy):
        browser = Driver(
            uc=True,
            undetectable=True,
            headless=True,
            proxy=proxy
        )

        return browser

    def _generate_random_username(self):
        return generate_username(1)

    def _generate_random_password(self):
        pwo = PasswordGenerator()
        password = pwo.generate()
        return password

    def checker(self, email: str, proxy: str) -> Optional[bool]:
        status = None
        try:
            browser = self._get_browser(proxy)
            self.browser = browser
            # browser.get('https://api64.ipify.org?format=json')
            browser.get(self.REGISTRATION_URL)
            username_el = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, '//input[@id="email"]')))
            username_el.send_keys(email)

            password = self._generate_random_password()
            password_el = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, '//input[@id="password"]')))
            password_el.send_keys(password)

            next_button_el = WebDriverWait(browser, self.SHORT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, '//button[span[.="Continue with Email"]]')))
            next_button_el.click()

            username = self._generate_random_username()
            username += self._generate_random_username()
            username_el = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, '//input[@id="username"]')))
            username_el.send_keys(username)

            
            random_date = self._generate_random_date()
            dob_year, dob_month, dob_day = random_date.split('-')
            self._process_dropdown('//input[@name="dobMonth"]/following-sibling::div[1]//select', str(int(dob_month)))
            self._process_dropdown('//input[@name="dobDay"]/following-sibling::div[1]//select', str(int(dob_day)))
            self._process_dropdown('//input[@name="dobYear"]/following-sibling::div[1]//select', dob_year)

            join_button = WebDriverWait(browser, self.SHORT_TIMEOUT).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[span[.="Join"]]')))
            join_button.click()

            try:
                WebDriverWait(browser, self.SHORT_TIMEOUT).until(
                    EC.visibility_of_element_located((By.XPATH, '//span[@id="email-error"][contains(., "That email address is already in use")]')))
                status = True
            except:
                status = False
        except Exception as e:
            error = str(e)
            pass
        logger.info(f'{email} => {status}')
        return status

    def _process_dropdown(self, selector, value):
        el = WebDriverWait(self.browser, self.SHORT_TIMEOUT).until(
                EC.visibility_of_element_located((By.XPATH, selector)))
        select = Select(el)
        select.select_by_value(value)

    def _generate_random_date(self):
            return self.random_date("1990-01-01", "2004-12-31", random.random())
    
    def str_time_prop(self, start, end, time_format, prop):
        """Get a time at a proportion of a range of two formatted times.

        start and end should be strings specifying times formatted in the
        given format (strftime-style), giving an interval [start, end].
        prop specifies how a proportion of the interval to be taken after
        start.  The returned time will be in the specified format.
        """

        stime = time.mktime(time.strptime(start, time_format))
        etime = time.mktime(time.strptime(end, time_format))

        ptime = stime + prop * (etime - stime)

        return time.strftime(time_format, time.localtime(ptime))


    def random_date(self, start, end, prop):
        return self.str_time_prop(start, end, '%Y-%m-%d', prop)


format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{message}</level>"
logger.configure(
    handlers=[{"sink": sys.stdout, "format": format, 'level': "INFO"}])


proxy = '0iyLsMBhVIRtEBuqLoSS:RNW78Fm5@185.162.130.86:10000'
email = 'gangabass@gmail.com'
email = 'rush2cash.course@gmail.com'

if __name__ == '__main__':
    parser = DeviantartBot()
    is_registered = parser.checker(email, proxy)

# Домен: deviantart.com
# Метод проверки который мы обнаружили: При входе, если пользователь не зарегистрирован выдает "Couldn't find that username"
# Скрин: http://icecream.me/05c797c76ef136a6bf1a94851cf88c56
