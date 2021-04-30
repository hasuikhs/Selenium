from module import Crawler

wait_time = 60

target = Crawler('../chromedriver') # 해당 위치에 chromedriver 다운로드

target_url = 'https://sample.com'
target.move_site(target_url)