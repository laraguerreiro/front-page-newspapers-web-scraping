from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path
import requests
import shutil
import time
 
def getCoverUrl(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'lxml')
  coverImg = soup.find('img')
  if coverImg != None:
    sizesCover = coverImg.get('data-srcset')
    sizesCoverArray = sizesCover.split(",")
    coverUrl = f'https:{sizesCoverArray[-1].split(" ")[1]}'
    return coverUrl
  else:
    return None


def getCover(date):
  year = date.strftime("%Y")
  path = f'Expresso/{year}'
  Path(path).mkdir(parents=True, exist_ok=True)
  url = f'https://leitor.expresso.pt/api/v1/render/calendar/issues?date={date.strftime("%Y-%m-%d")}'
  coverUrl = getCoverUrl(url)
  if coverUrl != None:
    imgCoverContent = requests.get(coverUrl, stream = True)
    extension = imgCoverContent.headers['content-type'].split("/")[-1]
    coverFileName = f'{path}/E_{date.strftime("%Y_%m_%d")}.{extension}'
    if imgCoverContent.status_code == 200:
      imgCoverContent.raw.decode_content = True 
      with open(coverFileName,'wb') as f:
        shutil.copyfileobj(imgCoverContent.raw, f)
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





