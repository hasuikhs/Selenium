import os, time
from module import Crawler
from dotenv import load_dotenv
import pandas as pd
from util import transform_str_to_int

load_dotenv()

WAIT_TIME = 60

## 1. input keyword
INPUT_KEYWORD = input('검색할 키워드 입력: ')
LIMIT_CNT = input('총 아이디 개수 입력: ')
LIMIT_FOLLOWER = int(input('팔로우수 하한선 입력: '))

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
SEARCH_URL = f'https://www.instagram.com/explore/tags/{ INPUT_KEYWORD }/'
target.move_site(SEARCH_URL)

## 5. open board
time.sleep(5)
FIRST_TARGET = 'article > div > div > div > div > div > a'
target.find_clickable(FIRST_TARGET).click()

### 5.1 create dataframe
df = pd.DataFrame({
  '번호': [],
  'id': [],
  '팔로우': [],
  'link': [],
})

TEXT_ELEMENT = 'article header div:nth-child(2) > div > div span a'
FOLLOW_ELEMNT = 'span[style="line-height: 18px;"]'

id_set = set([])

main_index = 1
index = 1
try:
  while len(id_set) < int(LIMIT_CNT):
    time.sleep(0.3)
    id = target.get_located_element(TEXT_ELEMENT).text
    target.hover_element(TEXT_ELEMENT)
    time.sleep(1.5)
    
    try:
      follower = transform_str_to_int(target.get_elements(FOLLOW_ELEMNT)[4].text)
    except:
      follower = transform_str_to_int(target.get_elements(FOLLOW_ELEMNT)[5].text)

    print(follower, LIMIT_FOLLOWER)
    if follower >= LIMIT_FOLLOWER:
      id_set.add(id)
      df.loc[len(df)] = [index, id, follower, f'https://www.instagram.com/{ id }']
      index = index + 1

    main_index = main_index + 1

    print(f'총 시도: { main_index }, 현재 들어간 횟수: { index }')
    target.submit_arrow_right()

finally:
  df.to_csv('result.csv')

target.quit_driver()