import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class Crawler:
  def __init__(self, chrome_driver_path, wait_time):
    self.chrome_options = webdriver.ChromeOptions()
    self.chrome_options.add_argument('--headless')
    self.chrome_options.add_argument('--no-sandbox')
    self.chrome_options.add_argument('--disable-gpu')
    self.chrome_options.add_argument('--disable-dev-shm-usage')
    self.chrome_options.add_argument('--disable-usb-devices')
    self.chrome_options.add_experimental_option('prefs', {
      'download.default_directory': './',
      'download.prompt_for_download': False,
      'directory_upgrade': True,
      'safebrowsing.enabled': True
    })

    self.chrome_driver_path = chrome_driver_path
    self.wait_time = wait_time

  def __enter__(self):
    self.driver = webdriver.Chrome(
      executable_path=self.chrome_driver_path, options=self.chrome_options)
    self.driver.maximize_window()
    self.driver.implicitly_wait(self.wait_time)
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    if self.driver is not None:
      self.driver.quit()

  def move_site(self, site_url: str):
    self.driver.get(site_url)

  def submit_arrow_right(self):
    self.find_clickable('body').send_keys(Keys.ARROW_RIGHT)

  def hover_element(self, selector: str):
    el = self.get_located_element(selector)
    a = ActionChains(self.driver)
    a.move_to_element(el).perform()

  def submit_input(self, selector: str, keyword: str):
    elem = self.find_clickable(selector)
    elem.send_keys(keyword)
    elem.send_keys(Keys.RETURN)

  def login(self, id_selector: str, pw_selector: str, user_id: str, user_pw: str):
    self.find_clickable(id_selector).send_keys(user_id)
    self.submit_input(pw_selector, user_pw)

  def get_located_element(self, selector: str):
    return WebDriverWait(self.driver, self.wait_time).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )

  def get_parent_element(self, element):
    return element.find_element(By.XPATH, 'parent::*')

  def get_elements(self, selector: str):
    return self.driver.find_elements(By.CSS_SELECTOR, selector)

  def find_clickable(self, selector: str):
    element = WebDriverWait(self.driver, self.wait_time).until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
    )
    return element

  def get_page_source(self) -> str:
    return self.driver.page_source

  def remove_download_file(self, file_name: str):
    if os.path.isfile(file_name):
      os.remove(file_name)
    else:
      print('Not exist file: ' + file_name)

  def get_url(self):
    return self.driver.current_url