# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\pictureselect.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_pictureSelect(object):
    def setupUi(self, pictureSelect):
        pictureSelect.setObjectName(_fromUtf8("pictureSelect"))
        pictureSelect.resize(480, 800)
        self.scrollArea = QtGui.QScrollArea(pictureSelect)
        self.scrollArea.setGeometry(QtCore.QRect(0, 100, 480, 550))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 478, 548))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayoutWidget = QtGui.QWidget(self.scrollAreaWidgetContents)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 481, 551))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 2, 1, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.pushButton_back = QtGui.QPushButton(pictureSelect)
        self.pushButton_back.setGeometry(QtCore.QRect(190, 680, 100, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_back.setFont(font)
        self.pushButton_back.setObjectName(_fromUtf8("pushButton_back"))

        self.retranslateUi(pictureSelect)
        QtCore.QMetaObject.connectSlotsByName(pictureSelect)

    def retranslateUi(self, pictureSelect):
        pictureSelect.setWindowTitle(_translate("pictureSelect", "Form", None))
        self.label.setText(_translate("pictureSelect", "TextLabel", None))
        self.label_2.setText(_translate("pictureSelect", "TextLabel", None))
        self.label_4.setText(_translate("pictureSelect", "TextLabel", None))
        self.label_3.setText(_translate("pictureSelect", "TextLabel", None))
        self.label_5.setText(_translate("pictureSelect", "TextLabel", None))
        self.label_6.setText(_translate("pictureSelect", "TextLabel", None))
        self.pushButton_back.setText(_translate("pictureSelect", "Back", None))

