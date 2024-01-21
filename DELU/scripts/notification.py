
class notification:

    def check(info:dict) -> bool|str:
        time = info.get("time", None)
        weekday = info.get("weekday", None)

        if (time == None): return "No Time Info"

        



        return