import os, time, logging, datetime as dt, time
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

### 1.1 로그 파일 이름과 경로 설정
dir_path = os.getcwd() + '/results/'
log_filename = 'error.log'

log_format = '%(asctime)s - %(levelname)s - %(message)s'
log_level = logging.ERROR

logger = logging.getLogger(__name__)
logger.setLevel(log_level)

file_handler = logging.FileHandler(filename=dir_path + '/../error.log')
file_handler.setLevel(log_level)
file_handler.setFormatter(logging.Formatter(log_format))

logger.addHandler(file_handler)

## 2. 폴더 생성 및 기존 파일 읽기
os.makedirs(dir_path, exist_ok=True)

csv_file_list = [file for file in os.listdir(dir_path) if file.endswith('.csv')]

if not csv_file_list:
  result_df = pd.DataFrame(columns=['num', 'id', 'link', 'follwers'])
else:
  result_df = pd.concat([pd.read_csv(os.path.join(dir_path, file), encoding_errors='ignore') for file in csv_file_list])

origin_id_set_list = set(result_df['id'])

id_set_list = set([])

for id in origin_id_set_list:
  if pd.isna(id):
    continue
  else:
    if 'instagram.com' in str(id):
      id = id.split('instagram.com/')[1].split('/')[0].split('?')[0]
    id_set_list.add(id)

start_time = time.time()

## 3. open browser
with Crawler('./chromedriver', WAIT_TIME_SEC) as target:
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
    'followers': []
  })

  USER_ID_SELECTOR = 'article header div:nth-child(2) > div > div span a'
  FOLLOWER_COUNT_SELECTOR = 'span[style="line-height: 18px;"]'

  new_id_set_list = set(result_df['id'])
  ### 7.searching...
  main_index = 0
  index = 0
  try:
    while len(new_id_set_list) < MAX_ID_COUNT:
      time.sleep(3)
      id = target.get_located_element(USER_ID_SELECTOR).text
      target.hover_element(USER_ID_SELECTOR)
      time.sleep(4)

      hover_element = target.get_elements(FOLLOWER_COUNT_SELECTOR)
      target_index = 4
      for element_index, element in enumerate(hover_element):
        if element.text in ['followers', '팔로워'] and element_index > 3:
          target_index = element_index - 1

      try:
        follower = transform_str_to_int(hover_element[target_index].text)
      except Exception as e:
        logger.error(str(e))

      if follower >= MIN_FOLLOWER_COUNT and id not in id_set_list and id not in new_id_set_list and 'official' not in id:
        new_id_set_list.add(id)
        index = index + 1
        result_df.loc[len(result_df)] = [index, id, f'https://www.instagram.com/{ id }/', follower]

      main_index = main_index + 1

      print_progress(index, MAX_ID_COUNT, start_time, main_index, 'Progress:', 'Complete', 1, 50)
      target.submit_arrow_right()

  ### 7.1 도중 오류 발생해도 파일 생성
  finally:
    now = dt.datetime.now().strftime('%Y-%m-%d_%H%M')
    result_df.to_csv(dir_path + f'result_{ SEARCH_KEYWORD }_{ now }.csv', index=False)

print('Process  End!')