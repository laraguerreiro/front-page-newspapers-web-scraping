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
  browser.implicitly_wait(10)
  urlLogin = "https://www.publico.pt/login/"
  urlJornal = "https://www.publico.pt/jornal/"
  browser.get(urlJornal)
  if os.path.isfile('cookies.pkl'):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
      browser.add_cookie(cookie)
  else:
    browser.get(urlLogin)
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-fxmqu"))).click()
    WebDriverWait(browser, 20).until(EC.text_to_be_present_in_element_value((By.CLASS_NAME, "login-form__button"), "Entrar"))
    browser.find_element_by_id("user-email").send_keys(os.environ.get("PUBLICO_USERNAME"))
    browser.find_element_by_id("user-password").send_keys(os.environ.get("PUBLICO_PASSWORD"))
    browser.find_element_by_class_name("login-form__button").click()
    WebDriverWait(browser, 20)
    browser.get(urlJornal)
    pickle.dump( browser.get_cookies(), open("cookies.pkl","wb"))
  return browser

browser = getBrowser()
soup = BeautifulSoup(browser.page_source, 'lxml')
pdfElementPrincipal = soup.find_all("ul", {"class": "print-covers__list"})[0]
pdfElement = pdfElementPrincipal.find_all("a")[1]
pdfUrl = pdfElement.get('href')
fileName = f'apagar_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.pdf'
publico_auth = browser.get_cookie('publico_auth')
if publico_auth is not None:
  cookiesRequest = { 'publico_auth': publico_auth['value']}
  pdfContent = requests.post(pdfUrl, stream = True, cookies = cookiesRequest)
  if pdfContent.status_code == 200:
    pdfContent.raw.decode_content = True 
    with open(fileName,'wb') as f:
      shutil.copyfileobj(pdfContent.raw, f)
      print(f'done: {pdfUrl}')
  else:
      print(f'error in url: {pdfUrl}')
else:
  print("Error Auth")
  os.remove("cookies.pkl")

browser.quit()








