from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import os.path
import shutil
import requests
import hashlib
import time

options = Options()
options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)

driver.get('https://ameblo.jp/juicejuice-official/imagelist-201905.html')

html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

dl_image_path = 'dl_images'

if not os.path.exists(dl_image_path):
    os.mkdir(dl_image_path)

imgs = soup.find_all("img", attrs={"class": "imgItem"})
for elm in imgs:
    print(elm['src'])
    src = elm['src']
    filename = hashlib.sha256(src.encode()).hexdigest()
    resp = requests.get(src, stream=True)
    with open(dl_image_path + '/' + filename + '.jpg', 'ab') as fp:
        shutil.copyfileobj(resp.raw, fp)
    time.sleep(1)

driver.quit()