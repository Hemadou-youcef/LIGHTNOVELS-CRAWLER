from bs4 import BeautifulSoup
from urllib.parse import urlparse
import cloudscraper
import json
from time import sleep
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    }
)
headers = {
    "Cookie": "__cf_bm=OzbthUSjBxpIg8hDUplq6UY7hqLazIrUCngwv3IPx3o-1648753455-0-AfzlNPuaK3bqgY1nqNs+u3mf/UVK9mCMqJYWbMeD9EGXG4rO78JPCjNt4LMRJTAX4WzlPHbX8Ja/cquhP4WpVYs=; cf_chl_2=534725c2caf13d9; cf_chl_prog=x11; cf_clearance=FxqW5cjTb9YxvJ0I.dYNI6pvL66TSlXz5_P9Piewew4-1648751175-0-150; PHPSESSID=12ufos52nln5oi2pp55u1hr6qh; viewed_ids=1205077",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Host":"ranobes.net"
}
def get_chapters(url):
    return_values = []
    try:
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
def get_content(url,session_request,end):
    try:
        page = scraper.get(url,timeout=10,headers=headers)
        soup = BeautifulSoup(page.content, 'html5lib')
        results = soup.select('#arrticle p')
        sleep(0.1)
        return results
    except:
        pass
