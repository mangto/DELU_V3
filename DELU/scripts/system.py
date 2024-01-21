import DELU.scripts.meal as meal
from DELU.scripts.news import news
from DELU.scripts.logger import logger
from DELU.scripts.sheet import spreadsheet
from DELU.scripts.bot import bot
from DELU.scripts.server import *

from threading import Thread
import time, sys

class system:

    logger = logger()

    def __init__(self, rooms:list[str]=[]) -> None:
        
        for room in rooms: bot(str(room))

        Thread(target=start).start()

        pass

    def refresh() -> None:
        meal.save()
        news.load()
        spreadsheet.update()
        return