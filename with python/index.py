import os, time
from module import Crawler
from dotenv import load_dotenv

load_dotenv()

WAIT_TIME = 60

## 1. input keyword
keyword = input()

## 2. open browser
target = Crawler('./chromedriver', WAIT_TIME)

TARGET_URL = 'https://www.instagram.com/'
target.move_site(TARGET_URL)

## 3. login
LOGIN_ID = os.getenv('USER_ID')
LOGIN_PW = os.getenv('USER_PASSWORD')

ID_SELECTOR = '#loginForm > div > div:nth-child(1) > div > label > input'
PW_SELECTOR = '#loginForm > div > div:nth-child(2) > div > label > input'

target.login(ID_SELECTOR, PW_SELECTOR, LOGIN_ID, LOGIN_PW)

## 4. search
# SEARCH_IMG = 'svg[aria-label="검색"]'
# SEARCH_INPUT = 'input[aria-label="입력 검색"]'

# el = target.get_located_element(SEARCH_IMG)
# parent = target.get_parent_element(el)
# parent.click()

# target.submit_input(SEARCH_INPUT, keyword)
time.sleep(5)
SEARCH_URL = f'https://www.instagram.com/explore/tags/{ keyword }/'
target.move_site(SEARCH_URL)

time.sleep(5)
FIRST_TARGET = 'article > div > div > div > div > div > a'
target.find_clickable(FIRST_TARGET).click()

TEXT_ELEMENT = 'article header div:nth-child(2) > div > div span a'

id_set = set([])

for i in range(1000):
  time.sleep(0.2)
  id = target.get_located_element(TEXT_ELEMENT).text
  id_set.add(id)
  print(i, id)
  target.submit_arrow_right()


print(id_set)
print(len(id_set))
### chrome wait
time.sleep(1000)