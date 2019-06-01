from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import os.path
import shutil
import requests
import hashlib
import time
import sys

options = Options()
options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

year = 2019
month = 5
i = 60 # 5年分
while i > 0:
    url = 'https://ameblo.jp/juicejuice-official/imagelist-' + str(year) + str(month).rjust(2, "0") + '.html'
    print('Link: ' + url)
    driver.get(url)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    dl_image_path = 'dl_images'

    if not os.path.exists(dl_image_path):
        os.mkdir(dl_image_path)

    imgs = soup.find_all("img", attrs={"class": "imgItem"})
    for j, elm in enumerate(imgs):
        sys.stdout.write('\r')
        sys.stdout.write('%-20s' % ('.' * j))
        sys.stdout.flush()
        src = elm['src']
        filename = hashlib.sha256(src.encode()).hexdigest()
        resp = requests.get(src, stream=True)
        with open(dl_image_path + '/' + filename + '.jpg', 'ab') as fp:
            shutil.copyfileobj(resp.raw, fp)
        time.sleep(1)
    sys.stdout.write('\n')

    month -= 1
    i -= 1
    if month == 0:
        year -= 1
        month = 12

driver.quit()
