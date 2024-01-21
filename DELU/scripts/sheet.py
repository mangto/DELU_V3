from oauth2client.service_account import ServiceAccountCredentials
from gspread import authorize
from json import dump

class spreadsheet:
    url = "https://docs.google.com/spreadsheets/d/1nDwQApT_rR60JZI5XXNCxC8_9O-Vn3l-NzxFFk6lPNE"
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('.\\DELU\\data\\fourth-cirrus-301609-ed9b67be5c94.json', scope)
    gc = authorize(credentials)
    sheet = gc.open_by_url(url).worksheet('일정')


    def load_dict():
        try: 
            date = spreadsheet.sheet.col_values(1)
            works = spreadsheet.sheet.col_values(2)
            result = {}
            for i, work in enumerate(works[1:]):
                if (result.get(date[i+1]) == None): result[date[i+1]] :list = [work]
                else: result[date[i+1]].append(work)
            return result
        except Exception as e:
            print(e)
            return spreadsheet.load_dict()
            
    def update(save=True):
        file :dict = {}
        sheet_data = spreadsheet.load_dict()

        for day in sheet_data:
            daily = file.get(day)
            if (daily == None): file[day] = sheet_data[day]
            else:
                for description in sheet_data[day]:
                    if (description not in file[day]): file[day].append(description)

        if (save): dump(file, open(".\\DELU\\data\\sheet.json", 'w', encoding='utf8'), indent="\t", ensure_ascii=False)

        return file