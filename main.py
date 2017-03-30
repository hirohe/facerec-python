# -*- coding: utf-8 -*-
import sys
import cv2

from ui import mainwindow
from camera import Video
from configure import config

from PyQt4.QtGui import QApplication

def main():
    
    model = cv2.createLBPHFaceRecognizer()
    model.load(config.TRAINING_FILE)
    
    video = Video.Video(0)
    video.setFrameSize(640, 480)
    video.setFPS(30)
    
    QtApp = QApplication(sys.argv)
    
    mainWindow = mainwindow.Ui_MainWindow()
    mainWindow.setModel(model)
    mainWindow.showFullScreen()
    mainWindow.setVideo(video)
    mainWindow.raise_()
    
    QtApp.exec_()

if __name__ == '__main__':
    main()
