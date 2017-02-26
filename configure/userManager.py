# -*- coding: utf-8 -*-
'''
Created on 2016年5月7日

@author: imhey_000
'''

import config
import json
import csv

class UserManager(object):
    '''
    classdocs
    '''
    users = []
    userIds = []
    userNames = []
    fieldNames = ['userName', 'id']
    
    __CSVFile = config.USERS_CVS_FILE

    def __init__(self, csvFile=None):
        '''
        Constructor
        '''
        if csvFile != None:
            self.__CSVFile = csvFile
        
    def hasUser(self, user):
        if type(user) is str:
            userNames = self.getAllUserName()
            if userNames.__contains__(user):
                return True
        elif type(user) is int:
            userIds = self.getAllUserId()
            if userIds.__contains__(str(user)):
                return True
            
        return False
                
    def addUser(self, name):
        if self.hasUser(name):
            return False
        else:
            userIds = self.getAllUserId()
            if userIds == []:
                newId = 1
            else:
                userIds.sort()
                newId = int(userIds[len(userIds)-1]) + 1
            newUser = {'userName':name, 'id':str(newId)}
            self.users.append(newUser)
            
            self.__writeCSV(newUser)
            
            return newId
        
#         
    def changeUserName(self, old, new):
        if self.hasUser(old):
            userNames = self.getAllUserName()
            index = userNames.index(old)
            self.users[index]['userName'] = str(new)
            self.__writeCSV(self.users)
            return True
        else:
            return False
        
    def deleteUser(self, userName):
        if self.hasUser(userName):
            userNames = self.getAllUserName()
            index = userNames.index(userName)
            self.users.__delitem__(index)
            self.__writeCSV(self.users)
            return True
        else:
            return False
#         
    def setCSVFile(self, fileName):
        self.__CSVFile = fileName
#         
    def getUserByName(self, name):
        self.__readCSV()
        for user in self.users:
            if user['userName'] == name:
                return user
#         
    def getUserById(self, id):
        self.__readCSV()
        for user in self.users:
            if int(user['id']) == id:
                return user

    def getAllUser(self):
        self.__readCSV()
        return self.users
#         
    def getAllUserName(self):
        self.__readCSV()
        return self.userNames
#         
    def getAllUserId(self):
        self.__readCSV()
        return self.userIds
            
    def __readCSV(self):
        self.csvIn = open(self.__CSVFile, 'rb')
        self.reader = csv.DictReader(self.csvIn, self.fieldNames)
        self.users = []
        self.userIds = []
        self.userNames = []
        for row in self.reader:
            self.users.append(row)
            self.userIds.append(row['id'])
            self.userNames.append(row['userName'])
        self.csvIn.close()

    def __writeCSV(self, data):
        if type(data) is list:
            self.csvOut = open(self.__CSVFile, 'wb')
            self.writer = csv.DictWriter(self.csvOut, self.fieldNames)
            print 'user update all'
            print data
            self.writer.writerows(data)
            self.csvOut.close()
            
        elif type(data) is dict:
            self.csvOut = open(self.__CSVFile, 'ab')
            self.writer = csv.DictWriter(self.csvOut, self.fieldNames)
            print 'user append'
            self.writer.writerow(data)
            self.csvOut .close()
        
    def __readJSON(self):
        self.jsonIn = open(self.__JSONFile, 'rb')
        self.users = json.loads(self.jsonIn.read())

    def __writeJSON(self, data):
        if type(data) is list:
            self.jsonOut = open(self.__CSVFile, 'wb')

        elif type(data) is dict:
            #TODO
            pass