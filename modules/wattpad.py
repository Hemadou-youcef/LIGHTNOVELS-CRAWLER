import requests
from bs4 import BeautifulSoup
import json
import cloudscraper
from urllib.parse import urlparse

scraper = cloudscraper.create_scraper()
headers = {
    "Host": "www.wattpad.com",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
}
first_url = ""
desc = ""
def get_chapters(url):
    return_values = []
    global first_url
    global desc
    try:
        #GETTING ALL CHAPTER LI TAGS
        page = scraper.get(url,headers=headers)
        soup = BeautifulSoup(page.content, 'html5lib')
        # results = soup.select('.list>li')
        results = soup.select('div.story-parts li')
        results = results[:len(results) // 2]
        # novel_name = soup.select(".box-artic>h1")[0].text.upper()
        novel_name = soup.select("title")[0].text.split("-")[0].upper()

        return_values.append(novel_name.strip())
        for key in ['\\','/',':','?','*','<','>','|','"']:
            return_values[0] = return_values[0].replace(key,'')

        desc = soup.select(".description-text")[0].text
        desc = desc.replace("\n",'</br>')

        url = urlparse(url)
        #MAKE A DICTIONARY FOR CHAPTER HREF AND NAME
        novel_chapters = []
        for i in range(len(results)):
            link = results[i].a
            novel_chapters.append({
                "link":url.scheme + "://" + url.netloc + link['href']
            })
        first_url = novel_chapters[0]["link"]
        return_values.append(novel_chapters)
        return return_values

    except Exception as e:
        pass
def get_content(url,session_request,end):
    global first_url
    global desc
    try:
        page = session_request.get(url, timeout=10,headers=headers)

        index = page.text.index('window.prefetched = ')
        page = page.text[index + 20 :]
        index = page.index('</script>')
        page = page[:index - 6]
        data = json.loads(page)
        first_element = next(iter(data))
        pages = data[first_element]["data"]["pages"]
        results = []
        for page in range(pages):
            temp_url = url + "/page/" + str(page)
            temp_page = session_request.get(temp_url, timeout=10,headers=headers)
            temp_soup = BeautifulSoup(temp_page.content, 'html5lib')
            for s in temp_soup.select('div.panel-reading span'):
                s.extract()
            for s in temp_soup.select('div.panel-reading p'):
                s = s.get_text(strip=True)
            results.append(temp_soup.select('div.panel-reading p'))

        results = results[0]
        if first_url == url:
            new_p = temp_soup.new_tag("p")
            new_p.append("-------------------------------")
            results.insert(0,new_p)
            for line in reversed(desc.split("</br>")):
                new_p = temp_soup.new_tag("p")
                new_p.append(line.strip())
                results.insert(0,new_p)

            
        return results
    except:
        pass
