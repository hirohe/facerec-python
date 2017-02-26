# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from facerec import recognize, train
from facerec import face
from camera import VideoStream
from configure import config, userManager

from soft_keyboard import *

import os
import cv2

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

#Qt css样式文件
style = QString(open('./ui/css/style.css').read())

#显示视频的Qt控件
#setRect当前一帧图像上画出方框，用于标记人脸的位置
#setRectColor设置方框的颜色
#setUserLabel在方框旁边添加识别信息，比如识别到的用户名
class VideoFrame(QtGui.QLabel):
        
    userName = None
    pen_faceRect = QtGui.QPen()
    pen_faceRect.setColor(QtGui.QColor(255, 0, 0))
    x = 0;y = 0;w = 0;h = 0
    
    def __init__(self, parent):
        QtGui.QLabel.__init__(self, parent)
        
    def setRect(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
    
    def setRectColor(self, r, g, b):
        self.pen_faceRect.setColor(QtGui.QColor(r, g, b))

    def setUserLabel(self, userName):
        self.userName = userName

    def paintEvent(self, event):
        QtGui.QLabel.paintEvent(self,event)
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen_faceRect)
        painter.drawRect(self.x, self.y, self.w, self.h)
        if self.userName != None:
            painter.drawText(self.x, self.y+15, self.userName)

#人脸识别界面
class FaceRec(QWidget):
    
    model = None
    confidence = -1
    label = ''
    faceRect = None
    
    captureFlag = 0
    
    confidences = []
    
    def __init__(self, mainWindow):
        super(FaceRec, self).__init__()
        self.mainWindow = mainWindow
        self.manager = userManager.UserManager()
        
        self.setupUi(self)
        
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.playVideo)
        self._timer.start(10)
        self.update()
    
    def setModel(self, model):
        self.model = model
    
    def setupUi(self, FaceRec):
        FaceRec.setObjectName(_fromUtf8("FaceRec"))
        FaceRec.resize(480, 800)
        
        font = QtGui.QFont()
        font.setPointSize(16)
        
        self.video_frame = VideoFrame(FaceRec)
        self.video_frame.setGeometry(QtCore.QRect(0, 100, 480, 360))
        
        self.pushButton_back = QtGui.QPushButton(FaceRec)
        self.pushButton_back.setGeometry(QtCore.QRect(190, 600, 80, 50))
        self.pushButton_back.setFont(font)
        self.pushButton_back.clicked.connect(self.pushButton_back_clicked)
        
        self.label_title = QtGui.QLabel(FaceRec)
        self.label_title.setGeometry(QtCore.QRect(10, 10, 460, 50))
        self.label_title.setFont(font)
        
        self.label_info = QtGui.QLabel(FaceRec)
        self.label_info.setGeometry(QtCore.QRect(0, 500, 480, 50))
        self.label_info.setFont(font)

        self.retranslateUi(FaceRec)
        QtCore.QMetaObject.connectSlotsByName(FaceRec)

    def pushButton_capture_clicked(self):
        print 'capture clicked'
        self.captureFlag = 10

    def pushButton_back_clicked(self):
        self._timer.stop()
        self.vs.stop()
        self.video.release()
        self.mainWindow.setupUi(self.mainWindow)

    def pushButton_capture_clicked(self):
        self.startRec()

    def setVideo(self, video):
        self.video = video
        
        self.vs = VideoStream.VideoStream(self.video,'192.168.1.113', 8888)
        #self.vs.startStream()
        
        self.startRec()
        
    def playVideo(self):
        try:
            pixMap_frame = QtGui.QPixmap.fromImage(self.video.getQImageFrame())
            x = 0;y = 0;w = 0;h = 0
            if self.faceRect != None:
                #640x480 to 480x360
                x, y, w, h = self.faceRect[0]*0.75, self.faceRect[1]*0.75, self.faceRect[2]*0.75, self.faceRect[3]*0.75
            self.video_frame.setRect(x, y, w, h)
            self.video_frame.setPixmap(pixMap_frame)
            self.video_frame.setScaledContents(True)
        except TypeError:
            print "No frame"
            
    def startRec(self):
        self.recognizer = recognize.Recognizer()
        self.recognizer.finished.connect(self.reciveRecognizeResult)
        image = self.video.getGrayCVImage()
        self.recognizer.startRec(image, self.model)
        
    def reciveRecognizeResult(self):
        self.faceRect = self.recognizer.result
        userName = None
        if not self.video.is_release:
            if self.recognizer.result != None:
                self.confidences.append(self.recognizer.confidence)
                mean = sum(self.confidences) / float(len(self.confidences))
                print 'label:',self.recognizer.label
                print 'confidence: %.4f'%self.recognizer.confidence,'mean:%.4f'%mean

                user = self.manager.getUserById(self.recognizer.label)

                self.video_frame.setUserLabel(userName)

                if user != None:
                    userName = user['userName']

                if self.recognizer.confidence <= 60:
                    self.video_frame.setRectColor(0, 255, 0)
                else:
                    self.video_frame.setRectColor(255, 0, 0)
            
            info = 'user: ' + str(userName) + ' | confidence: ' + str(self.recognizer.confidence)
            self.label_info.setText(info)
            self.startRec()

    def retranslateUi(self, FaceRec):
        FaceRec.setWindowTitle(_translate("FaceRec", u"from", None))
        self.label_title.setText(_translate("FaceRec", u"人脸识别", None))
        self.video_frame.setText(_translate("FaceRec", "video_frame", None))
        self.label_info.setText(_translate("FaceRec", "label_info", None))
        self.pushButton_back.setText(_translate("FaceRec", u"返回", None))

