import sys
import cv2
import serial

from facerec import recognize
from camera import Video
from fingerec import finger

def fingerTest():
    fingerPrint = finger.FingerPrint()
    #print 'clear all user'
    #fingerPrint.clearAllUser()
    print 'add user'
    fingerPrint.addUser(0x05)
    print 'get compare level'
    fingerPrint.getCompareLevel()
    #fingerPrint.setCompareLevel(tmp)
    print 'get user count'
    fingerPrint.getUserCount()
    print 'get timeout'
    fingerPrint.getTimeOut()
    print 'verify'
    fingerPrint.verifyUser()

def callback(label, confidence):
    print label
    print confidence


if __name__ == '__main__':    
    fingerTest()
# video = Video.Video(0)
# video.setFrameSize(640, 480)
# video.setFPS(30)
# 
# recognizer = recognize.Recognizer()
# image = video.getCVImage(cv2.COLOR_BGR2BGRA)
# cv2.rectangle(image, (10, 10), (100, 100), (255,0,0))
# cv2.imwrite('debug.png', image)

#recognizer.startRec(image, callback)
    
