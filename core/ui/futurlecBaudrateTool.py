# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'futurlecBaudrateTool.ui'
#
# Created: Sat Jul 25 23:15:05 2015
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(700, 93)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.baudrateComboBox = QtGui.QComboBox(self.groupBox)
        self.baudrateComboBox.setObjectName(_fromUtf8("baudrateComboBox"))
        self.horizontalLayout.addWidget(self.baudrateComboBox)
        self.defaultCheckBox = QtGui.QCheckBox(self.groupBox)
        self.defaultCheckBox.setObjectName(_fromUtf8("defaultCheckBox"))
        self.horizontalLayout.addWidget(self.defaultCheckBox)
        self.setPushButton = QtGui.QPushButton(self.groupBox)
        self.setPushButton.setObjectName(_fromUtf8("setPushButton"))
        self.horizontalLayout.addWidget(self.setPushButton)
        self.resetPushButton = QtGui.QPushButton(self.groupBox)
        self.resetPushButton.setObjectName(_fromUtf8("resetPushButton"))
        self.horizontalLayout.addWidget(self.resetPushButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "UKRAA Futurlec Controller Baudrate Tool", None))
        self.groupBox.setTitle(_translate("Dialog", "Baudrate Control", None))
        self.label.setText(_translate("Dialog", "Baudrate", None))
        self.defaultCheckBox.setText(_translate("Dialog", "Default", None))
        self.setPushButton.setText(_translate("Dialog", "Set", None))
        self.resetPushButton.setText(_translate("Dialog", "Reset", None))

