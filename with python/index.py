import os, time
from module import Crawler
from dotenv import load_dotenv

load_dotenv()

wait_time = 60

target = Crawler('./chromedriver') # 해당 위치에 chromedriver 다운로드

target_url = 'https://www.instagram.com/'
target.move_site(target_url)

LOGIN_ID = os.getenv('USER_ID')
LOGIN_PW = os.getenv('USER_PASSWORD')

print(LOGIN_ID)
print(LOGIN_PW)

target.login('#loginForm > div > div:nth-child(1) > div > label > input', '#loginForm > div > div:nth-child(2) > div > label > input', LOGIN_ID, LOGIN_PW)

time.sleep(10)