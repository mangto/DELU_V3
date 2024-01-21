from datetime import datetime

class logger:
    def __init__(self, file:str=".\\DELU\\log.txt") -> None:
        self.file = file
        pass

    def write(self, log:str, title:str="UNKNOWN") -> bool:
        log = str(log).replace("\n", "\\n")
        log = f"[{title}] [{datetime.now()}] {log}"

        with open(self.file, "a", encoding='utf8') as file:
            file.writelines("\n" + str(log))