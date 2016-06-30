# -*- coding: utf-8 -*-
'''
Created on 2016-4-26

@author: imhey_000
'''
import serial
import struct

from PyQt4.QtCore import QThread
from ctypes import *
from time import sleep

#基本应答信息定义
ACK_SUCCESS = 0x00
ACK_FAIL    = 0x01
ACK_FULL    = 0x04
ACK_NO_USER = 0x05
ACK_TIMEOUT = 0x08
ACK_GO_OUT  = 0x0F

#用户信息定义
ACK_ALL_USER    = 0x00
ACK_GUEST_USER  = 0x01
ACK_NORMAL_USER = 0x02
ACK_MASTER_USER = 0x03

#设置容量 MAX = 1000
USER_MAX_CNT    = 40

#命令定义
CMD_HEAD        = 0xF5
CMD_TAIL        = 0xF5
CMD_ADD_1       = 0x01
CMD_ADD_2       = 0x02
CMD_ADD_3       = 0x03
CMD_MATCH       = 0x0C
CMD_DEL         = 0x04
CMD_DEL_ALL     = 0x05
CMD_USER_CNT    = 0x09
CMD_COM_LEV     = 0x28
CMD_LP_MODE     = 0x2C
CMD_TIMEOUT     = 0x2E

CMD_FINGER_DETECTED = 0x14    

