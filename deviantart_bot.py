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


class DeviantartBot():

    def __init__(self):
        self.LOGIN_URL = 'https://www.deviantart.com/users/login'

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

    def checker(self, email: str, proxy: str) -> Optional[bool]:
        status = None
        try:
            browser = self._get_browser(proxy)
            # browser.get('https://api64.ipify.org?format=json')
            browser.get(self.LOGIN_URL)
            username_el = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, '//input[@id="username"]')))
            username_el.send_keys(email)
            next_button_el = WebDriverWait(browser, self.SHORT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@id="loginbutton"]')))
            next_button_el.click()

            try:
                WebDriverWait(browser, self.SHORT_TIMEOUT).until(
                    EC.visibility_of_element_located((By.XPATH, '//span[@id="username-error"]/span[contains(., "Couldn\'t find that username. Check the spelling and try again.")]')))
                status = False
            except:
                status = True
        except Exception as e:
            error = str(e)
            pass
        logger.info(f'{email} => {status}')
        return status


format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{message}</level>"
logger.configure(
    handlers=[{"sink": sys.stdout, "format": format, 'level': "INFO"}])


proxy = '0iyLsMBhVIRtEBuqLoSS:RNW78Fm5@185.162.130.86:10000'
email = 'gangabass@gmail.com'

if __name__ == '__main__':
    parser = DeviantartBot()
    is_registered = parser.checker(email, proxy)

# Домен: deviantart.com
# Метод проверки который мы обнаружили: При входе, если пользователь не зарегистрирован выдает "Couldn't find that username"
# Скрин: http://icecream.me/05c797c76ef136a6bf1a94851cf88c56
