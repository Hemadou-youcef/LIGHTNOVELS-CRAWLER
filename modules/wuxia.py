from bs4 import BeautifulSoup
from urllib.parse import urlparse
import cloudscraper
import time

scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    }
)
def get_chapters(url):
    return_values = []
    try:
        if url[len(url) - 1] != "/":
            url = url + "/"

        chapters_page = scraper.post(url + "ajax/chapters")
        
        soup = BeautifulSoup(chapters_page.content, 'html5lib')
        results = soup.select('ul>li')

        chapters_name = scraper.get(url)
        soup = BeautifulSoup(chapters_name.content, 'html5lib')
        return_values.append(soup.select(".post-title>h1")[0].text.upper())
        for key in ['\\','/',':','?','*','<','>','|','"',"\n"]:
            return_values[0] = return_values[0].replace(key,'')

        novel_chapters = []
        for i in range(len(results)):
            link = results[i].a
            novel_chapters.insert(0,{
                "link":link['href']
            })
        return_values.append(novel_chapters)
        return return_values

    except Exception as e:
        print(e)
def get_content(url):
    try:
        page = scraper.get(url,timeout=10)
        soup = BeautifulSoup(page.content, 'html5lib')
        results = soup.select('.text-left p')
        return results
    except:
        pass

