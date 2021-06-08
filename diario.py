from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import shutil
import time
 
def getCoverUrl(url):
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_prefs = {}
  chrome_options.experimental_options["prefs"] = chrome_prefs
  chrome_prefs["profile.default_content_settings"] = {"images": 2}
  browser = webdriver.Chrome(options=chrome_options)
  browser.get(url)
  html = browser.page_source
  soup = BeautifulSoup(html, 'lxml')
  coverElementArray = soup.find_all("figure", {"class": "t-s13-pic"})
  if len(coverElementArray) > 0:
    coverElement = coverElementArray[0]
    coverImg = coverElement.find('img')
    coverUrl = coverImg.get('data-src')
    return coverUrl
  else:
    return None

  
def getCover(date):
  year = date.strftime("%Y")
  path = f'Diario/{year}'
  Path(path).mkdir(parents=True, exist_ok=True)
  url = f'https://www.dn.pt/edicao-do-dia/{date.strftime("%Y-%m-%d")}.html'
  coverUrl = getCoverUrl(url)
  if coverUrl != None:
    imgCoverContent = requests.get(coverUrl, stream = True)
    extension = imgCoverContent.headers['content-type'].split("/")[-1]
    coverFileName = f'{path}/D_{date.strftime("%Y_%m_%d")}.{extension}'
    if imgCoverContent.status_code == 200:
      imgCoverContent.raw.decode_content = True 
      with open(coverFileName,'wb') as f:
        shutil.copyfileobj(imgCoverContent.raw, f)
        print(f'done: {date}')
    else:
        print(f'error downloading url: {url}')
  else:
    print(f'error to get url: {url}')


periods = ["2020-11-15/2020-12-15"]
for period in periods:
    periodArray = period.split('/')
    start = datetime.fromisoformat(periodArray[0])
    end = datetime.fromisoformat(periodArray[1])
    current = start
    while current <= end:
      getCover(current)
      time.sleep(3)
      current += timedelta(days=1)





