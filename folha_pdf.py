"""Script to get editions from folha de são paulo newspaper"""
import pickle
import time
import os
import calendar
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
load_dotenv()



def get_path(path_name):
    """return the path name after created it"""
    Path(path_name).mkdir(parents=True, exist_ok=True)
    return path_name

def screenshot(subject):
    """make screen shots when is necessary, used for debug"""
    gmt = time.gmtime()
    timestamp = calendar.timegm(gmt)
    path = get_path('screenshots')
    browser.save_screenshot(f'{path}/{subject}_{timestamp}.png')

def authentication():
    """authentication method for legal operations"""
    if os.path.isfile('cookies_folha.pkl'):
        cookies = pickle.load(open("cookies_folha.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
    else:
        browser.get(URL_LOGIN)
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, "registerEmail")))
        browser.find_element_by_id("registerEmail").send_keys(os.environ.get("FOLHA_USERNAME"))
        browser.find_element_by_id("registerPassword").send_keys(os.environ.get("FOLHA_PASSWORD"))
        browser.find_element_by_xpath('//*[@id="login"]/div[4]/button').click()
        WebDriverWait(browser, 40)
        screenshot('login')

def get_browser():
    """get browser for all operations"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--incognito")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    new_browser = webdriver.Chrome(options=chrome_options)
    new_browser.implicitly_wait(20)
    new_browser.set_page_load_timeout(20)
    return new_browser


URL_LOGIN = "https://login.folha.com.br/login"
URL_NEWSPAPER = "https://acervo.folha.com.br/index.do"

browser = get_browser()
authentication()

