# -*- coding: utf-8 -*-
import threading
import socket
import numpy as np
import cv2
from _socket import timeout

class VideoStream(threading.Thread):
    '''
    '''
    
    def __init__(self, video, host, port):
        '''
        Constructor
        '''
        super(VideoStream, self).__init__()
        
        self.video = video
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]
        
        self._stop = False
    
    def setEncodeParam(self, param):
        self.encode_param = param
    
    def setServer(self, host, port):
        self.host = host
        self.port = port
        
    def run(self):
        #self.s.connect((self.host, self.port))
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.settimeout(5)
        self.s.bind((self.host, self.port))
        self.s.listen(True)
        
        connect, address = self.waitConnect()
        if connect is None:
            return
        print 'address:', address
        while not self.stoped():
            try:
                frame = self.video.readFrame
                if frame != None:
                    frame = cv2.flip(frame, 1)
                    result, encodeImage = cv2.imencode('.jpg', frame, self.encode_param)
                    data = np.array(encodeImage)
                    stringData = data.tostring()
                    
                    connect.send(str(len(stringData)).ljust(16))
                    connect.send(stringData)
            except socket.error:
                connect.close()
                connect, address = self.waitConnect()
                if connect is None:
                    return
                print 'address:', address
        self.s.close()
        print 'stream stop'
                #self.s.closeSocket()
#                 data = np.array(frame)
#                 stringData = data.totring()
#                 self.s.send(str(len(stringData)).ljust(16))
#                 self.s.send(stringData)
        
    def waitConnect(self):
        connected = False
        connect, address = None, None
        while not connected and not self.stoped():
            try:
                connect, address = self.s.accept()
                connected = True
            except timeout:
                None
        return connect, address
        
    def startStream(self):
        self.start()
        
    def stop(self):
        self._stop = True
        
    def stoped(self):
        return self._stop
