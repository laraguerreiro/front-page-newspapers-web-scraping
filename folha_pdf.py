"""Script to get editions from folha de são paulo newspaper"""
import gc
import glob
import pickle
import shutil
import time
import os
import calendar
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from datetime import datetime, timedelta
from pathlib import Path
import requests
import img2pdf
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
    browser.get(URL_LOGIN)
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, "registerEmail")))
    screenshot('login')
    browser.find_element_by_id("registerEmail").send_keys(os.environ.get("FOLHA_USERNAME"))
    screenshot('login')
    browser.find_element_by_id("registerPassword").send_keys(os.environ.get("FOLHA_PASSWORD"))
    screenshot('login')
    try:
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login"]/div[4]/button'))).click()
    except:
        browser.refresh()
        screenshot('error_login')
    WebDriverWait(browser, 20)
        
def get_reader_url(url_search):
    browser.get(url_search)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    results = soup.find("div", {"id": "results"})
    a_result = results.find_all("a")[0]
    href_result = a_result.get('href')
    return href_result

def get_pages(url_reader, path):
    browser.get(url_reader)
    time.sleep(30)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    newspaper = soup.find("div", {"id": "slider-wrapper"})
    pages = newspaper.find_all("figure")
    page_number = 1
    page_file_names = []
    for page in (pages):
        img = page.find("img")
        page_download_url = img.get('data-zoom')
        img_content = requests.get(page_download_url, stream = True, timeout=10)
        extension = img_content.headers['content-type'].split("/")[-1]
        if page_number < 10:
            img_filename = f'{path}/0{page_number}_page.{extension}'
        else:
            img_filename = f'{path}/{page_number}_page.{extension}'
        if img_content.status_code == 200:
            img_content.raw.decode_content = True 
            with open(img_filename,'wb') as file:
                shutil.copyfileobj(img_content.raw, file)
            page_file_names.append(img_filename)
            print(f'Downloaded page {page_number} of {len(pages)}')
            page_number = page_number + 1
        else:
            print(f'error downloading page {page_number}, i will try again')
    return page_file_names
    
def get_pdf(date):
    """Make a pdf file with all pages of a date"""
    year = date.strftime("%Y")
    month = date.strftime("%m")
    day = date.strftime("%d")
    mydict = {
        'keyword': '', 
        'periododesc': f'{day}/{month}/{year}', 
        'por': 'Por Dia', 
        'startDate': '', 
        'endDate': '', 
        'days': day, 
        'month': month, 
        'year': year, 
        'jornais':1 
        }
    qstr = urlencode(mydict)
    url_search = f'{URL_NEWSPAPER}/busca.do?{qstr}'
    reader_url = get_reader_url(url_search)
    url_reader = f'{URL_NEWSPAPER}{reader_url}'
    print(f'Starting edition {date}')
    temp_path = get_path(f'tmp_{year}_{month}_{day}')
    get_pages(url_reader, temp_path)
    imgs = []
    path_pdf = get_path(f'FolhaPDF/{year}') 
    pdf_filename = f'{path_pdf}/F_{date.strftime("%Y_%m_%d")}.pdf'
    list_of_files = sorted( filter( lambda x: os.path.isfile(os.path.join(temp_path, x)),
                        os.listdir(temp_path) ) )
    print (f'Starting PDF {pdf_filename}')
    for page_file_name in list_of_files:
        path = os.path.join(temp_path, page_file_name)
        if os.path.isdir(path):
            continue
        imgs.append(path)
        with open(pdf_filename,"wb") as f:
            f.write(img2pdf.convert(imgs))
    print (f'Finished PDF {pdf_filename}')
    print (f'Removing tmp path {temp_path}')
    shutil.rmtree(temp_path)
    print (f'Removed tmp path {temp_path}')
    print(f'Finished edition {date}')
    

def get_browser():
    """get browser for all operations"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=2560,1440")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    new_browser = webdriver.Chrome(options=chrome_options)
    new_browser.implicitly_wait(20)
    new_browser.set_page_load_timeout(60)
    return new_browser


URL_LOGIN = "https://login.folha.com.br/login"
URL_NEWSPAPER = "https://acervo.folha.com.br"

browser = get_browser()
authentication()
periods = ["2020-01-08/2020-12-31"]
for period in periods:
    gc.collect()
    period_array = period.split('/')
    start = datetime.fromisoformat(period_array[0])
    end = datetime.fromisoformat(period_array[1])
    current = start
    while current <= end:
        try:
            get_pdf(current)
            current += timedelta(days=1)
        except:
            print(f'Exception when I was getting {current}. I will try again!')
            browser = get_browser()
