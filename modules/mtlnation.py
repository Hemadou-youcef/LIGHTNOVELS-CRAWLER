from bs4 import BeautifulSoup
from urllib.parse import urlparse
from time import sleep
from requests import request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import logging

logging.disable(logging.CRITICAL)
logging.disable(logging.ERROR)
logging.disable(logging.INFO)

driver = None
path = os.getcwd() + "\\chromedriver.exe"

def create_driver():
    global driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(chrome_options=options,executable_path=path)
    driver.set_window_position(-10000,0)


def close_driver():
    global driver
    driver.quit()

def wait_until(url,time,try_times):
    global driver
    driver.get(url)
    driver.execute_script('window.open("' + url + '/","_blank");')
    try_counter = 0
    while True and try_counter <= try_times:
        try:
            myElem = WebDriverWait(driver, time).until(EC.presence_of_element_located((By.ID, 'manga-reading-nav-head')))
            break
        except:
            try_counter = try_counter + 1
    if try_counter == (try_times + 1):
        return False

create_driver()

last_link = ""

def get_chapters(url):
    return_values = []
    global last_link
    global driver
    try:
        driver.get(url)
        driver.execute_script('window.open("' + url + '/","_blank");')
        try_counter = 0
        while True and try_counter <= 5: 
            try:
                myElem = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'wp-manga-chapter')))
                break
            except:
                try_counter = try_counter + 1
        if try_counter == 6:
            return False
        chapters_page = driver.page_source

        soup = BeautifulSoup(chapters_page, 'html5lib')
        # results = soup.select('.list>li')
        results = soup.select('ul.main>li')

        # novel_name = soup.select(".box-artic>h1")[0].text.upper()
        novel_name = soup.select("div.post-title>h1")[0].text.upper()

        return_values.append(novel_name.strip())
        for key in ['\\','/',':','?','*','<','>','|','"']:
            return_values[0] = return_values[0].replace(key,'')

        # url = urlparse(url)
        #MAKE A DICTIONARY FOR CHAPTER HREF AND NAME
        novel_chapters = []
        for i in range(len(results)):
            link = results[i].a
            novel_chapters.append({
                "link":link['href']
            })
            
        novel_chapters = novel_chapters[::-1]
        last_link = novel_chapters[len(novel_chapters) - 1]
        return_values.append(novel_chapters)
        return return_values


    except Exception as e:
        print(e)
def get_content(url,session_request,end):
    global last_link
    global driver
    try:
        
        driver.get(url)
        try_counter = 0
        while True and try_counter <= 5:
            try:
                myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'manga-reading-nav-head')))
                break
            except:
                driver.delete_all_cookies()
                wait_until(url,20,5)
                try_counter = try_counter + 1
                driver.refresh()

        if try_counter == 6:
            return False
        data = driver.page_source
        data = data.replace("</p>","</p><p>")
        data = data.replace("</p><p><p>","</p><p>")
        soup = BeautifulSoup(data, 'html5lib')

        results = soup.select('.c-blog-post>div:nth-child(6)>div>div>div>div:nth-child(2) p')
        if(last_link == url or end):
            driver.quit()
        return results
    except:
        pass
