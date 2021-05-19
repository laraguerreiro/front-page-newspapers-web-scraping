from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path
import requests
import shutil
import time
 
def getCoverUrl(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'lxml')
  coverElementPrincipal = soup.find_all("ul", {"class": "print-covers__list"})[0]
  coverElement = coverElementPrincipal.find(id="publico-lisboa")
  if(coverElement == None):
    coverElement = coverElementPrincipal.find(id="publico")
  coverImg = coverElement.find('img')
  coverUrl = coverImg.get('data-media-viewer')
  return coverUrl
  
def getCover(date):
  year = date.strftime("%Y")
  path = f'Publico/{year}'
  Path(path).mkdir(parents=True, exist_ok=True)
  url = f'https://www.publico.pt/jornal?date={date.strftime("%Y%m%d")}'
  coverUrl = getCoverUrl(url) 
  extension = coverUrl.split(".")[-1][0:3]
  coverFileName = f'{path}/P_{date.strftime("%Y_%m_%d")}.{extension}'
  imgCoverContent = requests.get(coverUrl, stream = True)
  if imgCoverContent.status_code == 200:
    imgCoverContent.raw.decode_content = True 
    with open(coverFileName,'wb') as f:
      shutil.copyfileobj(imgCoverContent.raw, f)
      print(f'done: {date}')
  else:
      print(f'error in url: {url}')


periods = ["2017-10-15/2017-11-15", "2018-10-15/2018-11-15", "2019-10-15/2019-11-15", "2020-10-15/2020-11-15"]
for period in periods:
    periodArray = period.split('/')
    start = datetime.fromisoformat(periodArray[0])
    end = datetime.fromisoformat(periodArray[1])
    current = start
    while current <= end:
      getCover(current)
      time.sleep(3)
      current += timedelta(days=1)





