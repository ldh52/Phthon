from time import sleep

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


# 웹 드라이버 설정
driver = webdriver.Chrome()
driver.implicitly_wait(3)

driver.get('https://workey.codeit.kr/costagram/index')
sleep(1)


# 로그인
driver.find_element(by=By.CSS_SELECTOR, value='.top-nav__login-link').click()
sleep(1)

driver.find_element(by=By.CSS_SELECTOR, value='.login-container__login-input').send_keys('codeit')
driver.find_element(by=By.CSS_SELECTOR, value='.login-container__password-input').send_keys('datascience')

driver.find_element(by=By.CSS_SELECTOR, value='.login-container__login-button').click()
sleep(1)


# 페이지 끝까지 스크롤
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(0.5)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


# 모든 썸네일 요소 가져오기
posts = driver.find_elements(by=By.CSS_SELECTOR, value='.post-list__post')

image_urls = []

for post in posts:
    # 썸네일 클릭
    post.click()
    sleep(0.5)

    # 이미지 주소 가져오기
    style_attr = driver.find_element(by=By.CSS_SELECTOR, value='.post-container__image').get_attribute('style')
    image_path = style_attr.split('"')[1]
    image_url = 'https://workey.codeit.kr' + image_path
    image_urls.append(image_url)

    # 닫기 버튼 클릭
    driver.find_element(by=By.CSS_SELECTOR, value='.close-btn').click()
    sleep(0.5)

driver.quit()


# 이미지 다운로드하기
for i in range(len(image_urls)):
    image_url = image_urls[i]
    response = requests.get(image_url)
    filename = 'image{}.jpg'.format(i)
    with open(filename, 'wb+') as f:
        f.write(response.content)
