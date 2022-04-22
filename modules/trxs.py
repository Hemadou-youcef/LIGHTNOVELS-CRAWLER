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

        results = soup.select('.book_list li')

        novel_name = soup.select(".infos>h1:first-child")[0].text.upper()

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
        # read_chapterDetail
        # content
        for s in soup.select('.read_chapterDetail span'):
            s.extract()
        results = soup.select('.read_chapterDetail p')

        return results
    except:
        pass
