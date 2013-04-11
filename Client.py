#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import datetime
import json
from math import ceil
from PyMeld import Meld
import pgdb as PgSQL      
from HtmlGen import HtmlGen

class Client:
    dbName = 'client'
    def __init__(self, userName = None , userPassword = None):
        self.accountNum = None
        self.conn = None
        self.dbName = dbName
        self.userName = userName
        self.userPassword = userPassword
        self.providerIdList = [] 

    def pg_connect(self):
        """
        Подключение к базе данных
        """
        try:
            connString = 'localhost:' + self.dbName + ':' + self.userName + ':' + self.userPassword
            self.conn=PgSQL.connect(connString)
            return True
        except:
            self.conn=None
            return False

    def __del__(self):
        if not self.conn is None:
            self.conn.close()

    def findClient(self, accountNum = None):
        #.....
        #.....
        queryStr = "SELECT accNum, hId, bId FROM clients WHERE accNum = " %(accountNum)
        query = self.query(queryStr) 
        bClientsId = [item["bid"] for item in filter(lambda x: x['bid'] is not None, [row for row in query]) ]
        hClientsId = [item["hid"] for item in filter(lambda x: x['hid'] is not None, [row for row in query]) ]

        if len(hClientsId) > 0:    # Физические лица
            if len(hClientsId) == 1 :
                hClientsId = '(' + str(hClientsId[0]) + ')' 
            else:
                hClientsId = str(tuple(hClientsId))
            queryStr = "SELECT fam, im, otch, dogovor_n, to_char(dogovor_data, 'DD-MM-YYYY') "\
                "AS dogovor_data , tarifdescr.descr AS tarifdescr , accNum, "\
                "FROM hClients, tarifdescr WHERE accNum IN %s "\
                "ORDER BY fam" %(hClientsId)
            queryH = self.query(queryStr)
        else:
            queryH = []

        if len(bClientsId) > 0:   # Юридические лица
            if len(bClientsId) == 1 :
                bClientsId = '(' + str(bClientsId[0]) + ')'
            else:
                bClientsId = str(tuple(bClientsId))
            queryStr = "SELECT bclients.descr AS descr, addres, inn, kpp, contractNum, to_char(contractDate, 'DD-MM-YYYY') "\
                "AS contractdate , tarifdescr.descr AS tarifdescr , accNum FROM bClients, tarifdescr WHERE "\
                "accNum IN %s ORDER BY descr" %(bClientsId)
            queryB = self.query(queryStr)
        else:
            queryB = []
        #...................

    def query(self, queryString, resultType='dict'):
        cursor = self.conn.cursor()
        cursor.execute(queryString) 
        result = cursor.fetchall()
        if resultType is None or resultType == 'tuple':
            return result      
        else:                  
            resultList = []
            cursorColumns = []
            for fieldName in cursor.description:
                cursorColumns.append(fieldName[0])
            for record in result:
                recordDict = {}
                for colNum in range(0, len(record)):
                    recordDict[cursorColumns[colNum]] = record[colNum]
                resultList.append(recordDict)
            return resultList 

    def execQuery(self, queryString):
        try:
            if not self.cursor:
                self.cursor = self.conn.cursor()
            action = queryString.split()[0]
            self.cursor.execute(queryString)
            if action == "SELECT":
                self.cursor.fetchone()
                cAction = "Найдено "
            elif action == "UPDATE":
                cAction = "Обновлено  "
            elif action == "DELETE":
                cAction = "Удалено  "
            elif action == "INSERT":
                cAction = "Добавлено "
            else:
                cAction = None
            if cAction:
                print cAction, self.cursor.rowcount, ' записей.'
            return self.cursor.rowcount
        except:
            return -1
        
    # ...........
