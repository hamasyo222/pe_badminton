# -*- coding: utf-8 -*-
import requests
import datetime
import pickle
import os.path
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome import service as fs
import traceback
import sys


keio_id = os.environ["KEIO_ID"]
keio_pass = os.environ["KEIO_PASS"]
line_token = os.environ["TOKEN"]

def reserve():  
    # 操作する
    #
    # Seleniumをあらゆる環境で起動させるオプション
    #
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--proxy-server="direct://"')
    options.add_argument('--proxy-bypass-list=*')
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless') # ※ヘッドレスモードを使用する場合、コメントアウトを外す
    options.binary_location = os.getcwd() + "/bin/headless-chromium"
    

    #
    # Chromeドライバーの起動
    #
    print("ドライバー起動")

    driver = webdriver.Chrome(os.getcwd() + "/bin/chromedriver", options=options)
    #driver = webdriver.Chrome()
    driver.implicitly_wait(20)

    #施設予約システムにアクセス
    driver.get("https://wellness.sfc.keio.ac.jp/v3/")

    #keio.jp認証
    #ID
    driver.find_element(By.CSS_SELECTOR,'#maincontents > form > div > table > tbody > tr:nth-child(1) > td > input').send_keys(keio_id)#

    #パスワード
    driver.find_element(By.CSS_SELECTOR,'#maincontents > form > div > table > tbody > tr:nth-child(2) > td > input').send_keys(keio_pass)#

    #ログイン
    driver.find_element(By.CSS_SELECTOR,'#maincontents > form > div > table > tbody > tr:nth-child(3) > td:nth-child(2) > input[type=submit]').click()

    #メニュー→予約
    driver.find_element(By.CSS_SELECTOR,'#navbar > div > a:nth-child(2)').click()
    
    #バドミントン探す
    i = 1
    while True:
        event =  driver.find_element(By.CSS_SELECTOR,f'#maincontents > div:nth-child(9) > table > tbody > tr:nth-child({i}) > td:nth-child(3)').text
        print(event)
        if event == "バドミントン":
            try:
                driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR,f'#maincontents > div:nth-child(9) > table > tbody > tr:nth-child({i}) > td:nth-child(13) > a'))
                driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR,'#maincontents > form > p > input.w3-btn.w3-small.w3-padding-small.w3-round-large.w3-pale-green.w3-border'))
                driver.find_element(By.CSS_SELECTOR,'#navbar > div > a:nth-child(2)').click()
            except Exception as e:
                driver.find_element(By.CSS_SELECTOR,'#navbar > div > a:nth-child(2)').click()
            else:
                send_line("予約できた")
            
        i += 1


#ライン送る
def send_line(message):
    url = "https://notify-api.line.me/api/notify"
    headers = {'Authorization': 'Bearer ' + line_token}
    
    message = message
    data = {
        "message": message
    }

    requests.post(
        "https://notify-api.line.me/api/notify",
        headers=headers,
        data=data,
    )



if __name__ == '__main__':
    reserve()