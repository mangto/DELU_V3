from json import dump



class spreadsheet:

    def update(Sheet:dict) -> None:
        sheets = {}

        for key in Sheet:
            sheet = Sheet[key]

            date = sheet.col_values(1)
            works = sheet.col_values(2)
            result = {}

            for i, work in enumerate(works[1:]):
                if (result.get(date[i+1]) == None): result[date[i+1]] = [work]
                else: result[date[i+1]].append(work)

            sheets[key] = result
        
        with open(".\\DELU\\data\\sheet.json", 'w', encoding='utf8') as file:
            dump(sheets, file, ensure_ascii=False, indent=4)

        return