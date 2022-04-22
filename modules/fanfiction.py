from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
import os

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
            myElem = WebDriverWait(driver, time).until(EC.presence_of_element_located((By.ID, 'storytext')))
            break
        except:
            try_counter = try_counter + 1
    if try_counter == (try_times + 1):
        return False

create_driver()

first_url = ""


def get_chapters(url):
    return_values = []
    global driver
    global first_url
    try:
        driver.get(url)
        driver.execute_script('window.open("' + url + '/","_blank");')
        try_counter = 0
        while True and try_counter <= 5:
            try:
                myElem = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, 'storytext')))
                break
            except:
                try_counter = try_counter + 1
        if try_counter == 6:
            return False
        chapters_page = driver.page_source

        soup = BeautifulSoup(chapters_page, 'html5lib')
        # results = soup.select('.list>li')
        results = soup.select('#chap_select option')
        results = results[:len(results) // 2]

        # novel_name = soup.select(".box-artic>h1")[0].text.upper()
        novel_name = soup.select("#profile_top >b")[0].text.upper()

        return_values.append(novel_name.strip())
        for key in ['\\', '/', ':', '?','*','<','>','|','"']:
            return_values[0] = return_values[0].replace(key, '')

        # url = urlparse(url)
        # MAKE A DICTIONARY FOR CHAPTER HREF AND NAME
        novel_chapters = []
        for i in range(len(results)):
            link = url.split("/")
            link[5] = str(i + 1)
            link = "/".join(link)
            novel_chapters.append({
                "link": link
            })

        first_url = novel_chapters[0]["link"]
        return_values.append(novel_chapters)
        return return_values

    except Exception as e:
        print(e)


def get_content(url, session_request,end):
    global first_url
    try:
        # page = requests.get(url,timeout=10,headers=headers)
        driver.get(url)
        try_counter = 0
        while True and try_counter <= 5:
            try:
                myElem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'storytext')))
                break
            except:
                driver.delete_all_cookies()
                wait_until(url,20,5)
                try_counter = try_counter + 1
                driver.refresh()
        if try_counter == 6:
            return False

        soup = BeautifulSoup(driver.page_source, 'html5lib')

        for s in soup.select('#storytext hr'):
            new_p = soup.new_tag("p")
            new_p.append("------------------------")
            s.insert_after(new_p)
        
        results = soup.select('#storytext p')
        
        if first_url == url:
            new_p = soup.new_tag("p")
            new_p.append("-------------------------------")
            results.insert(0,new_p)
            desc = soup.select('#profile_top>div.xcontrast_txt')[0].text
            desc = desc.replace("\n",'</br>')
            for line in reversed(desc.split("</br>")):
                new_p = soup.new_tag("p")
                new_p.append(line.strip())
                results.insert(0,new_p)

        if end:
            driver.quit()
        return results
    except:
        pass
