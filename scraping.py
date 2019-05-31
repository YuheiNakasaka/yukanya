from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

options = Options()
options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)

driver.get('https://razokulover.com/')

html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, "html.parser")

for elm in soup.find_all("a"):
    print(elm.prettify())

driver.quit()