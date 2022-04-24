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
    
    def close(self):
        self.dbCon.close()
    
    def isExistPart(self, cur: sqlite3.Cursor, partNo: int) -> bool:
        if partNo < 1 or partNo > 5: return False

        return bool(cur.execute(
            'SELECT 1 FROM TremENDous'
            'WHERE partNo=:partNo',
            { 'partNo': partNo }
        ).fetchone())
    
    def editTime(self, partNo: int, newTime: int):
        with self.dbCon as cur:
            if self.isExistPart(cur, partNo):
                raise NotExistPart(partNo)
            
            cur.execute(
                'UPDATE TremENDous'
                'SET time=:time'
                'WHERE partNo=:partNo',
                { 'time': value, 'partNo': partNo }
            )
    
    def editChart(self, partNo: int, newMemberID: int):
        with self.dbCon as cur:
            if self.isExistPart(cur, partNo):
                raise NotExistPart(partNo)
            
            cur.execute(
                'UPDATE TremENDous'
                'SET track=:track, trackSubmit=0'
                'WHERE partNo=:partNo',
                { 'track': newMemberID, 'partNo': partNo }
            )
    
    def editVFX(self, partNo: int, newMemberID: int):
        with self.dbCon as cur:
            if self.isExistPart(cur, partNo):
                raise NotExistPart(partNo)
            
            cur.execute(
                'UPDATE TremENDous'
                'SET vfx=:vfx, vfxSubmit=0'
                'WHERE partNo=:partNo',
                { 'vfx': newMemberID, 'partNo': partNo }
            )
    
    def chartSubmit(self, partNo: int):
        with self.dbCon as cur:
            if self.isExistPart(cur, partNo):
                raise NotExistPart(partNo)
            
            cur.execute(
                'UPDATE TremENDous'
                'SET chartSubmit=1'
                'WHERE partNo=:partNo',
                { 'partNo': partNo }
            )
    
    def vfxSubmit(self, partNo: int):
        with self.dbCon as cur:
            if self.isExistPart(cur, partNo):
                raise NotExistPart(partNo)
            
            cur.execute(
                'UPDATE TremENDous'
                'SET vfxSubmit=1'
                'WHERE partNo=:partNo',
                { 'partNo': partNo }
            )

db = DB()
