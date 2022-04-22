import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from time import sleep
from requests import request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import logging


driver = None


def create_driver():
    global driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")

    driver = uc.Chrome(options=options)
    # driver.set_window_position(-10000,0)


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


scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    }
)
headers = {
    "Cookie" : "cf_clearance=FxqW5cjTb9YxvJ0I.dYNI6pvL66TSlXz5_P9Piewew4-1648751175-0-150; viewed_ids=912832,1132601,131894,1094751,910574,782428,751045,1205077; read_mark=%7B%221178762%22%3A1600328%2C%22751045%22%3A1742566%2C%22782428%22%3A1742557%2C%22910574%22%3A1742545%7D; viewed_chapter_ids=1600328,1742545,1742557,1742566; dle_skin=Green; PHPSESSID=12ufos52nln5oi2pp55u1hr6qh; googtrans=null; googtrans=null; __cf_bm=lHzrkk4bp4Wlpig2ScTkv2RdCispJmJYULNz1yUKxpI-1650207929-0-AXxYMf8tcyoaBm3RSz3uk4DBw0OA79bRDxNXgqFFChpBCGWCAcgL2xfUwFKWDSsJMddb3jcwXsyjWE1rb+lm6Lo=",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Host":"ranobes.net"
}

def get_chapters(url):
    return_values = []
    global last_link
    global driver
    try:
        cookie = ""
        driver.get(url)
        try_counter = 0
        while True and try_counter <= 5: 
            try:
                myElem = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'body')))

                for i in driver.get_cookies():
                    cookie = cookie + i["name"] + "=" + i["value"] + ";"
                # headers["Cookie"] = cookie
                
                close_driver()
                break
            except:
                try_counter = try_counter + 1
        if try_counter == 6:
            return False

        real_url = url.split("/")[4].split("-")[0]
        url = "https://ranobes.net/chapters/" + real_url + "/"
        chapters_page = scraper.get(url,headers=headers)
        index = chapters_page.text.index('<script>window.__DATA__')
        chapters_page = chapters_page.text[index + 26 :]
        index = chapters_page.index('</script>')
        chapters_page = chapters_page[:index]

        data = json.loads(chapters_page)
        novel_name = data["book_title"]

        return_values.append(novel_name)
        for key in ['\\','/',':','?','*','<','>','|','"']:
            return_values[0] = return_values[0].replace(key,'')

        chapters_dict = data["chapters"]
        novel_chapters = []

        
        for i in range(2,data["pages_count"] + 1):
            page = scraper.get(url + "page/" + str(i) + "/",headers=headers)
            index = page.text.index('<script>window.__DATA__')
            page = page.text[index + 26 :]
            index = page.index('</script>')
            page = page[:index]
            data = json.loads(page)
            chapters_dict = chapters_dict + data["chapters"]
            sleep(0.1)

        for i in range(len(chapters_dict)):
            link = "https://ranobes.net/read-" + chapters_dict[i]["id"] + ".html"
            novel_chapters.insert(0,{
                "link": link
            })
        return_values.append(novel_chapters)

        return return_values

    except Exception as e:
        print(e)
def get_content(url,session_request):
    try:
        page = scraper.get(url,timeout=10,headers=headers)
        soup = BeautifulSoup(page.content, 'html5lib')
        results = soup.select('#arrticle p')
        sleep(0.1)
        return results
    except:
        pass


get_chapters("https://ranobes.net/novels/912832-im-really-not-the-demon-gods-lackey-v106171.html")