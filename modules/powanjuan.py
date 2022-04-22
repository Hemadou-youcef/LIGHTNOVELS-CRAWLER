import requests
from bs4 import BeautifulSoup
import mtranslate
from urllib.parse import urlparse

def get_chapters(url):
    return_values = []
    try:
        #GETTING ALL CHAPTER LI TAGS
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html5lib')
        # results = soup.select('.list>li')
        results = soup.select('.catalog li')

        # novel_name = soup.select(".box-artic>h1")[0].text.upper()
        novel_name = soup.select(".desc >h1")[0].text.upper()

        return_values.append(mtranslate.translate(novel_name,"en","auto"))
        for key in ['\\','/',':','?','*','<','>','|','"']:
            return_values[0] = return_values[0].replace(key,'')

        url = urlparse(url)
        #MAKE A DICTIONARY FOR CHAPTER HREF AND NAME
        novel_chapters = []
        for i in range(len(results)):
            link = results[i].a
            novel_chapters.append({
                "link":url.scheme + "://" + url.netloc + link['href']
            })
        return_values.append(novel_chapters)
        return return_values

    except Exception as e:
        pass
def get_content(url,session_request,end):
    try:
        page = session_request.get(url, timeout=10)
        soup = BeautifulSoup(page.content, 'html5lib')

        for s in soup.select('.content span'):
            s.extract()
        results = soup.select('.content p')

        return results
    except:
        pass
