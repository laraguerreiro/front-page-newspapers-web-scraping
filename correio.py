from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path
import requests
import shutil
import time
 
def getCoverUrl(url):
  r = requests.get(url)
  if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'lxml')
    coverElementArray = soup.find_all("a", {"class": "linkHighRes"})
    if len(coverElementArray) > 0:
      coverElement = coverElementArray[0]
      coverUrl = f'https:{coverElement.get("href")}'
      return coverUrl
    else:
      return None
  else:
    return None
  

getCoverUrl("https://www.cmjornal.pt/mais-cm/capas/detalhe/cm-de-hoje-01112020")

def getCover(date):
  year = date.strftime("%Y")
  path = f'Correio/{year}'
  Path(path).mkdir(parents=True, exist_ok=True)
  url = f'https://www.cmjornal.pt/mais-cm/capas/detalhe/cm-de-hoje-{date.strftime("%d%m%Y")}'
  coverUrl = getCoverUrl(url)
  if coverUrl != None:
    extension = coverUrl.split(".")[-1][0:3]
    coverFileName = f'{path}/C_{date.strftime("%Y_%m_%d")}.{extension}'
    pdfCoverContent = requests.get(coverUrl, stream = True)
    if pdfCoverContent.status_code == 200:
      pdfCoverContent.raw.decode_content = True 
      with open(coverFileName,'wb') as f:
        shutil.copyfileobj(pdfCoverContent.raw, f)
        print(f'done: {date}')
    else:
        print(f'error downloading url: {url}')
  else:
    print(f'error to get url: {url}')


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





