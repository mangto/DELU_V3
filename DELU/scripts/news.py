from urllib.request import urlopen
from bs4 import BeautifulSoup
from json import load, dump

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

urls = [
    "https://www.goeyi.kr/bojeong-h/na/ntt/selectNttList.do?mi=2094&bbsId=984",
    "https://www.goeyi.kr/bojeong-h/na/ntt/selectNttList.do?mi=2074&bbsId=968",
    ]

class news:
    def load_from_url(url:str) -> list[dict]: 
        req = urlopen(urls[1])
        soup = BeautifulSoup(req, 'html.parser')
        new = soup.find_all("tr")

        return new[1:]

    def load(urls:list=urls) -> list[dict]:
        with open(".\\DELU\\data\\news.json", "r", encoding='utf8') as file:
            result = load(file)

        new = []
        for url in urls:
            new += news.load_from_url(url)
        
        for n in new:
            description = [c for c in n.text.replace("\t", "").splitlines() if c != '']
            description = {
                "title":description[1],
                "author":description[3],
                "date":description[5]
            }

            if (description not in result): result.append(description)

        result = sorted(result, key=lambda x:x.get("date"), reverse=True)

        with open(".\\DELU\\data\\news.json", "w", encoding='utf8') as file:
            dump(result, file, ensure_ascii=False, indent="\t")
        
        return result
    
    def load_from_file() -> list:
        with open(".\\DELU\\data\\news.json", "r", encoding='utf8') as file:
            result = load(file)
        return result