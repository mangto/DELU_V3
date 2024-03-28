
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


url = "https://school.iamservice.net/organization/20019/group/2093903"

def get():
    driver = webdriver.Chrome()
    driver.get(url)
    bx_cont = [c.text for c in driver.find_elements(By.CLASS_NAME, 'bx_cont')]
    driver.quit()
    return bx_cont

def clean(meal:str) -> str:
    lines = meal.splitlines()

    caption = lines[0]
    foods = lines[1:]

    month = caption[:caption.find('월')]
    day = caption[caption.find('월 ')+2:caption.find('일')]
    key = f"{month}/{day}"

    result = []
    skip = False
    for food in foods:
        if (skip): continue
        if (food.startswith("상세페이지")): skip = True; continue
        if ("(" in food):

            index = food.rfind("(")
            next = food[index+1]
            if (next.isnumeric()): food = food[:index]

        food = "  • " + food
        result.append(food)

    result = "\n".join(result)

    return key, result

def save(Return=False):
    meals = get()
    meals = [clean(m) for m in meals]
    result = {pack[0]:pack[1] for pack in meals}

    with open(".\\DELU\\data\\meal.json", "w", encoding="utf8") as file:
        json.dump(result, file, indent="\t", ensure_ascii=False)

    if (Return): return result


def load(TimeInfo, update:bool=False, NoneMSG:str="급식이 없거나 오류가 발생했습니다", again=False):
    if (update): meal = save(True)
    else: meal = json.load(open(".\\DELU\\data\\meal.json", encoding='utf8'))
    
    food = meal.get(TimeInfo)

    if (food): return food
    else:
        if (again == False): return load(TimeInfo, True, again=True)
        else: return NoneMSG