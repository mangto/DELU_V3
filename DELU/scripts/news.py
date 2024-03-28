from urllib.request import urlopen
from bs4 import BeautifulSoup
from json import load, dump

from selenium import webdriver
from selenium.webdriver.common.by import By
import json

url = "https://school.iamservice.net/organization/20019/group/2093903"

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

urls = [
    "https://www.goeyi.kr/bojeong-h/na/ntt/selectNttList.do?mi=2094&bbsId=984",
    "https://www.goeyi.kr/bojeong-h/na/ntt/selectNttList.do?mi=2074&bbsId=968",
    ]

class news:
    def load_from_url(driver:webdriver.Chrome, url:str) -> list[dict]: 
        driver.get(url)
        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')
        new = soup.find_all("tr")

        return new[1:]


    def load(urls:list=urls) -> list[dict]:
        with open(".\\DELU\\data\\news.json", "r", encoding='utf8') as file:
            result = load(file)

        new = []
        driver = webdriver.Chrome()
        for url in urls:
            new += news.load_from_url(driver, url)
        driver.quit()
        
        for n in new:
            description = [c for c in n.text.replace("\t", "").splitlines() if c != '']
            date = [d for d in description if d[:3] == '202' and d[4] == '.']
            if (len(date) == 0): continue
            date = date[0]
            description = {
                "title":description[1],
                "author":description[3],
                "date":date
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