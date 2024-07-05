from google_sheet.Spreadsheet import Spreadsheet
from google_sheet.parser_module import get_ids, get_data


import time

def insert_values(cred, spreadsheetId, page, category_user, tgid, debugMode=False):

    ss = Spreadsheet(cred, spreadsheetId, debugMode=debugMode)

    sheet_title = ss.get_sheet_title(0)

    def htmlColorToJSON(htmlColor):
        if htmlColor.startswith("#"):
            htmlColor = htmlColor[1:]
        return {"red": int(htmlColor[0:2], 16) / 255.0, "green": int(htmlColor[2:4], 16) / 255.0,
                "blue": int(htmlColor[4:6], 16) / 255.0}
    # INSERT VALUES
    for i in get_data(get_ids(page, category_user), page, category_user, tgid):
        read_spreadsheet = ss.service.spreadsheets().values().get(spreadsheetId=spreadsheetId,
                                                                  range=f"{sheet_title}!A1:E").execute()


        count_rows = len(read_spreadsheet['values'])

        # COORDINATES
        next_row = count_rows+1
        next_coord = f'A{next_row}:E{next_row}'




        value = [[i[0], i[1], i[2], i[3], i[4]]]
        ss.prepare_setValues(next_coord, value, sheet_title)
        ss.runPrepared()



        # FORMATTING
        ss.prepare_setCellsFormat(next_coord, {"textFormat": {"fontSize": 12, 'bold': True, "fontFamily": "Comfortaa"}, "horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE"})
        ss.runPrepared()




        # BORDERS
        column_list = ['A', 'B', 'C', 'D', 'E']

        for i in column_list:
            border_cord = f'{i}{next_row}:{i}{next_row}'
            ss.prepare_setBorders(border_cord, 5, '#000000')
            ss.runPrepared()
        time.sleep(5)







