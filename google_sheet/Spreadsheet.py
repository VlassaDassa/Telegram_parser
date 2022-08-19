from pprint import pprint
import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials



# COLOR
def htmlColorToJSON(htmlColor):
    if htmlColor.startswith("#"):
        htmlColor = htmlColor[1:]
    return {"red": int(htmlColor[0:2], 16) / 255.0, "green": int(htmlColor[2:4], 16) / 255.0,
            "blue": int(htmlColor[4:6], 16) / 255.0}




# ERRORS
class SpreadsheetError(Exception):
    pass

class SpreadsheetNotSetError(SpreadsheetError):
    pass

class SheetNotSetError(SpreadsheetError):
    pass




class Spreadsheet:

    def __init__(self, jsonKeyFileName, spreadsheetId, debugMode = False):
        self.debugMode = debugMode
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonKeyFileName, ['https://www.googleapis.com/auth/spreadsheets',
                                                                                              'https://www.googleapis.com/auth/drive'])
        self.httpAuth = self.credentials.authorize(httplib2.Http())
        self.service = googleapiclient.discovery.build('sheets', 'v4', http = self.httpAuth)
        self.driveService = None  # Needed only for sharing
        self.spreadsheetId = spreadsheetId
        self.sheetId = None
        self.sheetTitle = None
        self.requests = []
        self.valueRanges = []





    # SET CURRENT SHEET AS FIRST OF THIS SPREADSHEET
    def setSpreadsheetById(self, spreadsheetId):
        spreadsheet = self.service.spreadsheets().get(spreadsheetId = spreadsheetId).execute()
        if self.debugMode:
            pprint(spreadsheet)
        self.spreadsheetId = spreadsheet['spreadsheetId']
        self.sheetId = spreadsheet['sheets'][0]['properties']['sheetId']
        self.sheetTitle = spreadsheet['sheets'][0]['properties']['title']





    # RUN PREPARED
    def runPrepared(self, valueInputOption = "USER_ENTERED"):
        if self.spreadsheetId is None:
            raise SpreadsheetNotSetError()
        upd1Res = {'replies': []}
        upd2Res = {'responses': []}
        try:
            if len(self.requests) > 0:
                upd1Res = self.service.spreadsheets().batchUpdate(spreadsheetId = self.spreadsheetId, body = {"requests": self.requests}).execute()
                if self.debugMode:
                    pprint(upd1Res)
            if len(self.valueRanges) > 0:
                upd2Res = self.service.spreadsheets().values().batchUpdate(spreadsheetId = self.spreadsheetId, body = {"valueInputOption": valueInputOption,
                                                                                                                       "data": self.valueRanges}).execute()
                if self.debugMode:
                    pprint(upd2Res)
        finally:
            self.requests = []
            self.valueRanges = []
        return (upd1Res['replies'], upd2Res['responses'])





    # PREPARE ADD NEW_SHEET
    def prepare_addSheet(self, sheetTitle, rows = 1000, cols = 26):
        self.requests.append({"addSheet": {"properties": {"title": sheetTitle, 'gridProperties': {'rowCount': rows, 'columnCount': cols}}}})

    # ADD NEW SHEET
    def addSheet(self, sheetTitle, rows = 1000, cols = 26):
        if self.spreadsheetId is None:
            raise SpreadsheetNotSetError()
        self.prepare_addSheet(sheetTitle, rows, cols)
        sheet = self.runPrepared()

        addedSheet = sheet[0][0]['addSheet']['properties']
        self.sheetId = addedSheet['sheetId']
        self.sheetTitle = addedSheet['title']
        return self.sheetId




    # RENAME SPREADSHEET
    def rename_Spreadsheet(self, new_name):
        if self.spreadsheetId is None:
            raise SpreadsheetNotSetError()

        if self.driveService is None:
            self.driveService = googleapiclient.discovery.build('drive', 'v3', http = self.httpAuth)

            body = {"name": new_name}

            self.driveService.files().update(fileId=self.spreadsheetId, body=body).execute()





    # DELETE SHEET
    def deleteSheet(self, list_id):
        if self.spreadsheetId is None:
            raise SpreadsheetNotSetError()

        request_body = {
            'requests': [
                {
                    'deleteSheet': {
                        'sheetId': list_id
                    }
                }
            ]

        }

        self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId, body=request_body).execute()





    # RETURN'S SHEET ID
    def get_sheet_id(self, index_list):
        if self.spreadsheetId is None:
            raise SpreadsheetNotSetError()

        sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.spreadsheetId).execute()
        sheets = sheet_metadata.get('sheets', '')                                               # --> все листы (получится список)
        sheet_id = sheets[index_list].get("properties", {}).get("sheetId", index_list)            # --> собственно, id
        return sheet_id





    # RETURN'S SHEET TITLE
    def get_sheet_title(self, index_list):
        if self.spreadsheetId is None:
            raise SpreadsheetNotSetError()

        sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.spreadsheetId).execute()
        sheets = sheet_metadata.get('sheets', '')
        sheet_title = sheets[index_list].get('properties', {}).get('sheetTitle', '')
        return sheet_title





    # CONVERTS FROM 'A-Z' IN '1,2,3...'
    def toGridRange(self, cellsRange):
        if isinstance(cellsRange, str):
            startCell, endCell = cellsRange.split(":")[0:2]
            cellsRange = {}
            rangeAZ = range(ord('A'), ord('Z') + 1)
            if ord(startCell[0]) in rangeAZ:
                cellsRange["startColumnIndex"] = ord(startCell[0]) - ord('A')
                startCell = startCell[1:]
            if ord(endCell[0]) in rangeAZ:
                cellsRange["endColumnIndex"] = ord(endCell[0]) - ord('A') + 1
                endCell = endCell[1:]
            if len(startCell) > 0:
                cellsRange["startRowIndex"] = int(startCell) - 1
            if len(endCell) > 0:
                cellsRange["endRowIndex"] = int(endCell)

        if self.sheetId is None:
            cellsRange["sheetId"] = self.get_sheet_id(0)
            return cellsRange

        cellsRange["sheetId"] = self.sheetId

        return cellsRange





    # SET BORDERS
    def prepare_setBorders(self, cellsRange, width, color, type='SOLID' ):

        self.requests.append({"updateBorders": {
            "range": self.toGridRange(cellsRange),
            "bottom": {"style": type, "width": width, "color": htmlColorToJSON(color)},
            "top": {"style": type, "width": width, "color": htmlColorToJSON(color)},
            "left": {"style": type, "width": width, "color": htmlColorToJSON(color)},
            "right": {"style": type, "width": width, "color": htmlColorToJSON(color)}}})




    # PREPARE SIZE
    def prepare_setDimensionPixelSize(self, dimension, startIndex, endIndex, pixelSize):
        if self.sheetId is None:
            raise SheetNotSetError()
        self.requests.append({"updateDimensionProperties": {
            "range": {"sheetId": self.sheetId,
                      "dimension": dimension,
                      "startIndex": startIndex,
                      "endIndex": endIndex},
            "properties": {"pixelSize": pixelSize},
            "fields": "pixelSize"}})


    def prepare_setColumnsWidth(self, startCol, endCol, width):
        self.prepare_setDimensionPixelSize("COLUMNS", startCol, endCol + 1, width)

    def prepare_setColumnWidth(self, col, width):
        self.prepare_setColumnsWidth(col, col, width)

    def prepare_setRowsHeight(self, startRow, endRow, height):
        self.prepare_setDimensionPixelSize("ROWS", startRow, endRow + 1, height)

    def prepare_setRowHeight(self, row, height):
        self.prepare_setRowsHeight(row, row, height)





    # SET VALUES
    def prepare_setValues(self, cellsRange, values, sheetTitle, majorDimension = "ROWS"):
        if sheetTitle is None:
            raise SheetNotSetError()

        self.valueRanges.append({"range": sheetTitle + "!" + cellsRange, "majorDimension": majorDimension, "values": values})





    # MERGE
    def prepare_mergeCells(self, cellsRange, mergeType = "MERGE_ALL"):
        self.requests.append({"mergeCells": {"range": self.toGridRange(cellsRange), "mergeType": mergeType}})





    # FORMAT
    def prepare_setCellsFormat(self, cellsRange, formatJSON, fields = "userEnteredFormat"):
        self.requests.append({"repeatCell": {"range": self.toGridRange(cellsRange), "cell": {"userEnteredFormat": formatJSON}, "fields": fields}})


    def prepare_setCellsFormats(self, cellsRange, formatsJSON, fields = "userEnteredFormat"):
        self.requests.append({"updateCells": {"range": self.toGridRange(cellsRange),
                                              "rows": [{"values": [{"userEnteredFormat": cellFormat} for cellFormat in rowFormats]} for rowFormats in formatsJSON],
                                              "fields": fields}})



