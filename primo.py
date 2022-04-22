import sys
import os
import time
import importlib
from urllib.parse import urlparse
import requests

website = {
    "trxs.cc":"trxs",
    "www.trxs.cc":"trxs",
    "trxs.org":"trxs",
    "www.trxs.org":"trxs",
    "jpxs123.org":"trxs",
    "www.jpxs123.org":"trxs",
    "jpxs123.cc":"trxs",
    "www.jpxs123.cc":"trxs",
    "powanjuan.cc":"powanjuan",
    "www.powanjuan.cc":"powanjuan",
    "ffxs8.com":"powanjuan",
    "www.ffxs8.com":"powanjuan",
    "sjks88.com":"sjks88",
    "www.sjks88.com":"sjks88",
    "sjks8.cc":"sjks88",
    "www.sjks8.cc":"sjks88",
    "novelfull.com":"novelfull",
    "www.novelfull.com":"novelfull",
    "ranobes.net":"ranobes",
    "www.ranobes.net":"ranobes",
    "wuxiaworld.site":"wuxia",
    "www.wuxiaworld.site":"wuxia",
    "kolnovel.com":"kolnovel",
    "fanfiction.net":"fanfiction",
    "www.fanfiction.net":"fanfiction",
    "wattpad.com":"wattpad",
    "www.wattpad.com":"wattpad",
}
lang = {
    "zh-CN":[
        "trxs.cc","www.trxs.cc","trxs.org","www.sjks88.com","sjks88.com","www.ffxs8.com","ffxs8.com",
        "www.powanjuan.cc","powanjuan.cc","www.jpxs123.cc","jpxs123.cc","jpxs123.org","www.trxs.org","www.jpxs123.org",
        "sjks8.cc","www.sjks8.cc"
    ],
    "en":[
        "www.wuxiaworld.site","wuxiaworld.site","www.ranobes.net","ranobes.net","www.novelfull.com","novelfull.com",
        "fanfiction.net","www.fanfiction.net","wattpad.com","www.wattpad.com"
    ],
    "ar":[
        "kolnovel.com"
    ]
}

