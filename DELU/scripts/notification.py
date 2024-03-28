from datetime import datetime
from DELU.scripts.logger import logger
from json import load, dump

class notification:
    with open(".\\DELU\\data\\notification_history.json", "r", encoding="utf8") as file:
        notification_history = load(file)
    logger = logger()


    def check(info:dict, CurrentTime:datetime, room:str) -> bool:

        try:
            
            tag = info.get("tag", "") + "|" + room
            time = info.get("time", None)
            weekday = info.get("weekday", None)

            if (type(time) != str): # time info must be "hour:minute" format
                notification.logger.write("No Time Info", "NOTIFICATION ERROR")
                return "No Time Info"
            if (not weekday): weekday = list(range(6)) # if weekday is [] or None or 0 -> set weekday to [0, 1, 2, 3, 4, 5, 6] 

            if (CurrentTime.weekday() not in weekday): return False

            sptime = time.split(":") # splited time
            if (len(sptime) != 2): # time info must be "hour:minute" format
                notification.logger.write(f"Invalid Time Info:{time}", "NOTIFICATION ERROR")
                return False

            
            try:  # convert time info to inteager
                hour = int(sptime[0])
                minute = int(sptime[1])

            except ValueError:
                notification.logger.write(f"Invalid Time Info:{time}", "NOTIFICATION ERROR")
                return False
            
            if (CurrentTime.hour != hour or CurrentTime.minute != minute): return False # check time

            timetag = f"{CurrentTime.year}/{CurrentTime.month}/{CurrentTime.day}"
            today_history = notification.notification_history.get(timetag, [])

            if (tag not in today_history):
                print("!")

                if (timetag not in notification.notification_history):  notification.notification_history[timetag] = [tag]
                else: notification.notification_history[timetag].append(tag)

                with open(".\\DELU\\data\\notification_history.json", "w", encoding="utf8") as file:
                    dump(notification.notification_history, file, indent="\t", ensure_ascii=False)

                return True
            

            return False
        
        except Exception as e:

            notification.logger.write(str(e), "NOTIFICATION ERROR")
            return False