# -*- coding: utf-8 -*-
import datetime
from time import strftime

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import ui

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

style = QString(open('./ui/css/style.css').read())

class Ui_MainWindow(QMainWindow):
    model = None
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        
        self.setupUi(self)
        self.setStyleSheet(style)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(480, 800)
        
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)

        self.label_date = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(28)
        self.label_date.setFont(font)
        self.verticalLayout.addWidget(self.label_date)

        self.lcd_time = QtGui.QLCDNumber(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.lcd_time.setFont(font)
        self.lcd_time.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.lcd_time.setDigitCount(8)
        self.lcd_time.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.verticalLayout.addWidget(self.lcd_time)

        self.label_welcome = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(28)
        self.label_welcome.setFont(font)
        self.label_welcome.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label_welcome)

        self.gridLayout_buttons = QtGui.QGridLayout()
        self.gridLayout_buttons.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.gridLayout_buttons.setMargin(0)
        self.gridLayout_buttons.setSpacing(50)
        
        #button face
        self.btn_face = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_face.sizePolicy().hasHeightForWidth())
        self.btn_face.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(26)
        self.btn_face.setFont(font)
        self.gridLayout_buttons.addWidget(self.btn_face, 0, 0, 1, 1)
        
        self.btn_face.clicked.connect(self.btn_face_clicked)
        
        #button register
        self.btn_register = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_register.sizePolicy().hasHeightForWidth())
        self.btn_register.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(26)
        self.btn_register.setFont(font)
        self.gridLayout_buttons.addWidget(self.btn_register, 1, 0, 1, 1)
        
        self.btn_register.clicked.connect(self.btn_register_clicked)

        self.verticalLayout.addLayout(self.gridLayout_buttons)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.updateTime)
        self._timer.start(1000)
        self.update()

    def updateTime(self):
        # date = datetime.datetime.now().strftime('    %Y-%m-%d')
        dateNow = datetime.datetime.now()
        dy = dateNow.strftime('     %Y')
        dm = dateNow.strftime('%m')
        dd = dateNow.strftime('%d')
        time = dateNow.strftime('%H:%M:%S')
        
        self.label_date.setText(dy+u'年'+dm+u'月'+dd+u'日')
        # self.lcd_time.setText(time)
        self.lcd_time.display(strftime("%H"+":"+"%M"+":"+"%S"))

    def setModel(self, model):
        self.model = model

    def setVideo(self, video):
        self.video = video
        
    def btn_face_clicked(self):
        print 'facerec clicked'
        self.video.open(0)
        self._timer.stop()
        
        self.facerec = ui.FaceRec(self)
        self.facerec.setModel(self.model)
        self.facerec.setVideo(self.video)
        self.setCentralWidget(self.facerec)
        
    def btn_register_clicked(self):
        print 'face register'
        self._timer.stop()
        
        self.register = ui.FaceRegister(self)
        self.register.setModel(self.model)
        self.register.setVideo(self.video)
        self.setCentralWidget(self.register)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label_date.setText(_translate("MainWindow", u"    0000年00月00日", None))
        self.label_welcome.setText(unicode(u"人脸识别系统"))
        self.btn_face.setText(u"人脸识别")
        self.btn_register.setText(u"人脸录入")

