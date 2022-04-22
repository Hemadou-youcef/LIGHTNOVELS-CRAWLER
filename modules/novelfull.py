import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

headers = {
    "Host":"novelfull.com",
    "Accept":"*/*",
    "User-Agent":"PostmanRuntime/7.28.0",
}
def get_chapters(url):
    return_values = []
    try:
        #GETTING ALL CHAPTER LI TAGS
        page = requests.get(url,headers=headers)
        soup = BeautifulSoup(page.content, 'html5lib')
        getId = int(soup.select('#truyen-id')[0]["value"])
        novel_name = soup.select("h3.title")[0].text.upper()
        url = "https://novelfull.com/ajax-chapter-option?novelId={}"
        page = requests.get(url.format(getId),headers=headers)
        soup = BeautifulSoup(page.content, 'html5lib')
        results = soup.select('select.chapter_jump>option')

        return_values.append(novel_name)
        for key in ['\\','/',':','?','*','<','>','|','"']:
            return_values[0] = return_values[0].replace(key,'')

        url = urlparse(url)
        #MAKE A DICTIONARY FOR CHAPTER HREF AND NAME
        novel_chapters = []
        for i in range(len(results)):
            link = results[i]
            novel_chapters.append({
                "link":url.scheme + "://" + url.netloc + link['value']
            })
        return_values.append(novel_chapters)
        return return_values

    except Exception as e:
        print(e)
def get_content(url,session_request,end):
    try:
        page = session_request.get(url,headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, 'html5lib')
        for s in soup.select('#chapter-content div'):
            s.extract()
        results = soup.select('#chapter-content p')

        return results
    except:
        pass
