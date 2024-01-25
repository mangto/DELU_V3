from datetime import datetime, date
import DELU.scripts.meal as meal
from DELU.scripts.news import news

class FME:
    def edit(string:str) -> str:

        # find FME contents
        tokens = string.split("///")

        for i, token in enumerate(tokens):

            if (token.startswith("FME:") == False): continue

            contents = token.split(":")
            if (len(contents) < 2): continue

            TYPE = contents[1].lower()
            ARGUMENT = []
            edited:str
            if (len(contents) >= 3): ARGUMENT = contents[2:]

            match TYPE:
                case 'meal': func = FME.functions.meal
                case 'time': func = FME.functions.time
                case 'date': func = FME.functions.date
                case 'dday': func = FME.functions.dday
                case 'news': func = FME.functions.news
                case _: func = FME.functions.dummy
            
            tokens[i] = func(ARGUMENT)

            continue
        
        string = ''.join(tokens)
        
        return string
    
    class functions:
        def dummy(arg:list) -> str:
            return "[UNKNOWN FME]"
        
        def news(arg:list) -> str:
            new = news.load_from_file()
            threshold = 7 if len(arg) == 0 else int(arg[0])
            current = datetime.now().date()
            result = []

            for info in new:
                time = info.get("date", None)

                if (time == None): continue

                target = time.split('.')
                target = date(int(target[0]), int(target[1]), int(target[2]))
                diff = current - target

                if (diff.days > threshold): continue

                author = info.get("author", "익명")
                text = info.get("title", "알 수 없는 내용")

                msg = f"[{time[time.find('.')+1:]}] {text}"
                result.append(msg)


            if (len(result) == 0): return "새로운 공지사항이 없습니다!"

            return '\n\n'.join(result)
        
        def dday(arg:list) -> str:
            current = datetime.now().date()
            tags = arg[0].split("/")
            year = int(tags[0])
            month = int(tags[1])
            day = int(tags[2])

            target = date(year, month, day)
            diff = target-current

            return f"D-{diff.days}일"

        def date(arg:list) -> str:
            today = datetime.now()
            date = f"{today.month}/{today.day}"
            
            return date
        
        def meal(arg:list) -> str:
            date:str
            if (len(arg) == 0): date = "today"
            else: date = arg[0]
            if (date == "today"):
                today = datetime.now()
                date = f"{today.month}/{today.day}"
            

            return meal.load(date, True)

        def time(arg:list) -> str:
            return str(datetime.now())