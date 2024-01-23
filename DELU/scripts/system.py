import DELU.scripts.meal as meal
from DELU.scripts.news import news
from DELU.scripts.logger import logger
from DELU.scripts.sheet import spreadsheet
from DELU.scripts.bot import bot
from DELU.scripts.server import *

from threading import Thread
from multiprocessing import Process
import time
from oauth2client.service_account import ServiceAccountCredentials
from gspread import authorize
from json import dump, load

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('.\\DELU\\data\\fourth-cirrus-301609-ed9b67be5c94.json', scope)
gc = authorize(credentials)
with open(".\\DELU\\data\\sheetlinks.json", "r", encoding="utf8") as file: urls = load(file)

class system:

    logger = logger()
    UpdateCycle = 5 * 60 # update every FIVE minute
    LastUpdate = time.time() - UpdateCycle

    def __init__(self, rooms:list[str]=[]) -> None:
        
        for room in rooms: bot(str(room))

        Thread(target=start).start()

        pass
    
    def auto_refresher_no_multiprocessing() -> None:
        sheets = {key:gc.open_by_url(urls[key]).worksheet('일정') for key in urls}
        while True:
            current = time.time()

            if (current - system.LastUpdate < system.UpdateCycle): 
                time.sleep(1)
                continue

            meal.save()
            news.load()
            spreadsheet.update(sheets)
            system.LastUpdate = current
        
    def auto_refresher() -> None:
        p = Process(target = system.auto_refresher_no_multiprocessing)
        p.start()