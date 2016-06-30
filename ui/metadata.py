# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'metadata.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MetadataDialog(object):
    def setupUi(self, MetadataDialog):
        MetadataDialog.setObjectName("MetadataDialog")
        MetadataDialog.resize(640, 480)
        self.gridLayout = QtWidgets.QGridLayout(MetadataDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(MetadataDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(MetadataDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(MetadataDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 1)
        self.metadataEdit = QtWidgets.QTextBrowser(MetadataDialog)
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        font.setPointSize(10)
        self.metadataEdit.setFont(font)
        self.metadataEdit.setStyleSheet("QTextBrowser {\n"
"    background-color: \'#FFFFE0\';\n"
"}")
        self.metadataEdit.setObjectName("metadataEdit")
        self.gridLayout.addWidget(self.metadataEdit, 1, 0, 1, 1)
        self.metadataNotesEdit = QtWidgets.QLineEdit(MetadataDialog)
        self.metadataNotesEdit.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setFamily("Droid Sans")
        font.setPointSize(10)
        self.metadataNotesEdit.setFont(font)
        self.metadataNotesEdit.setMaxLength(100)
        self.metadataNotesEdit.setCursorPosition(0)
        self.metadataNotesEdit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.metadataNotesEdit.setObjectName("metadataNotesEdit")
        self.gridLayout.addWidget(self.metadataNotesEdit, 3, 0, 1, 1)

        self.retranslateUi(MetadataDialog)
        self.buttonBox.accepted.connect(MetadataDialog.accept)
        self.buttonBox.rejected.connect(MetadataDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MetadataDialog)

    def retranslateUi(self, MetadataDialog):
        _translate = QtCore.QCoreApplication.translate
        MetadataDialog.setWindowTitle(_translate("MetadataDialog", "Metadata"))
        self.label.setText(_translate("MetadataDialog", "Metadata"))
        self.label_2.setText(_translate("MetadataDialog", "Observation Notes"))