class FingerPrint(object):
    
    gTxBuf = None
    gRsBuf = None
    device = None
    resource = ''
    rate = 0
    
    def __init__(self, resource='/dev/ttyAMA0', rate=19200):
        self.gTxBuf = (c_ubyte * 9)()
        self.gTxBuf[0] = 0x00
        self.gTxBuf[1] = 0x00
        self.gTxBuf[2] = 0x00
        self.gTxBuf[3] = 0x00
        self.gTxBuf[4] = 0x00
        self.gTxBuf[5] = 0x00
        self.gTxBuf[6] = 0x00
        self.gTxBuf[7] = 0x00
        self.gTxBuf[8] = 0x00
        
        self.gRsBuf = (c_ubyte * 9)()
        
        self.baudRate = rate
        self.resource = resource
        self.device = serial.Serial(resource, baudrate=rate)
        
    def packTxData(self):
        data = struct.pack('BBBBBBBBB', self.gTxBuf[0],
                                        self.gTxBuf[1],
                                        self.gTxBuf[2],
                                        self.gTxBuf[3],
                                        self.gTxBuf[4],
                                        self.gTxBuf[5],
                                        self.gTxBuf[6],
                                        self.gTxBuf[7],
                                        self.gTxBuf[8])
        return data
       
    def packRsData(self):
        data = struct.pack('BBBBBBBB',  self.gRsBuf[0],
                                        self.gRsBuf[1],
                                        self.gRsBuf[2],
                                        self.gRsBuf[3],
                                        self.gRsBuf[4],
                                        self.gRsBuf[5],
                                        self.gRsBuf[6],
                                        self.gRsBuf[7])
        return data
       
    def unpackRsData(self):
        out = struct.unpack('BBBBBBBB', self.gRsBuf)
        return out
        
    def txAndRsCmd(self, sCnt, rCnt, delay):
        checkSum = 0
        self.device = serial.Serial(self.resource, self.baudRate, timeout=delay)
        
        data = self.packTxData()
        
        self.device.write(struct.pack('B', CMD_HEAD))
        for i in range(0, sCnt):
            self.device.write(data[i])
            #self.unpackData(data)
            checkSum ^= self.gTxBuf[i]
        self.device.write(struct.pack('B', checkSum))
        self.device.write(struct.pack('B', CMD_TAIL))
        
        self.gRsBuf = self.device.read(8)
        
        print 'gRsBuf len:', len(self.gRsBuf)
        
        if len(self.gRsBuf) != rCnt:
            print 'time out'
            return ACK_TIMEOUT
        if self.gRsBuf[0] != struct.pack('B', CMD_HEAD):
            print 'fail type error1'
            return ACK_FAIL
        if self.gRsBuf[rCnt - 1] != struct.pack('B', CMD_TAIL):
            print 'fail type error2'
            return ACK_FAIL
        if self.gRsBuf[1] != struct.pack('B', self.gTxBuf[0]):
            print 'fail type error3'
            return ACK_FAIL
        
        #debug
        reponse = self.unpackRsData()
        for i in range(0, 8):
            print hex(reponse[i])
        
        checkSum = 0
        for i in range(1, (len(self.gRsBuf) - 1)):
            checkSum ^= struct.unpack('B', self.gRsBuf[i])[0]
        print struct.pack('B', checkSum)
        if checkSum != 0:
            print 'checksum error'
            return ACK_FAIL
            
        print 'success'
        return ACK_SUCCESS
        
    def addUser(self, userCode):
        userCount = self.getUserCount()
        if userCount >= USER_MAX_CNT:
            return ACK_FAIL
        
        print 'add 1'
        self.gTxBuf[0] = CMD_ADD_1
        self.gTxBuf[1] = 0x00
        self.gTxBuf[2] = userCode
        self.gTxBuf[3] = 0x03
        self.gTxBuf[4] = 0x00
        result = self.txAndRsCmd(5, 8, 200)
        if result == ACK_SUCCESS and struct.unpack('B', self.gRsBuf[4])[0] == ACK_SUCCESS:
            print 'add 2'
            self.gTxBuf[0] = CMD_ADD_2
            result = self.txAndRsCmd(5, 8, 200)
            if result == ACK_SUCCESS and struct.unpack('B', self.gRsBuf[4])[0] == ACK_SUCCESS:
                print 'add 3'
                self.gTxBuf[0] = CMD_ADD_3
                result = self.txAndRsCmd(5, 8, 200)
                if result == ACK_SUCCESS and struct.unpack('B', self.gRsBuf[4])[0] == ACK_SUCCESS:
                    print 'add success'
                    return ACK_SUCCESS
                else:
                    return ACK_FAIL
            else:
                return ACK_FAIL
        else:
            return ACK_FAIL
        
    def clearAllUser(self):
        self.gTxBuf[0] = CMD_DEL_ALL
        self.gTxBuf[1] = 0x00
        self.gTxBuf[2] = 0x00
        self.gTxBuf[3] = 0x00
        self.gTxBuf[4] = 0x00
        
        result = self.txAndRsCmd(5, 8, 50)
        print result
        #print struct.unpack('B', result)[0]
        #if result == ACK_SUCCESS and self.gRsBuf[4] == ACK_SUCCESS:
        if result == 0x00 and struct.unpack('B', self.gRsBuf[4])[0] == 0x00:
            print 'user all clear'
            None
            
    def isMasterUser(self, userID):
        if userID == 1 or userID == 2 or userID == 3:
            return True
        else:
            return False
        
    def verifyUser(self):
        self.gTxBuf[0] = CMD_MATCH
        self.gTxBuf[1] = 0x00
        self.gTxBuf[2] = 0x00
        self.gTxBuf[3] = 0x00
        self.gTxBuf[4] = 0x00
        
        result = self.txAndRsCmd(5, 8, 150)
        print hex(result)
        if result != ACK_TIMEOUT:
            if result == ACK_SUCCESS and self.isMasterUser(struct.unpack('B', self.gRsBuf[4])[0]):
                print 'verify success'
                return ACK_SUCCESS
            elif struct.unpack('B', self.gRsBuf[4])[0] == ACK_NO_USER:
                print 'no user'
                return ACK_NO_USER
            else:
                print 'verify fail'
                return ACK_GO_OUT
        else:
            return ACK_TIMEOUT
        
    def getUserCount(self):
        self.gTxBuf[0] = CMD_USER_CNT
        self.gTxBuf[1] = 0x00
        self.gTxBuf[2] = 0x00
        self.gTxBuf[3] = 0x00
        self.gTxBuf[4] = 0x00
        
        result = self.txAndRsCmd(5, 8, 10)
        if result == ACK_SUCCESS and struct.unpack('B', self.gRsBuf[4])[0] == ACK_SUCCESS:
            print 'user count: ',struct.unpack('B', self.gRsBuf[3])[0]
            return struct.unpack('B', self.gRsBuf[3])[0]
        else:
            return 0xFF
        
    def getCompareLevel(self):
        self.gTxBuf[0] = CMD_COM_LEV
        self.gTxBuf[1] = 0x00
        self.gTxBuf[2] = 0x00
        self.gTxBuf[3] = 0x01
        self.gTxBuf[4] = 0x00
        
        result = self.txAndRsCmd(5, 8, 10)
        if result == ACK_SUCCESS and struct.unpack('B', self.gRsBuf[4])[0] == ACK_SUCCESS:
            print 'compare level: ',struct.unpack('B', self.gRsBuf[3])[0]
            return struct.unpack('B', self.gRsBuf[3])[0]
        else:
            return 0xFF
        
    def setCompareLevel(self, tmp):
        self.gTxBuf[0] = CMD_COM_LEV
        self.gTxBuf[1] = 0x00
        self.gTxBuf[2] = tmp
        self.gTxBuf[3] = 0x00
        self.gTxBuf[4] = 0x00
        
        result = self.txAndRsCmd(5, 8, 10)
        if result == ACK_SUCCESS and struct.unpack('B', self.gRsBuf[4])[0] == ACK_SUCCESS:
            return struct.unpack('B', self.gRsBuf[3])[0]
        else:
            return 0xFF
        
    def getTimeOut(self):
        self.gTxBuf[0] = CMD_TIMEOUT
        self.gTxBuf[1] = 0x00
        self.gTxBuf[2] = 0x00
        self.gTxBuf[3] = 0x01
        self.gTxBuf[4] = 0x00
        
        result = self.txAndRsCmd(5, 8, 10)
        if result == ACK_SUCCESS and struct.unpack('B', self.gRsBuf[4])[0] == ACK_SUCCESS:
            return struct.unpack('B', self.gRsBuf[3])[0]
        else:
            return 0xFF
        
    