class Accumulator:
    def light_novel(self):
        print("")
        print("░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗██╗░░░░░███████╗██████╗░")
        print("██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██║░░░░░██╔════╝██╔══██╗")
        print("██║░░╚═╝██████╔╝███████║░╚██╗████╗██╔╝██║░░░░░█████╗░░██████╔╝")
        print("██║░░██╗██╔══██╗██╔══██║░░████╔═████║░██║░░░░░██╔══╝░░██╔══██╗")
        print("╚█████╔╝██║░░██║██║░░██║░░╚██╔╝░╚██╔╝░███████╗███████╗██║░░██║")
        print("░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚══════╝╚══════╝╚═╝░░╚═╝")
        print("\n")
        try:
            while True:
                self.novel_url = input("WRITE NOVEL URL: ")
                if self.novel_url :
                    break
            self.suffix = ""
            
            
            url = urlparse(self.novel_url)
            try:
                self.site_module = importlib.import_module("modules." + website[url.netloc])
                for x in lang.keys():
                    if url.netloc in  lang[x]:
                        self.lang = x
                    
            except:
                print("website not supported, Try another one")
                return False

            self.number = input("HOW MUCH CHAPTER(0=ALL CHAPTER): ")
            if not self.number :
                self.number = 0
            else:
                self.number = int(self.number)
            self.type = input("TXT OR HTML (DEFAULT = TXT): ").lower()
            if not self.type :
                self.type="txt"
            if self.type == "txt":
                self.single_file = input("SINGLE FILE??: (Y/N)(DEFAULT=N): ").lower()
                if not self.single_file :
                    self.single_file="n"
            else:
                self.single_file="n"
            
            
            
            header = open("required/header.txt", "r")
            self.header = header.read()
            header.close()

            footer = open("required/footer.txt", "r")
            self.footer = footer.read()
            footer.close()

            style = open("required/style.css", "r")
            self.style = style.read()
            if self.lang != "ar":
                self.style.replace("rtl","ltr")
            style.close()
            
            #GET CHANPTER
            self.chapters = self.get_chapter()
            if not bool(self.chapters):
                sys.exit()
            #CREATING DOCUMENT FOR NOVEL
            self.document_creating()
            
            #DOWNLOADING
            self.download_loop()
            if self.single_file == "y":
                new_file = open(self.novel_name + ".txt", "w",encoding="utf-8")
                new_file.write(self.single_txt)
                new_file.close()

            sys.stdout.write("│\n")
            print("DONE!!")
            print("THANK FOR USING OUR PRODUCT")
        except Exception as e:
            print("ERROR ENTRING LIGHT NOVEL")
            print(e)
    def get_chapter(self):
        print("GETTING CHAPTERS...")
        try:
            try_counter = 0
            while True and try_counter <= 10: 
                return_values = self.site_module.get_chapters(self.novel_url)
                if len(return_values[1]) != 0:
                    self.novel_name = return_values[0]
                    return return_values[1]
                time.sleep(5)
                try_counter += 1    
            if try_counter == 11:
                return False
            

        except Exception as e:
            print("ERROR GETTING CHAPTERS")
            print(e)
    def document_creating(self):
        print("CREATING DOCUMENT...")
        try:
            if not os.path.exists('downloads'):
                os.mkdir('downloads')
            os.chdir('downloads')
            
            if not os.path.exists(self.lang):
                os.mkdir(self.lang)
            os.chdir(self.lang)
            
            i = 2
            while True:
                if os.path.exists(self.novel_name + self.suffix):
                    self.suffix  = "-" + str(i)
                    i += 1
                else:
                    os.mkdir(self.novel_name + self.suffix)
                    os.chdir(self.novel_name + self.suffix)
                    break
            print("CREATING SUCCESSFULLY")
        except Exception as e:
            print("ERROR CREATING DOCUMENT")
            print("CLOSING...")
            print(e)
            sys.exit()
    def download_loop(self):
        try:
            print("START DOWNLOADING")
            
            
            self.single_txt = ""
            range_bar = 0
            self.previous = "#"

            if self.number == 0:
                range_bar_unit = 50 / len(self.chapters)
                number_chapter_downloded = len(self.chapters)
            else:
                range_bar_unit = 50 / self.number
                number_chapter_downloded = self.number

            current_message = "0/" + str(number_chapter_downloded)
            self.progress_bar_header(current_message)
            
            self.session_requests = requests.Session()
            for i in range(number_chapter_downloded):
                range_bar += range_bar_unit

                try_counter = 0
                while True and try_counter <= 3: 
                    try:
                        if self.downloader(self.chapters[i]["link"],"CHAPTER-" + str(i + 1),i + 1):
                            break
                        else:
                            try_counter == 4
                            break
                    except:
                        try_counter += 1
                if try_counter == 4:
                    print("error download chapters")
                    time.sleep(3)
                    sys.exit()
                current_message = str(i + 1) + "/" + str(number_chapter_downloded)
                sys.stdout.write(" " * (self.progress - 1) + "|" + current_message + " ")
                sys.stdout.write("\b" * (self.progress + len(current_message) + 1))
               
                sys.stdout.flush()

                for j in range(int(range_bar)):
                    self.progress_bar_animated()
                    range_bar-= 1
        except Exception as e:
            print("ERROR WHILE DOWNLOAD")
            print(e)
    def downloader(self,url,chapter_name,current_loop):
        try:
            end = False
            if self.number == 0:
                end = (len(self.chapters) == current_loop)
            else:
                end = (self.number == current_loop)

            try_counter = 0
            while True and try_counter <= 10: 
                results = self.site_module.get_content(url,self.session_requests,end)
                if len(results) != 0:
                    break
                time.sleep(5)
                try_counter += 1    

            if try_counter == 11:
                return False
            if self.single_file == "y":
                self.single_txt += "----------------------------------\n"
                self.single_txt += "CHAPTER-" + str(current_loop) + "\n\n"

                for i in range(len(results)):
                    self.single_txt +=results[i].text.strip() + '\n'

                self.single_txt += "\n\n"
            else:
                if self.type == "html":
                    navigation = '<div id="navigation"><a href="' + self.previous + '"><button>PREV</button></a><a href="CHAPTER-' + str(current_loop + 1) + '.html"><button>NEXT</button></a></div>'
                    new_file = open(chapter_name + ".html", "w",encoding="utf-8")
                    new_file.write(self.header)
                    new_file.write(navigation)
                    for i in range(len(results)):
                        new_file.write( "<p>" + results[i].text.strip() + "</p>")
                    new_file.write(navigation)
                    new_file.write(self.footer)
                else:
                    new_file = open(chapter_name + ".txt", "w",encoding="utf-8")
                    for i in range(len(results)):
                        new_file.write(results[i].text.strip() + '\n')
                
                new_file.close()
            return True
        except Exception as e:
            if self.type == "html":
                os.remove(chapter_name +  + ".html") 
            else:
                os.remove(chapter_name +  + ".txt") 
            print("ERROR HAPPEN IN " + chapter_name)
            return False
    def progress_bar_header(self,message):
        toolbar_width = 50
        self.progress = 51
        print("")
        print("PROGRESS...")
        sys.stdout.write("│%s│" % (" " * toolbar_width) + message + " ")
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width + len(message) + 2))

    def progress_bar_animated(self):
        sys.stdout.write("█")
        sys.stdout.flush()
        self.progress -= 1
Acc = Accumulator()
Acc.light_novel()
time.sleep(5)