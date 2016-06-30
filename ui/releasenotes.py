# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'releasenotes.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 480)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.releasenotesText = QtWidgets.QTextEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(14)
        self.releasenotesText.setFont(font)
        self.releasenotesText.setFrameShape(QtWidgets.QFrame.Box)
        self.releasenotesText.setFrameShadow(QtWidgets.QFrame.Plain)
        self.releasenotesText.setReadOnly(True)
        self.releasenotesText.setObjectName("releasenotesText")
        self.gridLayout.addWidget(self.releasenotesText, 0, 0, 1, 1)
        self.releasenotesDialog = QtWidgets.QDialogButtonBox(Dialog)
        self.releasenotesDialog.setOrientation(QtCore.Qt.Horizontal)
        self.releasenotesDialog.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.releasenotesDialog.setObjectName("releasenotesDialog")
        self.gridLayout.addWidget(self.releasenotesDialog, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.releasenotesDialog.accepted.connect(Dialog.accept)
        self.releasenotesDialog.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Release Notes"))

