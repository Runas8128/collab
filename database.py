from typing import Union
import sqlite3

from error import NotExistPart

class DBCon:
    def __init__(self):
        self.con = sqlite3.connect('.db')
    
    def __enter__(self):
        return self.con.cursor()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.commit()
    
    def close(self):
        self.con.close()

class DB:
    def __init__(self):
        self.dbCon = DBCon()
        with self.dbCon as cur:
            cur.execute(
                '''CREATE TABLE IF NOT EXISTS TremENDous (
                    partNo INTEGER PRIMARY KEY,
                    time TEXT,
                    chart INTEGER, chartSubmit INTEGER,
                    vfx INTEGER, vfxSubmit INTEGER
                )'''
            )
            cur.execute(
                '''CREATE TABLE IF NOT EXISTS ProgMsgID (
                    ID INTEGER PRIMARY KEY
                )'''
            )
    
    def init(self):
        with self.dbCon as cur:
            cur.executemany(
                "INSERT INTO TremENDous values (?, ?, 0, -1, 0, -1)", [
                    (1, '0:00 ~ 1:40'),
                    (2, '1:40 ~ 3:13'),
                    (3, '3:13 ~ 4:32'),
                    (4, '4:32 ~ 6:00'),
                    (5, '6:00 ~ 7:25'),
                ]
            )
    
    def setProgMsgID(self, newID: int):
        with self.dbCon as cur:
            if cur.execute('SELECT 1 FROM ProgMsgID').fetchone():
                cur.execute("UPDATE ProgMsgID SET ID = :newID", {'newID': newID})
            else:
                cur.execute("INSERT INTO ProgMsgID VALUES (:newID)", {'newID': newID})
    
    def getProgMsgID(self) -> int:
        with self.dbCon as cur:
            rst = cur.execute('SELECT 1 FROM ProgMsgID').fetchone()
            return rst[0] if rst else 0

    def close(self):
        self.dbCon.close()
    
    def getData(self):
        with self.dbCon as cur:
            return cur.execute(
                'SELECT * FROM TremENDous'
            ).fetchall()
    
    def isExistPart(self, cur: sqlite3.Cursor, partNo: int) -> bool:
        return bool(cur.execute(
            'SELECT 1 FROM TremENDous'
            'WHERE partNo = :partNo',
            { 'partNo': partNo }
        ).fetchone())
    
    def editTime(self, partNo: int, newTime: int):
        with self.dbCon as cur:
            if self.isExistPart(cur, partNo):
                raise NotExistPart(partNo)
            
            cur.execute(
                'UPDATE TremENDous'
                'SET time = :time'
                'WHERE partNo = :partNo',
                { 'time': value, 'partNo': partNo }
            )
    
    def editChart(self, partNo: int, newMemberID: int):
        with self.dbCon as cur:
            if self.isExistPart(cur, partNo):
                raise NotExistPart(partNo)
            
            cur.execute(
                'UPDATE TremENDous'
                'SET track = :track, trackSubmit = 0'
                'WHERE partNo = :partNo',
                { 'track': newMemberID, 'partNo': partNo }
            )
    
    def editVFX(self, partNo: int, newMemberID: int):
        with self.dbCon as cur:
            if self.isExistPart(cur, partNo):
                raise NotExistPart(partNo)
            
            cur.execute(
                'UPDATE TremENDous'
                'SET vfx = :vfx, vfxSubmit = 0'
                'WHERE partNo = :partNo',
                { 'vfx': newMemberID, 'partNo': partNo }
            )
    
    def chartSubmit(self, partNo: int):
        with self.dbCon as cur:
            if self.isExistPart(cur, partNo):
                raise NotExistPart(partNo)
            
            cur.execute(
                'UPDATE TremENDous'
                'SET chartSubmit = 1'
                'WHERE partNo = :partNo',
                { 'partNo': partNo }
            )
    
    def vfxSubmit(self, partNo: int):
        with self.dbCon as cur:
            if self.isExistPart(cur, partNo):
                raise NotExistPart(partNo)
            
            cur.execute(
                'UPDATE TremENDous'
                'SET vfxSubmit = 1'
                'WHERE partNo = :partNo',
                { 'partNo': partNo }
            )
