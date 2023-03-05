from collections import deque
from html.parser import HTMLParser
from threading import Lock
from urllib.error import HTTPError
from urllib.parse import urljoin
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor


TARGET_URL=input("Enter the URL : ")
pname=input("Enter the Product Name : ")
NUMBER_OF_THREADS = 10
MAX_DEPTH = 3



class MyHTMLParser(HTMLParser):
    def __init__(self, url=None):
        super().__init__()
        self.links = []
        self.url = url

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            if "href" not in dict(attrs):
                return

            href = dict(attrs)["href"]

            
            if self.url:
                href = urljoin(self.url, href)

            self.links.append(href)


def get_html(url):
    
    try:
        return urlopen(url).read().decode("utf-8")
    except HTTPError as e:
        return e.read().decode("utf-8")



def parse_html(html, url=None):
    
    parser = MyHTMLParser(url)
    parser.feed(html)
    return parser

data=[]

def handle(url, depth, callback, lock):
    
    html = get_html(url)
    links = parse_html(html, url).links



 
    with lock:
        
        pass
    u=[]
    if f'{pname}' in url:
        data.append(url)
    


    for link in links:

        with lock:
            callback((depth + 1, link))


def crawl(url, max_depth):
    
    seen = set()
    crawling = deque([(0, url)])
    lock = Lock()
    with ThreadPoolExecutor(max_workers=NUMBER_OF_THREADS) as executor:
        tasks = []
        while crawling:
            depth, url = crawling.popleft()

            
            if depth == max_depth:
                continue

           
            if url in seen:
                continue
            seen.add(url)

            
            tasks.append(executor.submit(handle, url, depth, crawling.append, lock))
            if len(tasks)==50:
                break
            
            
            while tasks and not crawling:
                tasks.pop().result()
    
            
    



if __name__ == "__main__":
    crawl(TARGET_URL, max_depth=MAX_DEPTH)


mlist=[]
for i in range(len(data)):
    model=data[i][24:].split("/")
    mlist.append(model[1])

for i in range(len(data)):
    print('\n Model Name : '+mlist[i],'\n Link : '+ data[i])