from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path
import requests
import shutil
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#estratégia: acessar o site filtrando a data específica dentro do período pesquisado. 
#no site faz a raspagem dos dados para encontrar a url da imagem que contém a capa (campo definido)
# faz o download da imagem e salva em arquivo na sua pasta específica. 

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
  coverElementPrincipal = soup.find_all("article")[0]
  coverElement = coverElementPrincipal.find("img")
  if coverElement != None:
    coverUrl = coverElement.get('data-src')
    return coverUrl
  else:
    return None


def getCover(date):
  year = date.strftime("%Y")
  path = f'Jornal/{year}'
  Path(path).mkdir(parents=True, exist_ok=True)
  url = f'https://www.jn.pt/edicao-do-dia/{date.strftime("%Y-%m-%d")}.html'
  coverUrl = getCoverUrl(url) 
  if coverUrl != None:
    imgCoverContent = requests.get(coverUrl, stream = True)
    extension = imgCoverContent.headers['content-type'].split("/")[-1]
    coverFileName = f'{path}/J_{date.strftime("%Y_%m_%d")}.{extension}'
    if imgCoverContent.status_code == 200:
      imgCoverContent.raw.decode_content = True 
      with open(coverFileName,'wb') as f:
        shutil.copyfileobj(imgCoverContent.raw, f)
        print(f'done: {date}')
    else:
        print(f'error downloading url: {url}')
  else:
    print(f'error in url: {url}')



periods = ["2019-10-15/2019-11-15", "2020-11-15/2020-12-15"]
for period in periods:
    periodArray = period.split('/')
    start = datetime.fromisoformat(periodArray[0])
    end = datetime.fromisoformat(periodArray[1])
    current = start
    while current <= end:
      getCover(current)
      time.sleep(3)
      current += timedelta(days=1)

