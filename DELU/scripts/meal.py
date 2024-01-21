from urllib.request import urlopen
from bs4 import BeautifulSoup
import re, json

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def clean(food):
    food = [f for f in food if f != '' and f != "TODAY"]

    title = f"{food[0]} [{food[1]}]"
    food_string = "  • " + "\n  • ".join([re.sub(r'[0-9.()]', '', f) for f in food[2:] if re.sub(r'[0-9.()]', '', f) != ""])
    
    TimeInfo = food[0].split(".")
    TimeInfo = f"{TimeInfo[0]}/{TimeInfo[1]}"

    return f"{food_string}", TimeInfo

def save(Return=False):
    current = json.load(open(".\\DELU\\data\\meal.json", encoding='utf8'))

    url="https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%B3%B4%EC%A0%95%EA%B3%A0%EB%93%B1%ED%95%99%EA%B5%90+%EA%B8%89%EC%8B%9D"
    req = urlopen(url)
    soup = BeautifulSoup(req, 'html.parser')
    foods = soup.find_all("div", "timeline_box")

    for food in foods:
        cleaned, TimeInfo = clean(food.text.split(" "))
        current[TimeInfo] = cleaned

    json.dump(current, open(".\\DELU\\data\\meal.json", 'w', encoding='utf8'), indent="\t", ensure_ascii=False)
    if (Return): return current

def load(TimeInfo, update:bool=False, NoneMSG:str="급식이 없거나 오류가 발생했습니다", again=False):
    if (update): meal = save(True)
    else: meal = json.load(open(".\\DELU\\data\\meal.json", encoding='utf8'))
    
    food = meal.get(TimeInfo)

    if (food): return food
    else:
        if (again == False): return load(TimeInfo, True, again=True)
        else: return NoneMSG