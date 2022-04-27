from bs4 import BeautifulSoup
from urllib.parse import urlparse
from time import sleep
from regex import D
from requests import request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from urllib.parse import parse_qs
import os
import logging

logging.disable(logging.CRITICAL)
logging.disable(logging.ERROR)
logging.disable(logging.INFO)

driver = None
path = os.getcwd() + "\\required\\chromedriver.exe"

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

first_url = ""
desc = ""
def get_chapters(url):
    return_values = []
    global first_url
    global driver
    global desc
    try:
        driver.get(url)
        driver.execute_script('window.open("' + url + '/","_blank");')
        try_counter = 0
        while True and try_counter <= 5: 
            try:
                myElem = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'chapter-list')))
                break
            except:
                try_counter = try_counter + 1
        if try_counter == 6:
            return False
        chapters_page = driver.page_source

        soup = BeautifulSoup(chapters_page, 'html5lib')
        # results = soup.select('.list>li')
        
        pages = soup.select('ul.pagination>li')
        
        desc_line = soup.select('div.content>p')
        for line in desc_line:
            desc = desc + line.text + "</br>"

        novel_name = soup.select("h1.novel-title")[0].text.upper()
        return_values.append(novel_name.strip())
        for key in ['\\','/',':','?','*','<','>','|','"']:
            return_values[0] = return_values[0].replace(key,'')

        results = []    
        if len(pages) == 0:
            results = soup.select("ul.chapter-list>li")
        else:
            for page in pages:
                if page.text.isdigit():
                    if int(page.text) == 1:
                        results = results + soup.select('ul.chapter-list>li')
                    else:
                        link = "https://www.readwn.com" + page.a['href']
                        index = link.index('wjm=')
                        novel_url_name = link[index + 4 :]
                        novel_url = "https://www.readwn.com/e/extend/fy.php?page={}&wjm=" + novel_url_name
                        i = 1
                        while True:
                            driver.get(novel_url.format(str(i)))
                            chapters_page = driver.page_source
                            soup = BeautifulSoup(chapters_page, 'html5lib')
                            if len(soup.select('ul.pagination>li')) == 4:
                                break

                            results = results + soup.select('ul.chapter-list>li')
                            i += 1
                        break
        #MAKE A DICTIONARY FOR CHAPTER HREF AND NAME
        novel_chapters = []
        for i in range(len(results)):
            link = results[i].a
            novel_chapters.append({
                "link": "https://www.readwn.com" + link['href']
            })
            
        first_url = novel_chapters[0]["link"]
        return_values.append(novel_chapters)
        return return_values


    except Exception as e:
        print(e)
def get_content(url,session_request,end):
    global first_url
    global driver
    global desc
    try:
        
        driver.get(url)
        try_counter = 0
        while True and try_counter <= 5:
            try:
                myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'chapter-content')))
                break
            except:
                if try_counter == 0:
                    driver.delete_all_cookies()
                    wait_until(url,20,5)
                else:
                    print("    --- restart drive")
                    close_driver()
                    create_driver()
                    wait_until(url,20,5)
                    print("")

                try_counter = try_counter + 1
                driver.refresh()
        if try_counter == 6:
            return False
        data = driver.page_source
        data = data.replace("</p>","</p><p>")
        data = data.replace("</p><p><p>","</p><p>")
        soup = BeautifulSoup(data, 'html5lib')

        no_filtered_results = soup.select('div.chapter-content p')
        results = []

        zeros = 0
        for tag in no_filtered_results:
            if tag.text == "":
                if zeros == 0:
                    results.append(tag)
                zeros = zeros + 1
            else:
                results.append(tag)
                zeros = 0
        
        if first_url == url:
            new_p = soup.new_tag("p")
            new_p.append("▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
            results.insert(0,new_p)
            
            for line in reversed(desc.split("</br>")):
                new_p = soup.new_tag("p")
                new_p.append(line.strip())
                results.insert(0,new_p)

        if(end):
            driver.quit()
        return results
    except:
        pass