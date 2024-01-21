from DELU.scripts.basicfunc import open_chatroom, send_text, PostKeyEx, SendReturn, copy_chatroom
from DELU.scripts.bot import bot
from DELU.scripts.FME import FME
from DELU.scripts.logger import logger
import DELU.scripts.meal as meal
from DELU.scripts.news import news
from DELU.scripts.system import system
from DELU.scripts.sheet import spreadsheet
from DELU.scripts.server import *
from DELU.scripts.controller import *

__all__ = [
    "open_chatroom", "send_text", "PostKeyEx", "SendReturn", "copy_chatroom",
    "bot",
    "FME",
    "logger",
    "meal",
    "news",
    "system",
    "spreadsheet",
]

# =========================================================

GREETING :str
with open(".\\DELU\\greeting.txt", "r", encoding="utf8") as file:
    GREETING = file.read()
print(GREETING)