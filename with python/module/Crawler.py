import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Crawler:

    def __init__(self, chrome_driver_path):
        self._options = webdriver.ChromeOptions()
        # self._options.add_argument('--headless')
        self._options.add_argument('--no-sandbox')
        self._options.add_argument('--disabled-gpu')
        self._options.add_argument('--disabled-dev-shm-usage')
        self._options.add_experimental_option('prefs', {
            'download.default_directory': './',
            'download.prompt_for_download': False,
            'directory_upgrade': True,
            'safebrowsing.enabled': True
        })
        self._driver = webdriver.Chrome(
            executable_path=chrome_driver_path, chrome_options=self._options)
        self._driver.maximize_window()

    def move_site(self, site_url):
        return self._driver.get(site_url)

    def login(self, id_xpath, pw_xpath, user_id, user_pw):
        self._driver.find_element_by_xpath(id_xpath).send_keys(user_id)
        self._driver.find_element_by_xpath(pw_xpath).send_keys(user_pw)
        self._driver.find_element_by_xpath(pw_xpath).send_keys(Keys.RETURN)

    def get_element_by_xpath_with_explicit_wait_millis(self, xpath, explicit_wait_second):
        WebDriverWait(self._driver, explicit_wait_second).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        return self._driver.find_element_by_xpath(xpath)

    def get_clickableElement_by_xpath_with_explicit_wait_millis(self, xpath, explicit_wait_second):
        WebDriverWait(self._driver, explicit_wait_second).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        return self._driver.find_element_by_xpath(xpath)

    def check_clickable_and_click_element(self, xpath, wait_time):
        WebDriverWait(self._driver, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, xpath))).send_keys(Keys.ENTER)

    def find_clickable(self, xpath, explicit_wait_second):
        element = WebDriverWait(self._driver, explicit_wait_second).until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath))
        )
        return element

    def find_clickable_and_click(self, xpath, explicit_wait_second):
        element = WebDriverWait(self._driver, explicit_wait_second).until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath))
        )
        self._driver.execute_script("arguments[0].click();", element)


    def wait_implicit_time(self, second):
        self._driver.implicitly_wait(second)

    def get_page_source(self):
        return self._driver.page_source

    def remove_download_file(self, file_name):
        if os.path.isfile(file_name):
            os.remove(file_name)
        else:
            print('Not exist file: ' + file_name)

    def get_current_url(self):
        return self._driver.current_url

    def quit_driver(self):
        self._driver.quit()