#人脸录入界面
class FaceRegister(QWidget):
    
    faceRect = None
    
    captureFlag = 0
    personName = None
    recOver = False
    model = None
    
    def __init__(self, mainWindow):
        super(FaceRegister, self).__init__()
        
        self.mainWindow = mainWindow
        self.manager = userManager.UserManager()
        
        self.setupUi(self)
        
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.playVideo)
        #self._timer.start(10)    
        
        self.update()
        
    def setupUi(self, FaceRegister):
        FaceRegister.setObjectName(_fromUtf8("FaceRegister"))
        FaceRegister.resize(480, 800)
        
        self.inputDialog = InputDialog(self.reciveUserName)

        font = QtGui.QFont()
        font.setPointSize(16)

        self.label_title = QtGui.QLabel(FaceRegister)
        self.label_title.setGeometry(QtCore.QRect(20, 50, 440, 60))
        self.label_title.setFont(font)

        self.progressBar = QtGui.QProgressBar(FaceRegister)
        self.progressBar.setGeometry(QtCore.QRect(20, 470, 440, 60))
        self.progressBar.setRange(0, 20)
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)

        self.video_frame = VideoFrame(FaceRegister)
        self.video_frame.setGeometry(QtCore.QRect(0, 100, 480, 360))
         
        self.pushButton_capture = QtGui.QPushButton(FaceRegister)
        self.pushButton_capture.setGeometry(QtCore.QRect(190, 560, 100, 60))
        self.pushButton_capture.setFont(font)
        self.pushButton_capture.clicked.connect(self.pushButton_capture_clicked)
         
        self.pushButton_back = QtGui.QPushButton(FaceRegister)
        self.pushButton_back.setGeometry(QtCore.QRect(190, 650, 100, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_back.setFont(font)
        self.pushButton_back.clicked.connect(self.pushButton_back_clicked)
 
        self.retranslateUi(FaceRegister)
        QtCore.QMetaObject.connectSlotsByName(FaceRegister)
        
    def setVideo(self, video):
        self.video = video
        if self.video.is_release:
            self.video.open(0)
        
    def setModel(self, model):
        self.model = model
        
    def playVideo(self):
        try:
            pixMap_frame = QtGui.QPixmap.fromImage(self.video.getQImageFrame())
            x = 0;y = 0;w = 0;h = 0
            if self.faceRect != None:
                x, y, w, h = self.faceRect[0]*0.75, self.faceRect[1]*0.75, self.faceRect[2]*0.75, self.faceRect[3]*0.75
            self.video_frame.setRect(x, y, w, h)
            self.video_frame.setPixmap(pixMap_frame)
            self.video_frame.setScaledContents(True)
        except TypeError:
            print 'No frame'
        
    def startRec(self):
        self.recognizer = recognize.Recognizer()
        self.recognizer.finished.connect(self.reciveRecognizeResult)
        image = self.video.getGrayCVImage()
        self.recognizer.startRec(image, None)
        
    def reciveRecognizeResult(self):
        self.faceRect = self.recognizer.result
        if self.faceRect != None and self.captureFlag != 0:
            x, y, w, h = self.faceRect
            crop = face.crop(self.recognizer.faceImage, x, y, w, h)
            personDir = os.path.join(config.FACES_DIR, self.personName)
            if not os.path.exists(personDir):
                os.makedirs(personDir)
            fileName = os.path.join(personDir, 'face_'+'%03d.pgm'%self.captureFlag)
            cv2.imwrite(fileName, crop)
            print 'capture'
            self.captureFlag -= 1
            self.progressBar.setValue(20 - self.captureFlag)
            if self.captureFlag == 0:
                self.recOver = True
                print 'capture over'
                self.video.release()
                self.startPictureSelect()
   
        if not self.video.is_release and self.recOver == False:
            self.startRec()
        
    def reciveUserName(self, name):
        self.personName = str(name)
        
        #self.inputDialog.deleteLater()
        print name
        personDir = os.path.join(config.FACES_DIR, self.personName)
        if os.path.exists(personDir):
            print 'person already exist'
            #TODO alert
            self.inputDialog.show(u'用户已存在！')
        else:
            self.pushButton_capture.setEnabled(False)
            self.captureFlag = 20
            self.progressBar.setVisible(True)
            self.label_title.setText(u'开始截取图片')
            self._timer.start(10)
            self.startRec()
            
    def startPictureSelect(self):
        print 'start picture select'
        pictureSelect = PictureSelect(self.mainWindow, self.personName)
        pictureSelect.setModel(self.model)
        self.mainWindow.setCentralWidget(pictureSelect)
        
    def pushButton_capture_clicked(self):
        self.inputDialog.setInfo(u'请输入用户名')
        self.inputDialog.show()
        self.inputDialog.clear()
            
    def pushButton_back_clicked(self):
        self._timer.stop()
        self.video.release()
        self.mainWindow.setupUi(self.mainWindow)
        
    def retranslateUi(self, FaceRegister):
        FaceRegister.setWindowTitle(_translate("FaceRegister", "Form", None))
        self.label_title.setText(_translate("FaceRegister", u" ", None))
        self.video_frame.setText(_translate("FaceRegister", " ", None))
        self.pushButton_capture.setText(_translate("FaceRegister", u"开始", None))
        self.pushButton_back.setText(_translate("FaceRegister", u"返回", None))

#软键盘控件
class InputDialog(TouchInputWidget):
    def __init__(self, callback):
        TouchInputWidget.__init__(self)
        
        self.callback = callback
        
        self.labelInfo = QtGui.QLabel()
        
        self.editUserName = QtGui.QLineEdit()
        self.editUserName.keyboard_type = 'default'
        
        self.pushButton_accept = QtGui.QPushButton(self)
        self.pushButton_accept.setText(u'确认')
        self.pushButton_accept.clicked.connect(self.reciveUserName)
        
        gl = QtGui.QVBoxLayout()
        gl.addWidget(self.pushButton_accept)
        gl.addWidget(self.labelInfo)
        gl.addWidget(self.editUserName)
        
        self.setLayout(gl)
        
    def setInfo(self, info):
        self.labelInfo.setText(info)
        
    def clear(self):
        self.editUserName.clear()
        
    def reciveUserName(self):
        self.touch_interface._input_panel_all.hide()
        self.userName = self.editUserName.text()
        if self.userName == '':
            return
        self.callback(self.userName)
        self.hide()

#图片选择界面
class PictureSelect(QWidget):
    
    pictures = []
    pictureNames = []
    path = None
    model = None

    def __init__(self, mainWindow, path):
        super(PictureSelect, self).__init__()
        self.mainWindow = mainWindow
        self.path = path

        self.setupUi(self)
        
        self.readPictures()
        
        self.showPictures()
        
    def setupUi(self, pictureSelect):
        pictureSelect.setObjectName(_fromUtf8("pictureSelect"))
        pictureSelect.resize(480, 800)
        
        self.setStyleSheet(style)
        
        font = QtGui.QFont()
        font.setPointSize(18)
        
        self.label_info = QtGui.QLabel(pictureSelect)
        self.label_info.setGeometry(QtCore.QRect(0, 20, 480, 50))
        self.label_info.setFont(font)
        
        self.scrollArea = QtGui.QScrollArea(pictureSelect)
        self.scrollArea.setGeometry(QtCore.QRect(0, 100, 480, 550))
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 478, 548))
        
        self.gridLayoutWidget = QtGui.QWidget(self.scrollArea)
        
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        
        self.scrollArea.setWidget(self.gridLayoutWidget)
        
        font = QtGui.QFont()
        font.setPointSize(16)
        
        self.pushButton_delete = QtGui.QPushButton(pictureSelect)
        self.pushButton_delete.setGeometry(QtCore.QRect(70, 680, 100, 60))
        self.pushButton_delete.setFont(font)
        self.pushButton_delete.clicked.connect(self.pushButton_delete_clicked)
        
        self.pushButton_ok = QtGui.QPushButton(pictureSelect)
        self.pushButton_ok.setGeometry(QtCore.QRect(190, 680, 100, 60))
        self.pushButton_ok.setFont(font)
        self.pushButton_ok.clicked.connect(self.pushButton_ok_clicked)
        
        self.pushButton_back = QtGui.QPushButton(pictureSelect)
        self.pushButton_back.setGeometry(QtCore.QRect(310, 680, 100, 60))
        self.pushButton_back.setFont(font)
        self.pushButton_back.setObjectName(_fromUtf8("pushButton_back"))
        self.pushButton_back.clicked.connect(self.pushButton_back_clicked)

        self.retranslateUi(pictureSelect)
        QtCore.QMetaObject.connectSlotsByName(pictureSelect)

    def setModel(self, model):
        self.model = model

    def readPictures(self):
        self.pictures = []
        self.pictureNames = []
        path = os.path.join(config.FACES_DIR, self.path)
        for fileName in train.walkFiles(path, '*.pgm'):
            self.pictures.append(QtGui.QPixmap(fileName))
            self.pictureNames.append(fileName)

    def clearGridLayout(self):
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().deleteLater()

    def showPictures(self):
        for i in range(0, len(self.pictures)):
            label_pic = PictureLabel()
            label_pic.mousePressEvent = label_pic.clicked
            h = self.pictures[i].height()
            w = self.pictures[i].width()
            label_pic.setFixedSize(QSize(w, h))
            label_pic.setPixmap(self.pictures[i])
            label_pic.setPictureName(self.pictureNames[i])
            self.gridLayout.addWidget(label_pic, i/2, i%2, 1, 1)
        self.gridLayoutWidget.setFixedSize(self.gridLayout.sizeHint())

    def trainFinish(self):
        dialog = QtGui.QMessageBox()
        dialog.setWindowTitle('info')
        dialog.setText(u'人脸录入已完成(%s)'%self.path)
        if dialog.exec_():
            print 'over'
            self.label_info.setText(u'选择要删除的图片，点击删除按钮进行删除')
            self.pushButton_ok.setEnabled(True)

    def pushButton_delete_clicked(self):
        self.pushButton_delete.setEnabled(False)
        for i in range(self.gridLayout.count()):
            item = self.gridLayout.itemAt(i)
            if item != None:
                label_pic = item.widget()
                print label_pic.pictureName
                if label_pic.selected:
                    print 'delete',label_pic.pictureName
                    os.remove(os.path.join(config.FACES_DIR, self.path, label_pic.pictureName))
            
        self.clearGridLayout()   
        self.readPictures()
        self.showPictures()
        self.pushButton_delete.setEnabled(True)

    def pushButton_ok_clicked(self):
        self.label_info.setText(u'正在录入人脸...')
        self.pushButton_ok.setEnabled(False)
        self.trainThread = TrainThread(self.model, os.path.join(config.TRAINING_DIR, config.TRAINING_FILE))
        self.trainThread.finished.connect(self.trainFinish)
        self.trainThread.start()

    def pushButton_back_clicked(self):
        self.gridLayout = None
        self.pictures = []
        self.pictureNames = []
        self.mainWindow.setupUi(self.mainWindow)

    def retranslateUi(self, pictureSelect):
        pictureSelect.setWindowTitle(_translate("pictureSelect", "Form", None))
        self.label_info.setText(_translate("pictureSelect", u"选择要删除的图片，点击删除按钮进行删除", None))
        self.pushButton_back.setText(_translate("pictureSelect", u"返回", None))
        self.pushButton_delete.setText(_translate("pictureSelect", u"删除", None))
        self.pushButton_ok.setText(_translate("pictureSelect", u"录入", None))

class TrainThread(QtCore.QThread):
    
    model = None
    trainFileName = None
    
    def __init__(self, model, trainFileName):
        super(TrainThread, self).__init__()
        
        self.model = model
        self.trainFileName = trainFileName
        
    def run(self):
        train.trainFace(self.model)
        print 'train faces over'
        self.model.load(self.trainFileName)
        print 'model reload over'

#显示单个图像的Qt控件
class PictureLabel(QtGui.QLabel):
        
    selected = False
    pictureName = None
    
    def __init__(self):
        QtGui.QLabel.__init__(self)
        self.deleteImage = QtGui.QPixmap('./res/pic/delete_100x100.png')
        
    def setPictureName(self, name):
        self.pictureName = name
        
    def clicked(self, event):
        print 'clicked'
        if self.selected:
            self.selected = False
        else:
            self.selected = True
        self.update()
        
    def paintEvent(self, event):
        QtGui.QLabel.paintEvent(self,event)
        if self.selected:
            painter = QtGui.QPainter(self)
            size = self.sizeHint()
            x = size.width()/2 - 50
            y = size.height()/2 - 50
            painter.drawPixmap(x, y, self.deleteImage)
