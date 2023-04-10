import os, time, datetime as dt
from module import Crawler
from dotenv import load_dotenv
import pandas as pd
from util import transform_str_to_int, print_progress

load_dotenv()

WAIT_TIME_SEC = 60

## 1. input keyword
SEARCH_KEYWORD = input('검색할 키워드 입력: ')
MAX_ID_COUNT = int(input('총 아이디 개수 입력: '))
MIN_FOLLOWER_COUNT = int(input('팔로우수 하한선 입력: '))

## 2. 폴더 생성 및 기존 파일 읽기
dir_path = os.getcwd() + '/results/'
os.makedirs(dir_path, exist_ok=True)

file_list = os.listdir(dir_path)
csv_file_list = [file for file in file_list if file.endswith('.csv')]

result_df = pd.concat([pd.read_csv(dir_path + file) for file in os.listdir(dir_path) if file.endswith('.csv')])

id_set_list = set(result_df['id'])
## 3. open browser
target = Crawler('./chromedriver', WAIT_TIME_SEC)

TARGET_URL = 'https://www.instagram.com/'
target.move_site(TARGET_URL)

## 4. login
USER_ID = os.getenv('USER_ID')
USER_PASSWORD = os.getenv('USER_PASSWORD')

LOGIN_ID_SELECTOR = '#loginForm > div > div:nth-child(1) > div > label > input'
LOGIN_PW_SELECTOR = '#loginForm > div > div:nth-child(2) > div > label > input'

target.login(LOGIN_ID_SELECTOR, LOGIN_PW_SELECTOR, USER_ID, USER_PASSWORD)

## 5. search
time.sleep(5)
HASHTAG_SEARCH_URL = f'https://www.instagram.com/explore/tags/{ SEARCH_KEYWORD }/'
target.move_site(HASHTAG_SEARCH_URL)

## 6. open board
time.sleep(5)
FIRST_POST_SELECTOR = 'article > div > div > div > div > div > a'
target.find_clickable(FIRST_POST_SELECTOR).click()

### 6.1 create dataframe
result_df = pd.DataFrame({
  'num': [],
  'id': [],
  'link': [],
  'follwers': []
})

USER_ID_SELECTOR = 'article header div:nth-child(2) > div > div span a'
FOLLOWER_COUNT_SELECTOR = 'span[style="line-height: 18px;"]'

new_id_set_list = set(result_df['id'])
### 7.searching...
main_index = 0
index = 0
try:
  while len(new_id_set_list) < MAX_ID_COUNT:
    time.sleep(1)
    id = target.get_located_element(USER_ID_SELECTOR).text
    target.hover_element(USER_ID_SELECTOR)
    time.sleep(4)
    
    try:
      follower = transform_str_to_int(target.get_elements(FOLLOWER_COUNT_SELECTOR)[4].text)
    except:
      follower = transform_str_to_int(target.get_elements(FOLLOWER_COUNT_SELECTOR)[5].text)

    if follower >= MIN_FOLLOWER_COUNT and id not in id_set_list and id not in new_id_set_list and 'official' not in id:
      new_id_set_list.add(id)
      index = index + 1
      result_df.loc[len(result_df)] = [index, id, f'https://www.instagram.com/{ id }', follower]

    main_index = main_index + 1

    print_progress(index, MAX_ID_COUNT, main_index, 'Progress:', 'Complete', 1, 50)
    target.submit_arrow_right()

### 7.1 도중 오류 발생해도 파일 생성
finally:
  now = dt.datetime.now().strftime('%Y-%m-%d_%H%M')
  result_df.to_csv(f'results/result_{ SEARCH_KEYWORD }_{ now }.csv', index=False)
  target.quit_driver()