class FingerPrintThread(QThread):
        
    runFunction     = 1
    ADD_USER        = 0
    VERIFY          = 1
    CLEAR_ALL_USER  = 2
    SET_COM_LEV     = 3
    GET_COM_LEV     = 4
    GET_TIME_OUT    = 5
    GET_USER_CNT    = 6
    
    callBack = None
    resource = ''
    rate = 0
    
    def __init__(self, resource='/dev/ttyAMA0', rate=19200):
        super(FingerPrintThread, self).__init__()
        
        self.resource = resource
        self.rate = rate
        self.fingerPrint = FingerPrint(resource=self.resource, rate=self.rate)
    
        self.result = None
    
    def setFunction(self, runFunction):
        self.runFunction = runFunction
    
    def run(self):
        
        if self.runFunction == self.ADD_USER:
            self.result = self.fingerPrint.addUser(self.userCode)
        elif self.runFunction == self.VERIFY:
            self.result = self.fingerPrint.verifyUser()
        elif self.runFunction == self.CLEAR_ALL_USER:
            self.result = self.fingerPrint.clearAllUser()
        elif self.runFunction == self.SET_COM_LEV:
            self.result = self.fingerPrint.setCompareLevel(self.tmp)
        elif self.runFunction == self.GET_COM_LEV:
            self.result = self.fingerPrint.getCompareLevel()
        elif self.runFunction == self.GET_TIME_OUT:
            self.result = self.fingerPrint.getTimeOut()
        elif self.runFunction == self.GET_USER_CNT:
            self.result = self.fingerPrint.getUserCount()
        
        
    