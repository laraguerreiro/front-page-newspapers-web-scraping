from string import printable
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path
import requests
import shutil
import time
import pickle
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
load_dotenv()

# pegar a url do PDF. para tanto o código html da página foi estudado para ver onde ele estava
def getPDFUrl(url, kind, browser):
  browser.get(url)
  soup = BeautifulSoup(browser.page_source, 'lxml')
  section = soup.find("section", {"id": "print-covers", "class": "print-covers"})
  li = section.find_all("li", {"id": f'{kind}'})
  if len(li) > 0 :
    a = li[0].find_all("a")[1]
    href = a.get('href')
    return href
  else:
    return "Not Found"

# pegar o PDF a partir da url definida.
def getPDF(date, kind, browser):
  year = date.strftime("%Y")
  path = f'PublicoPDF/{kind}/{year}'
  Path(path).mkdir(parents=True, exist_ok=True)
  url = f'https://www.publico.pt/jornal?date={date.strftime("%Y%m%d")}'
  print(url) 
  PDFFileName = f'{path}/P_{kind}_{date.strftime("%Y")}_{date.strftime("%m")}_{date.strftime("%d")}.pdf'
  if os.path.isfile(PDFFileName) == False :
    PDFUrl = getPDFUrl(url, kind, browser)
    if PDFUrl != "Not Found":
      publico_auth = browser.get_cookie('publico_auth')
      if publico_auth is not None:
        cookiesRequest = { 'publico_auth': publico_auth['value']}
        pdfContent = requests.post(PDFUrl, stream = True, cookies = cookiesRequest)
        if pdfContent.status_code == 200:
          pdfContent.raw.decode_content = True 
          with open(PDFFileName,'wb') as f:
            shutil.copyfileobj(pdfContent.raw, f)
            print(f'done: {date}')
        else:
            print(f'error in url: {url}')
      else:
        print("Error Auth")
        os.remove("cookies.pkl")
    else:
      print(f"Not found {kind} in {date}")
  else:
    print(f"already downloaded: {PDFFileName}")


# o modulo selenium simula um navegador, o que é necessário visto que o Público
#  exige que se esteja autenticado para ter acesso aos pdfs de seu arquivo.
def getBrowser():
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--incognito")
  chrome_prefs = {}
  chrome_options.experimental_options["prefs"] = chrome_prefs
  chrome_prefs["profile.default_content_settings"] = {"images": 2}
  browser = webdriver.Chrome(options=chrome_options)
  browser.implicitly_wait(20)
  browser.set_page_load_timeout(20)
  urlLogin = "https://www.publico.pt"
  urlJornal = "https://www.publico.pt/jornal/"
  browser.get(urlJornal)
  if os.path.isfile('cookies.pkl'):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
      browser.add_cookie(cookie)
  else:
    browser.get(urlLogin)
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-fxmqu"))).click()
    browser.find_element_by_xpath('//*[@id="masthead-container"]/div[2]/ul/li[3]/button').click()
    WebDriverWait(browser, 20).until(EC.text_to_be_present_in_element_value((By.CLASS_NAME, "login-form__button"), "Continuar"))
    browser.find_element_by_id("login-email-input").send_keys(os.environ.get("PUBLICO_USERNAME"))
    browser.find_element_by_class_name("login-form__button").click()
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, "login-password-input")))
    browser.find_element_by_id("login-password-input").send_keys(os.environ.get("PUBLICO_PASSWORD"))
    browser.find_element_by_xpath('//*[@id="login-form-password"]/div/div[4]/input').click()
    WebDriverWait(browser, 40)
    browser.get(urlLogin)
    browser.get(urlLogin)
    pickle.dump( browser.get_cookies(), open("cookies.pkl","wb"))
  return browser


global browser
browser = getBrowser()
periods = ["2021-01-13/2021-12-31"]
for period in periods:
    periodArray = period.split('/')
    start = datetime.fromisoformat(periodArray[0])
    end = datetime.fromisoformat(periodArray[1])
    current = start
    while current <= end:
      try:
        getPDF(current, "p2", browser)
        getPDF(current, "ipsilon", browser)
        current += timedelta(days=1)
      except Exception as e:
        browser = getBrowser()
        print (e)
        print (current)
      time.sleep(2)
      
      







