# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'releasenotes.ui'
#
# Created: Mon May  2 14:03:46 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 480)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.releasenotesText = QtGui.QTextEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(14)
        self.releasenotesText.setFont(font)
        self.releasenotesText.setFrameShape(QtGui.QFrame.Box)
        self.releasenotesText.setFrameShadow(QtGui.QFrame.Plain)
        self.releasenotesText.setReadOnly(True)
        self.releasenotesText.setObjectName("releasenotesText")
        self.gridLayout.addWidget(self.releasenotesText, 0, 0, 1, 1)
        self.releasenotesDialog = QtGui.QDialogButtonBox(Dialog)
        self.releasenotesDialog.setOrientation(QtCore.Qt.Horizontal)
        self.releasenotesDialog.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.releasenotesDialog.setObjectName("releasenotesDialog")
        self.gridLayout.addWidget(self.releasenotesDialog, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.releasenotesDialog, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.releasenotesDialog, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Release Notes", None, QtGui.QApplication.UnicodeUTF8))

