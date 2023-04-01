import os, time
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

    def login(self, id_selector, pw_selector, user_id, user_pw, wait_time):
        self.find_clickable(id_selector, wait_time).send_keys(user_id)
        self.find_clickable(pw_selector, wait_time).send_keys(user_pw)
        self.find_clickable(pw_selector, wait_time).send_keys(Keys.RETURN)

    def get_element_with_explicit_wait_millis(self, selector, explicit_wait_second):
        WebDriverWait(self._driver, explicit_wait_second).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        return self._driver.find_element(By.CSS_SELECTOR, selector)

    def find_clickable(self, selector, explicit_wait_second):
        element = WebDriverWait(self._driver, explicit_wait_second).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )
        return element

    def find_clickable_and_click(self, selector, explicit_wait_second):
        element = WebDriverWait(self._driver, explicit_wait_second).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
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
