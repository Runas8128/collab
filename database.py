import sqlite3

class DB:
    def __init__(self):
        self.con = sqlite3.connect('.db')
        cur = self.con.cursor()
        cur.execute(
            'CREATE TABLE if not exists'
            'TremENDous(partNo integer PRIMARY KEY, time text, chart integer, vfx integer)'
        )
        self.con.commit()
    
    def close(self):
        self.con.commit()
        self.con.close()
    
    def editPartTime(self, partNo: int, time: str):
        cur = self.con.cursor()
        cur.execute('SELECT ')
        self.con.commit()

db = DB()
