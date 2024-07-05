import sqlite3

class Database:
    
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()


    # Example create func
    async def reg_user(self, user_name, tgid, date_reg):
        with self.connection:
            self.cursor.execute('INSERT OR IGNORE INTO `start_registration` (`user_name`, `tgid`, `date_reg`) VALUES (?, ?, ?)', (user_name, tgid, date_reg))


    async def check_exist_spreadsheet(self, tgid):
        with self.connection:
            res = self.cursor.execute('SELECT `spreadsheet_id` FROM `spreadsheets` WHERE tgid=?', (tgid, )).fetchone()
            if res is None:
                return False
            else:
                return True

    async def add_spreadsheet(self, tgid, spreadsheet_id):
        with self.connection:
            self.cursor.execute('INSERT INTO `spreadsheets` (`tgid`, `spreadsheet_id`) VALUES(?, ?)', (tgid, spreadsheet_id, ))


    async def delete_spreadsheet(self, tgid):
        with self.connection:
            self.cursor.execute('DELETE FROM `spreadsheets` WHERE tgid=?', (tgid, ))


    async def get_spreadsheetid(self, tgid):
        with self.connection:
            return self.cursor.execute('SELECT `spreadsheet_id` FROM `spreadsheets` WHERE tgid=?', (tgid, )).fetchone()


    async def set_status_errors(self, tgid):
        with self.connection:
            self.cursor.execute('INSERT OR IGNORE INTO `status_errors` (`tgid`, `status`) VALUES(?, ?)', (tgid, 1))


    def update_status_errors(self, tgid, status):
        with self.connection:
            self.cursor.execute('UPDATE `status_errors` SET status=? WHERE tgid=?', (status, tgid))


    async def get_status_errors(self, tgid):
        with self.connection:
            res = self.cursor.execute('SELECT `status` FROM `status_errors` WHERE tgid=?', (tgid, )).fetchone()
            return res[0]

    # При старте, 0 - свободен
    async def set_parsing_status(self, tgid):
        with self.connection:
            self.cursor.execute('INSERT OR IGNORE INTO `parsing_status` (`tgid`, `status`) VALUES(?, ?)', (tgid, 0))


    def update_parsing_status(self, tgid, status):
        with self.connection:
            self.cursor.execute('UPDATE `parsing_status` SET status=? WHERE tgid=?', (status, tgid))


    async def get_parsing_status(self, tgid):
        with self.connection:
            res = self.cursor.execute('SELECT `status` FROM `parsing_status` WHERE tgid=?', (tgid, )).fetchone()
            return res[0]




    async def set_schedule_status(self, tgid):
        with self.connection:
            self.cursor.execute('INSERT OR IGNORE INTO `cancel_parsing` (`tgid`, `status`) VALUES(?, ?)', (tgid, 'inactive'))


    async def update_schedule_status(self, tgid, status):
        with self.connection:
            self.cursor.execute('UPDATE `cancel_parsing` SET status=? WHERE tgid=?', (status, tgid))


    async def get_schedule_status(self, tgid):
        with self.connection:
            return self.cursor.execute('SELECT `status` FROM `cancel_parsing` WHERE tgid=?', (tgid, )).fetchone()

#cancel_parsing
#-status
#-tgid

#parsing_status
#-status
#-tgid

#status_errors
#-status
#-tgid

#spreadsheets
#-spreadsheet_id
#-tgid

#start_registration
#-user_name
#-tgid
#-date_reg