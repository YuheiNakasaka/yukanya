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
import json
import requests
from urllib import parse

class JJScraping:
    def __init__(self):
        # selenium
        options = Options()
        options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
        options.add_argument('--headless')
        options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')
        self.driver = webdriver.Chrome(options=options)

        # requests
        self.session = requests.session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'})

    def from_ameba_blog(self, year, month, term):
        while i > 0:
            url = 'https://ameblo.jp/juicejuice-official/imagelist-' + str(year) + str(month).rjust(2, "0") + '.html'
            print('Link: ' + url)
            self.driver.get(url)
            html = self.driver.page_source.encode('utf-8')
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
        self.driver.quit()

    def from_google(self, keyword, dirname):
        print('Start ' + keyword)
        google_search_url = 'https://www.google.co.jp/search'
        dl_image_dir = 'dl_gimages'
        if not os.path.exists(dl_image_dir):
            os.mkdir(dl_image_dir)
        member_image_dir = dl_image_dir + '/' + dirname 
        if not os.path.exists(member_image_dir):
            os.mkdir(member_image_dir)

        # linkの収集
        maximum = 500
        page = 0
        results = []
        while maximum > 0:
            print('残り ' + str(maximum))
            # fetch html
            params = parse.urlencode({ 'q': keyword, 'tbm': 'isch', 'filter': '0', 'ijn': str(page) })
            url = google_search_url + '?' + params
            html = self.session.get(url).text
            soup = BeautifulSoup(html, 'lxml')

            # get image links
            elements = soup.select('.rg_meta.notranslate')
            jsons = [json.loads(elm.get_text()) for elm in elements]
            links = [js['ou'] for js in jsons]
            if len(links) ==  0:
                print('no links')
                break
            else:
                results += links
                maximum -= len(links)
            page += 1
            time.sleep(2)
        
        # 画像のdownload
        for i, img_url in enumerate(results):
            if i % 50 == 0: time.sleep(5)
            try:
                req = requests.get(img_url, allow_redirects=False)
                with open(member_image_dir + '/' + str(i) + '.jpg', 'wb') as f:
                    f.write(req.content)
            except requests.exceptions.ConnectionError:
                continue
            except UnicodeEncodeError:
                continue
            except UnicodeError:
                continue
            except IsADirectoryError:
                continue

if __name__ == '__main__':
    # client = JJScraping()
    # client.from_ameba_blog(2019, 5, 60)
    client = JJScraping()
    client.from_google('宮崎由加', 'yukamiyazaki')
    client.from_google('金澤朋子', 'tomokokanazawa')
    client.from_google('高木紗友希', 'sayukitakagi')
    client.from_google('段原瑠々', 'rurudanbara')
    client.from_google('稲場愛香', 'manakainaba')
    client.from_google('宮本佳林', 'karinmiyamoto')
    client.from_google('植村あかり', 'akariuemura')
