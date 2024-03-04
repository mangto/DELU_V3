from datetime import datetime, date
import DELU.scripts.meal as meal
from DELU.scripts.news import news

from json import load

class FME:
    def edit(string:str) -> str:

        string = string.replace("\\n", "\n")
        lines = string.splitlines()
        string = []
        kwargs = {}
        for line in lines:
            if (not line.startswith("#define ") or line.count("=") != 1):
                string.append(line)
                continue
            line = line[8:].replace(" ", "")
            name, value = line.split("=")
            kwargs[name] = value
        string = "\n".join(string)


        # find FME contents
        tokens = string.split("///")

        for i, token in enumerate(tokens):

            if (token.startswith("FME:") == False): continue

            contents = token.split(":")
            if (len(contents) < 2): continue

            TYPE = contents[1].lower()
            ARGUMENT = []
            if (len(contents) >= 3): ARGUMENT = contents[2:]

            match TYPE:
                case 'meal': func = FME.functions.meal
                case 'time': func = FME.functions.time
                case 'date': func = FME.functions.date
                case 'dday': func = FME.functions.dday
                case 'news': func = FME.functions.news
                case 'sheet': func = FME.functions.sheet
                case 'schedule': func = FME.functions.schedule
                case _: func = FME.functions.dummy
            
            tokens[i] = func(ARGUMENT, kwargs=kwargs)

            continue
        
        string = ''.join(tokens)
        
        return string
    


    class functions:
        def dummy(arg:list, kwargs:dict={}) -> str:
            return "[UNKNOWN FME]"
        
        def schedule(arg:list, kwargs:dict={}) -> str:
            room = arg[0]
            with open(".\\DELU\\data\\schedule.json", "r", encoding="utf8") as file:
                schedule = load(file)
            if room not in schedule: return "FME Error: Unknown Class ID"

            weekday = datetime.now().weekday()

            return schedule[room][weekday]
        
        def news(arg:list, kwargs:dict={}) -> str:
            new = news.load_from_file()
            threshold = 7 if len(arg) == 0 else int(arg[0])
            current = datetime.now().date()


            result = {}

            for info in new:
                time = info.get("date", None)

                if (time == None): continue

                target = time.split('.')
                target = date(int(target[0]), int(target[1]), int(target[2]))
                diff = current - target

                if (diff.days > threshold): continue

                author = info.get("author", "익명")
                text = info.get("title", "알 수 없는 내용")
                
                if (time not in result): result[time] = ["  • " + text]
                else: result[time].append("  • " + text)
            
            if (len(result) == 0): return "새로운 공지사항이 없습니다!"

            result = sorted(result.items(), key=lambda x:x[0], reverse=True)
            text = ""
            
            for i, d in enumerate(result):
                if (i > 0): text += "\n"
                infos = d[1]
                d = d[0]
                d = d[d.find(".")+1:]
                text += " [" + d + "]\n"
                text += "\n".join(infos)

            return text
        
        def sheet(arg:list, kwargs:dict={}) -> str:
            room = arg[0]
            
            with open(".\\DELU\\data\\sheet.json", "r", encoding="utf8") as file:
                sheet = load(file)
            
            if (room not in sheet): return "FME Error: Unknown Class ID"

            data = sheet.get(room, {})

            notions = []

            for d in data:
                current = datetime.now().date()
                tags = ['2024'] + d.split("/")
                year = int(tags[0])
                month = int(tags[1])
                day = int(tags[2])
                target = date(year, month, day)
                diff = target-current

                if (diff.days < 10):
                    titles = '\n  • '+ '\n  • '.join(data[d])
                    d = d.split("/")
                    month = d[0] if len(d[0]) == 2 else "0"+d[0]
                    day = d[1] if len(d[1]) == 2 else "0"+d[1]
                    notions.append(f" [{month}.{day}]{titles}")

                continue


            return "\n".join(notions)

        def dday(arg:list, kwargs:dict={}) -> str:
            current = datetime.now().date()
            tags = arg[0].split("/")
            year = int(tags[0])
            month = int(tags[1])
            day = int(tags[2])

            target = date(year, month, day)
            diff = target-current

            return f"D-{diff.days}일"

        def date(arg:list, kwargs:dict={}) -> str:
            today = datetime.now()
            date = f"{today.month}월 {today.day}일"
            
            return date
        
        def meal(arg:list, kwargs:dict={}) -> str:
            date:str
            if (len(arg) == 0): date = "today"
            else: date = arg[0]
            if (date == "today"):
                today = datetime.now()
                date = f"{today.month}/{today.day}"
            

            return meal.load(date, True)

        def time(arg:list, kwargs:dict={}) -> str:
            return str(datetime.now())