# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PyQt4 import QtGui

#封装cv2.VideoCapture函数，用于读取摄像头每帧图像的数据
#可将每帧图像数据转化为QImage及CVImage
class Video():
    def __init__(self, device):
        self.capture = cv2.VideoCapture(device)
        self.currentFrame = np.array([])
        self.readFrame = None
        self.is_release = False
 
    def setFrameSize(self, width, height):
        self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)
        
    def setFPS(self, fps):
        self.capture.set(cv2.cv.CV_CAP_PROP_FPS, fps)

    def read(self):
        ret, self.readFrame = self.capture.read()
        if ret == True:
            return self.readFrame
        else:
            return None

    def open(self, device):
        self.is_release = False
        self.capture.open(device)

    def release(self):
        self.is_release = True
        self.capture.release()

    def captureNextFrame(self, isFlip = True):
        """                           
        capture frame and reverse RBG BGR and return opencv image                                      
        """
        self.read()
        if self.readFrame != None:
            self.currentFrame = cv2.cvtColor(self.readFrame, cv2.COLOR_BGR2RGB)
            if isFlip == True:
                self.currentFrame = cv2.flip(self.currentFrame, 1)
            
    def convertFrame(self):
        """
        converts frame to format suitable for QtGui
        """
        try:
            height,width = self.currentFrame.shape[:2]
            img = QtGui.QImage(self.currentFrame,
                              width,
                              height,
                              QtGui.QImage.Format_RGB888)
            return img
        except:
            return None

    def getFrame(self):
        readFrame = self.read()
        return readFrame
        
    def getQImageFrame(self):
        self.captureNextFrame()
        return self.convertFrame()

    def getCVImage(self, params):
        return cv2.cvtColor(self.readFrame, params)
    
    def getGrayCVImage(self, isFlip=True):
        if self.readFrame != None:
            grayFrame = cv2.cvtColor(self.readFrame, cv2.COLOR_BGR2GRAY)
            if isFlip == True:
                grayFrame = cv2.flip(grayFrame, 1)
            return grayFrame
        else:
            print 'readFrame is None'
            return None