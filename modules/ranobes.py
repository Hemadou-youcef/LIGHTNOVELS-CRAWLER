from bs4 import BeautifulSoup
from urllib.parse import urlparse
import cloudscraper
import json
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
        real_url = url.split("/")[4].split("-")[0]
        url = "https://ranobes.net/chapters/" + real_url
        chapters_page = scraper.get(url)
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
            page = scraper.get(url + "/page/" + str(i))
            index = page.text.index('<script>window.__DATA__')
            page = page.text[index + 26 :]
            index = page.index('</script>')
            page = page[:index]
            data = json.loads(page)
            chapters_dict = chapters_dict + data["chapters"]

        for i in range(len(chapters_dict)):
            link = "https://ranobes.net/read-" + chapters_dict[i]["id"] + ".html"
            novel_chapters.insert(0,{
                "link": link
            })
        return_values.append(novel_chapters)
        return return_values

    except Exception as e:
        print(e)
def get_content(url):
    try:
        page = scraper.get(url,timeout=10)
        soup = BeautifulSoup(page.content, 'html5lib')
        results = soup.select('#arrticle p')
        
        return results
    except:
        pass
