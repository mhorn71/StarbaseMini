# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'metadata.ui'
#
# Created: Fri May 20 12:15:54 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MetadataDialog(object):
    def setupUi(self, MetadataDialog):
        MetadataDialog.setObjectName("MetadataDialog")
        MetadataDialog.resize(640, 480)
        self.gridLayout = QtGui.QGridLayout(MetadataDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(MetadataDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(MetadataDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(MetadataDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 1)
        self.metadataEdit = QtGui.QTextBrowser(MetadataDialog)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(14)
        self.metadataEdit.setFont(font)
        self.metadataEdit.setObjectName("metadataEdit")
        self.gridLayout.addWidget(self.metadataEdit, 1, 0, 1, 1)
        self.metadataNotesEdit = QtGui.QLineEdit(MetadataDialog)
        self.metadataNotesEdit.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(14)
        self.metadataNotesEdit.setFont(font)
        self.metadataNotesEdit.setMaxLength(100)
        self.metadataNotesEdit.setCursorPosition(0)
        self.metadataNotesEdit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.metadataNotesEdit.setObjectName("metadataNotesEdit")
        self.gridLayout.addWidget(self.metadataNotesEdit, 3, 0, 1, 1)

        self.retranslateUi(MetadataDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), MetadataDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), MetadataDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MetadataDialog)

    def retranslateUi(self, MetadataDialog):
        MetadataDialog.setWindowTitle(QtGui.QApplication.translate("MetadataDialog", "Metadata", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MetadataDialog", "Metadata", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MetadataDialog", "Observation Notes", None, QtGui.QApplication.UnicodeUTF8))

