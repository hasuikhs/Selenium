import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class Crawler:

    def __init__(self, chrome_driver_path, wait_time):
        self._options = webdriver.ChromeOptions()
        self._options.add_argument('--headless')
        self._options.add_argument('--no-sandbox')
        self._options.add_argument('--disabled-gpu')
        self._options.add_argument('--disabled-dev-shm-usage')
        self._options.add_argument('--disable-usb-devices')
        self._options.add_experimental_option('prefs', {
            'download.default_directory': './',
            'download.prompt_for_download': False,
            'directory_upgrade': True,
            'safebrowsing.enabled': True
        })
        self._driver = webdriver.Chrome(
            executable_path=chrome_driver_path, chrome_options=self._options)
        self._driver.maximize_window()

        self._driver_path = chrome_driver_path
        self._time = wait_time

    def __enter__(self):
        self._driver = webdriver.Chrome(self._driver_path, chrome_options=self._options)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._driver.quit()

    def move_site(self, site_url):
        return self._driver.get(site_url)

    def submit_arrow_right(self):
        self.find_clickable('body').send_keys(Keys.ARROW_RIGHT)

    def hover_element(self, selector):
        el = self.get_located_element(selector)
        a = ActionChains(self._driver)
        a.move_to_element(el).perform()

    def submit_input(self, selector, keyword):
        self.find_clickable(selector).send_keys(keyword)
        self.find_clickable(selector).send_keys(Keys.RETURN)

    def login(self, id_selector, pw_selector, user_id, user_pw):
        self.find_clickable(id_selector).send_keys(user_id)
        self.submit_input(pw_selector, user_pw)

    def get_located_element(self, selector):
        WebDriverWait(self._driver, self._time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        return self._driver.find_element(By.CSS_SELECTOR, selector)

    def get_parent_element(self, element):
        return element.find_element(By.XPATH, '..')

    def get_elements(self, selector):
        return self._driver.find_elements(By.CSS_SELECTOR, selector)

    def find_clickable(self, selector):
        element = WebDriverWait(self._driver, self._time).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )
        return element

    def find_clickable_and_click(self, selector):
        element = WebDriverWait(self._driver, self._time).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )
        self._driver.execute_script("arguments[0].click();", element)

    def wait_implicit_time(self):
        self._driver.implicitly_wait(self._time)

    def get_page_source(self):
        return self._driver.page_source

    def remove_download_file(self, file_name):
        if os.path.isfile(file_name):
            os.remove(file_name)
        else:
            print('Not exist file: ' + file_name)

    def get_current_url(self):
        return self._driver.current_url