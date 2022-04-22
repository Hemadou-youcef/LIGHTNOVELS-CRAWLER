import requests
from bs4 import BeautifulSoup
import mtranslate
from urllib.parse import urlparse

def get_chapters(url):
    return_values = []
    try:
        #GETTING ALL CHAPTER LI TAGS
        try_counter = 0
        while True and try_counter <= 3: 
            try:
                page = requests.get(url, timeout=10)
                break
            except:
                print("REQUEST TIME OUT (" + str(3 - try_counter) + " TRY LEFT)")
                try_counter += 1
        
        soup = BeautifulSoup(page.content, 'lxml')
        results = soup.select('.epcheck li')

        novel_name = soup.select("h1.entry-title")[0].text.upper()

        return_values.append(novel_name)
        for key in ['\\','/',':','?','*','<','>','|','"']:
            return_values[0] = return_values[0].replace(key,'')

        url = urlparse(url)
        #MAKE A DICTIONARY FOR CHAPTER HREF AND NAME
        novel_chapters = []
        for i in range(len(results),0,-1):
            link = results[i-1].a
            novel_chapters.append({
                "link":link['href']
            })
        return_values.append(novel_chapters)
        return return_values

    except Exception as e:
        pass
def get_content(url,session_request,end):
    try:
        page = session_request.get(url, timeout=10)
        soup = BeautifulSoup(page.content, 'lxml')
        for s in soup.select('.epcontent div'):
            s.extract()
        for s in soup.select('.epcontent span'):
            s.extract()
        results = soup.select('.epcontent p')

        return results
    except:
        pass
