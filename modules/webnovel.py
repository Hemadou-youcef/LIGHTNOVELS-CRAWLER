from bs4 import BeautifulSoup
from urllib.parse import urlparse
import cloudscraper
import requests


scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    }
)
first_url = ""
desc = ""
def get_chapters(url):
    return_values = []
    global first_url
    global desc
    global scraper
    try:
        url = url + "/catalog"

        chapters_page = scraper.get(url)
        soup = BeautifulSoup(chapters_page.content, 'html5lib')
        results = soup.select('ol.content-list>li')
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'android',
                'desktop': False
            }
        )
        
        return_values.append(soup.select("a>h3")[0].text.upper())
        for key in ['\\','/',':','?','*','<','>','|','"',"\n"]:
            return_values[0] = return_values[0].replace(key,'')

        desc_page = scraper.get(url.split("/catalog")[0])
        
        soup = BeautifulSoup(desc_page.content, 'html5lib')
        desc = soup.select('section.g_wrap.mt16>div')[0].text
        desc = desc.replace("\n",'</br>')

        url = urlparse(url)
        novel_chapters = []
        for i in range(len(results)):
            link = results[i].a
            novel_chapters.insert(0,{
                "link":url.scheme + "://m.webnovel.com" + link['href']
            })
        novel_chapters = novel_chapters[::-1]
        first_url = novel_chapters[0]["link"]
        return_values.append(novel_chapters)
        return return_values

    except Exception as e:
        print(e)
def get_content(url,session_request,end):
    global first_url
    global desc
    try:
        page = scraper.get(url,timeout=10)
        soup = BeautifulSoup(page.content, 'html5lib')
        results = soup.select('body>div>div>div>div>div:nth-child(2) p')

        if first_url == url:
            new_p = soup.new_tag("p")
            new_p.append("▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
            results.insert(0,new_p)
            for line in reversed(desc.split("</br>")):
                new_p = soup.new_tag("p")
                new_p.append(line.strip())
                results.insert(0,new_p)
        return results
    except:
        pass
