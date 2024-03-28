from DELU.scripts.basicfunc import *
from DELU.scripts.FME import FME
from DELU.scripts.logger import logger
from DELU.scripts.notification import notification

from datetime import datetime
from threading import Thread
from uuid import uuid4
from os.path import isfile
from json import load
from time import sleep
import socket, sys


class bot:
    def __init__(self, room:str, lps:int=5, notification:str=".\\DELU\\data\\notification\\2-1.json") -> None:
        self.room = room
        self.uuid = str(uuid4())
        self.logger = logger()
        self.notification :list[dict] = None
        self.lps = lps
        self.lps_sleep = 1/lps

        self.logger.write(f"{self.uuid}:{self.room}", "BOT INITIALIZE")


        if (isfile(str(notification))):

            with open(notification, 'r', encoding='utf8') as file:
                self.notification = load(file)

            self.logger.write(f"{self.uuid}:loaded notification from {notification}", "NOTIFICATION LOAD")

        else:
            self.notification = []
            self.logger.write(f"{self.uuid}:failed loading notification from {notification}", "NOTIFICATION LOADING FAILED")

        Thread(target=self.loop).start()
        pass
        
    def loop(self):
        host = '127.0.0.1'
        port = 12345

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Login with an ID
        client_id = self.room
        client_socket.send(client_id.encode('utf-8'))
        client_socket.settimeout(self.lps_sleep)

        while True:
            try:

                # check notification
                current = datetime.now()
                for notion in self.notification:
                    if (not notification.check(notion, current, self.room)): continue
                    self.reply(notion.get("string", ""))


                # receive data

                data = client_socket.recv(1024)
                if not data:
                    continue

                message = data.decode('utf-8')
                
                self.reply(message)

            except TimeoutError: continue
            except Exception as e:
                print(f"Error receiving message: {e}")
                sys.exit()
                break

            # sleep(self.lps_sleep)

    def reply(self, string:str, room:str=None, EditMethod=FME.edit) -> bool:
        '''
        Send string:str to room:str with threading
         * string: str
         * room: str
         * EditMethod: function -> str
        
        Return: bool

         * If CHATROOM is None, Bot automatically sends message to self.room.
         * If EDITMODE is None, Bot doesn't edit message.
         * Bot automatically write log.
        '''
        t = Thread(target=self.send, args=(string, room, EditMethod))
        t.start()

        return

    def send(self, string:str, room:str=None, EditMethod=FME.edit) -> bool:
        try:
            if (EditMethod): string = str(EditMethod(string))
            if (room == None): room = self.room

            send_text(room, string)
            log = f"{self.uuid}:{self.room}:{string}"
            self.logger.write(log, "REPLY SUCCEED")
            return True
        
        except Exception as e:
            log = f"{self.uuid}:{self.room}:{string}"
            self.logger.write(log, "REPLY FAILED")
            self.logger.write(e, "EXCEPTION")
            return False