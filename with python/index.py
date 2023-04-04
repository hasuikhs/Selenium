import os, time, datetime as dt
from module import Crawler
from dotenv import load_dotenv
import pandas as pd
from util import transform_str_to_int, print_progress

load_dotenv()

WAIT_TIME = 60

## 1. input keyword
INPUT_KEYWORD = input('검색할 키워드 입력: ')
LIMIT_CNT = int(input('총 아이디 개수 입력: '))
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

main_index = 0
index = 0
try:
  while len(id_set) < LIMIT_CNT:
    time.sleep(0.5)
    id = target.get_located_element(TEXT_ELEMENT).text
    target.hover_element(TEXT_ELEMENT)
    time.sleep(2)
    
    try:
      follower = transform_str_to_int(target.get_elements(FOLLOW_ELEMNT)[4].text)
    except:
      follower = transform_str_to_int(target.get_elements(FOLLOW_ELEMNT)[5].text)

    if follower >= LIMIT_FOLLOWER and id not in id_set:
      id_set.add(id)
      index = index + 1
      df.loc[len(df)] = [index, id, follower, f'https://www.instagram.com/{ id }']

    main_index = main_index + 1

    print_progress(index, LIMIT_CNT, main_index, 'Progress:', 'Complete', 1, 50)
    target.submit_arrow_right()

finally:
  now = dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
  df.to_csv(f'result_{ now }.csv')

target.quit_driver()