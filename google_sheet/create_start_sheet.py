from google_sheet.Spreadsheet import Spreadsheet
import googleapiclient.errors


# Database
from database.sqlite_db import Database


# PATH
from pathlib import Path



# COLOR
def create_start_sheet(GOOGLE_CREDENTIALS_FILE, spreadsheetId, tgid, debugMode=False):
    dir_path = str(Path.cwd())
    path_to_db = str(Path(dir_path, 'google_parser.db'))
    db = Database(path_to_db)
    try:
        def htmlColorToJSON(htmlColor):
            if htmlColor.startswith("#"):
                htmlColor = htmlColor[1:]
            return {"red": int(htmlColor[0:2], 16) / 255.0, "green": int(htmlColor[2:4], 16) / 255.0,
                    "blue": int(htmlColor[4:6], 16) / 255.0}



        sheetTitle = "Товары"


        header = [['Название', 'Текущая цена', 'Обычная цена', 'Ссылка на картинку', 'Категория']]


        rowCount = 100000


        # CREATING AN INSTANCE OF A CLASS
        ss = Spreadsheet(GOOGLE_CREDENTIALS_FILE, spreadsheetId, debugMode=debugMode)

        # ADDING A NEW SHEET
        ss.addSheet(sheetTitle, rows=rowCount + 3, cols=8)

        # EDITING SIZE CELL
        ss.prepare_setRowHeight(0, 40)
        ss.prepare_setRowsHeight(0, rowCount+3, 40)
        ss.prepare_setColumnWidth(2, 200)
        ss.prepare_setColumnWidth(1, 200)
        ss.prepare_setColumnWidth(3, 200)
        ss.prepare_setColumnWidth(4, 150)


        # FORMATTING TEXT
        ss.prepare_setCellsFormat("A1:E1", {'backgroundColor': htmlColorToJSON('#9988DD'), "textFormat": {"fontSize": 11, 'bold': True, "fontFamily": "Comfortaa"},  "horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE"})


        columns_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        # HEADER BORDERS
        i = 0
        while i != 5:
            ss.prepare_setBorders(f'{columns_list[i]}1:{columns_list[i]}1', 5, '#000000')
            i += 1


        # START TASK
        ss.rename_Spreadsheet('Данные')            # --> переименование
        list_id = ss.get_sheet_id(0)               # id листа
        ss.deleteSheet(int(list_id))               # удаление листа по id



        # INSERT VALUES
        sheet_title = ss.get_sheet_title(0)

        ss.prepare_setValues("A1:E1", header, sheet_title)

        ss.runPrepared()

        db.update_status_errors(tgid, 1)
    except googleapiclient.errors.HttpError:
        db.update_status_errors(tgid, 0)


