# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'instrumentAttributes.ui'
#
# Created: Tue Sep 15 10:02:39 2015
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

class Ui_InstrumentAttributesDialog(object):
    def setupUi(self, InstrumentAttributesDialog):
        InstrumentAttributesDialog.setObjectName(_fromUtf8("InstrumentAttributesDialog"))
        InstrumentAttributesDialog.resize(523, 624)
        InstrumentAttributesDialog.setMinimumSize(QtCore.QSize(500, 603))
        InstrumentAttributesDialog.setMaximumSize(QtCore.QSize(1000, 1000))
        self.gridLayout_3 = QtGui.QGridLayout(InstrumentAttributesDialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.groupBox = QtGui.QGroupBox(InstrumentAttributesDialog)
        self.groupBox.setStyleSheet(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem, 2, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtGui.QComboBox(self.groupBox)
        self.comboBox.setMaxCount(253)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.horizontalLayout.addWidget(self.comboBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.StarinetAddressLineEdit = QtGui.QLineEdit(self.groupBox)
        self.StarinetAddressLineEdit.setMinimumSize(QtCore.QSize(129, 27))
        self.StarinetAddressLineEdit.setMaxLength(15)
        self.StarinetAddressLineEdit.setObjectName(_fromUtf8("StarinetAddressLineEdit"))
        self.horizontalLayout_2.addWidget(self.StarinetAddressLineEdit)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.StarinetPortLineEdit = QtGui.QLineEdit(self.groupBox)
        self.StarinetPortLineEdit.setMinimumSize(QtCore.QSize(170, 27))
        self.StarinetPortLineEdit.setMaxLength(5)
        self.StarinetPortLineEdit.setObjectName(_fromUtf8("StarinetPortLineEdit"))
        self.horizontalLayout_3.addWidget(self.StarinetPortLineEdit)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setMinimumSize(QtCore.QSize(67, 35))
        self.label_4.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_4.addWidget(self.label_4)
        self.Chan0LabelEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan0LabelEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan0LabelEdit.setMaximumSize(QtCore.QSize(160, 16777215))
        self.Chan0LabelEdit.setMaxLength(12)
        self.Chan0LabelEdit.setObjectName(_fromUtf8("Chan0LabelEdit"))
        self.horizontalLayout_4.addWidget(self.Chan0LabelEdit)
        self.Chan0ColourLineEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan0ColourLineEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan0ColourLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Chan0ColourLineEdit.setMaxLength(7)
        self.Chan0ColourLineEdit.setObjectName(_fromUtf8("Chan0ColourLineEdit"))
        self.horizontalLayout_4.addWidget(self.Chan0ColourLineEdit)
        self.PickerButton0 = QtGui.QPushButton(self.groupBox)
        self.PickerButton0.setMinimumSize(QtCore.QSize(107, 27))
        self.PickerButton0.setMaximumSize(QtCore.QSize(100, 16777215))
        self.PickerButton0.setObjectName(_fromUtf8("PickerButton0"))
        self.horizontalLayout_4.addWidget(self.PickerButton0)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setMinimumSize(QtCore.QSize(66, 35))
        self.label_5.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_5.addWidget(self.label_5)
        self.Chan1LabelEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan1LabelEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan1LabelEdit.setMaximumSize(QtCore.QSize(160, 16777215))
        self.Chan1LabelEdit.setMaxLength(12)
        self.Chan1LabelEdit.setObjectName(_fromUtf8("Chan1LabelEdit"))
        self.horizontalLayout_5.addWidget(self.Chan1LabelEdit)
        self.Chan1ColourLineEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan1ColourLineEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan1ColourLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Chan1ColourLineEdit.setMaxLength(7)
        self.Chan1ColourLineEdit.setObjectName(_fromUtf8("Chan1ColourLineEdit"))
        self.horizontalLayout_5.addWidget(self.Chan1ColourLineEdit)
        self.PickerButton1 = QtGui.QPushButton(self.groupBox)
        self.PickerButton1.setMinimumSize(QtCore.QSize(107, 27))
        self.PickerButton1.setMaximumSize(QtCore.QSize(100, 16777215))
        self.PickerButton1.setObjectName(_fromUtf8("PickerButton1"))
        self.horizontalLayout_5.addWidget(self.PickerButton1)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 3, 0, 1, 1)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setMinimumSize(QtCore.QSize(67, 34))
        self.label_6.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_6.addWidget(self.label_6)
        self.Chan2LabelEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan2LabelEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan2LabelEdit.setMaximumSize(QtCore.QSize(160, 16777215))
        self.Chan2LabelEdit.setMaxLength(12)
        self.Chan2LabelEdit.setObjectName(_fromUtf8("Chan2LabelEdit"))
        self.horizontalLayout_6.addWidget(self.Chan2LabelEdit)
        self.Chan2ColourLineEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan2ColourLineEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan2ColourLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Chan2ColourLineEdit.setMaxLength(7)
        self.Chan2ColourLineEdit.setObjectName(_fromUtf8("Chan2ColourLineEdit"))
        self.horizontalLayout_6.addWidget(self.Chan2ColourLineEdit)
        self.PickerButton2 = QtGui.QPushButton(self.groupBox)
        self.PickerButton2.setMinimumSize(QtCore.QSize(107, 27))
        self.PickerButton2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.PickerButton2.setObjectName(_fromUtf8("PickerButton2"))
        self.horizontalLayout_6.addWidget(self.PickerButton2)
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 4, 0, 1, 1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setMinimumSize(QtCore.QSize(67, 35))
        self.label_7.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_7.addWidget(self.label_7)
        self.Chan3LabelEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan3LabelEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan3LabelEdit.setMaximumSize(QtCore.QSize(160, 16777215))
        self.Chan3LabelEdit.setMaxLength(12)
        self.Chan3LabelEdit.setObjectName(_fromUtf8("Chan3LabelEdit"))
        self.horizontalLayout_7.addWidget(self.Chan3LabelEdit)
        self.Chan3ColourLineEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan3ColourLineEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan3ColourLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Chan3ColourLineEdit.setMaxLength(7)
        self.Chan3ColourLineEdit.setObjectName(_fromUtf8("Chan3ColourLineEdit"))
        self.horizontalLayout_7.addWidget(self.Chan3ColourLineEdit)
        self.PickerButton3 = QtGui.QPushButton(self.groupBox)
        self.PickerButton3.setMinimumSize(QtCore.QSize(107, 27))
        self.PickerButton3.setMaximumSize(QtCore.QSize(100, 16777215))
        self.PickerButton3.setObjectName(_fromUtf8("PickerButton3"))
        self.horizontalLayout_7.addWidget(self.PickerButton3)
        self.gridLayout_2.addLayout(self.horizontalLayout_7, 5, 0, 1, 1)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setMinimumSize(QtCore.QSize(67, 35))
        self.label_8.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout_8.addWidget(self.label_8)
        self.Chan4LabelEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan4LabelEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan4LabelEdit.setMaximumSize(QtCore.QSize(160, 16777215))
        self.Chan4LabelEdit.setMaxLength(12)
        self.Chan4LabelEdit.setObjectName(_fromUtf8("Chan4LabelEdit"))
        self.horizontalLayout_8.addWidget(self.Chan4LabelEdit)
        self.Chan4ColourLineEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan4ColourLineEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan4ColourLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Chan4ColourLineEdit.setMaxLength(7)
        self.Chan4ColourLineEdit.setObjectName(_fromUtf8("Chan4ColourLineEdit"))
        self.horizontalLayout_8.addWidget(self.Chan4ColourLineEdit)
        self.PickerButton4 = QtGui.QPushButton(self.groupBox)
        self.PickerButton4.setMinimumSize(QtCore.QSize(107, 27))
        self.PickerButton4.setMaximumSize(QtCore.QSize(100, 16777215))
        self.PickerButton4.setObjectName(_fromUtf8("PickerButton4"))
        self.horizontalLayout_8.addWidget(self.PickerButton4)
        self.gridLayout_2.addLayout(self.horizontalLayout_8, 6, 0, 1, 1)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setMinimumSize(QtCore.QSize(67, 35))
        self.label_9.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_9.addWidget(self.label_9)
        self.Chan5LabelEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan5LabelEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan5LabelEdit.setMaximumSize(QtCore.QSize(160, 16777215))
        self.Chan5LabelEdit.setMaxLength(12)
        self.Chan5LabelEdit.setObjectName(_fromUtf8("Chan5LabelEdit"))
        self.horizontalLayout_9.addWidget(self.Chan5LabelEdit)
        self.Chan5ColourLineEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan5ColourLineEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan5ColourLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Chan5ColourLineEdit.setMaxLength(7)
        self.Chan5ColourLineEdit.setObjectName(_fromUtf8("Chan5ColourLineEdit"))
        self.horizontalLayout_9.addWidget(self.Chan5ColourLineEdit)
        self.PickerButton5 = QtGui.QPushButton(self.groupBox)
        self.PickerButton5.setMinimumSize(QtCore.QSize(107, 27))
        self.PickerButton5.setMaximumSize(QtCore.QSize(100, 16777215))
        self.PickerButton5.setObjectName(_fromUtf8("PickerButton5"))
        self.horizontalLayout_9.addWidget(self.PickerButton5)
        self.gridLayout_2.addLayout(self.horizontalLayout_9, 7, 0, 1, 1)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.label_10 = QtGui.QLabel(self.groupBox)
        self.label_10.setMinimumSize(QtCore.QSize(67, 34))
        self.label_10.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout_10.addWidget(self.label_10)
        self.Chan6LabelEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan6LabelEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan6LabelEdit.setMaximumSize(QtCore.QSize(160, 16777215))
        self.Chan6LabelEdit.setMaxLength(12)
        self.Chan6LabelEdit.setObjectName(_fromUtf8("Chan6LabelEdit"))
        self.horizontalLayout_10.addWidget(self.Chan6LabelEdit)
        self.Chan6ColourLineEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan6ColourLineEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan6ColourLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Chan6ColourLineEdit.setMaxLength(7)
        self.Chan6ColourLineEdit.setObjectName(_fromUtf8("Chan6ColourLineEdit"))
        self.horizontalLayout_10.addWidget(self.Chan6ColourLineEdit)
        self.PickerButton6 = QtGui.QPushButton(self.groupBox)
        self.PickerButton6.setMinimumSize(QtCore.QSize(107, 27))
        self.PickerButton6.setMaximumSize(QtCore.QSize(100, 16777215))
        self.PickerButton6.setObjectName(_fromUtf8("PickerButton6"))
        self.horizontalLayout_10.addWidget(self.PickerButton6)
        self.gridLayout_2.addLayout(self.horizontalLayout_10, 8, 0, 1, 1)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.label_11 = QtGui.QLabel(self.groupBox)
        self.label_11.setMinimumSize(QtCore.QSize(67, 35))
        self.label_11.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout_11.addWidget(self.label_11)
        self.Chan7LabelEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan7LabelEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan7LabelEdit.setMaximumSize(QtCore.QSize(160, 16777215))
        self.Chan7LabelEdit.setMaxLength(12)
        self.Chan7LabelEdit.setObjectName(_fromUtf8("Chan7LabelEdit"))
        self.horizontalLayout_11.addWidget(self.Chan7LabelEdit)
        self.Chan7ColourLineEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan7ColourLineEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan7ColourLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Chan7ColourLineEdit.setMaxLength(7)
        self.Chan7ColourLineEdit.setObjectName(_fromUtf8("Chan7ColourLineEdit"))
        self.horizontalLayout_11.addWidget(self.Chan7ColourLineEdit)
        self.PickerButton7 = QtGui.QPushButton(self.groupBox)
        self.PickerButton7.setMinimumSize(QtCore.QSize(107, 27))
        self.PickerButton7.setMaximumSize(QtCore.QSize(100, 16777215))
        self.PickerButton7.setObjectName(_fromUtf8("PickerButton7"))
        self.horizontalLayout_11.addWidget(self.PickerButton7)
        self.gridLayout_2.addLayout(self.horizontalLayout_11, 9, 0, 1, 1)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.label_12 = QtGui.QLabel(self.groupBox)
        self.label_12.setMinimumSize(QtCore.QSize(67, 35))
        self.label_12.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.horizontalLayout_12.addWidget(self.label_12)
        self.Chan8LabelEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan8LabelEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan8LabelEdit.setMaximumSize(QtCore.QSize(160, 16777215))
        self.Chan8LabelEdit.setMaxLength(12)
        self.Chan8LabelEdit.setObjectName(_fromUtf8("Chan8LabelEdit"))
        self.horizontalLayout_12.addWidget(self.Chan8LabelEdit)
        self.Chan8ColourLineEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan8ColourLineEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan8ColourLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Chan8ColourLineEdit.setMaxLength(7)
        self.Chan8ColourLineEdit.setObjectName(_fromUtf8("Chan8ColourLineEdit"))
        self.horizontalLayout_12.addWidget(self.Chan8ColourLineEdit)
        self.PickerButton8 = QtGui.QPushButton(self.groupBox)
        self.PickerButton8.setMinimumSize(QtCore.QSize(107, 27))
        self.PickerButton8.setMaximumSize(QtCore.QSize(100, 16777215))
        self.PickerButton8.setObjectName(_fromUtf8("PickerButton8"))
        self.horizontalLayout_12.addWidget(self.PickerButton8)
        self.gridLayout_2.addLayout(self.horizontalLayout_12, 10, 0, 1, 1)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        spacerItem4 = QtGui.QSpacerItem(80, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem4)
        self.label_13 = QtGui.QLabel(self.groupBox)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.horizontalLayout_13.addWidget(self.label_13)
        spacerItem5 = QtGui.QSpacerItem(120, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem5)
        self.label_14 = QtGui.QLabel(self.groupBox)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.horizontalLayout_13.addWidget(self.label_14)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem6)
        self.gridLayout_2.addLayout(self.horizontalLayout_13, 1, 0, 1, 1)
        spacerItem7 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem7, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(InstrumentAttributesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_3.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(InstrumentAttributesDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), InstrumentAttributesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), InstrumentAttributesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InstrumentAttributesDialog)

    def retranslateUi(self, InstrumentAttributesDialog):
        InstrumentAttributesDialog.setWindowTitle(_translate("InstrumentAttributesDialog", "Instrument Attributes", None))
        self.groupBox.setTitle(_translate("InstrumentAttributesDialog", "Instrument Attributes", None))
        self.label.setText(_translate("InstrumentAttributesDialog", "Staribus Address", None))
        self.label_2.setText(_translate("InstrumentAttributesDialog", "Starinet IP Address", None))
        self.label_3.setText(_translate("InstrumentAttributesDialog", "Starinet Port", None))
        self.label_4.setText(_translate("InstrumentAttributesDialog", "Channel 0", None))
        self.PickerButton0.setText(_translate("InstrumentAttributesDialog", "Colour Picker", None))
        self.label_5.setText(_translate("InstrumentAttributesDialog", "Channel 1", None))
        self.PickerButton1.setText(_translate("InstrumentAttributesDialog", "Colour Picker", None))
        self.label_6.setText(_translate("InstrumentAttributesDialog", "Channel 2", None))
        self.PickerButton2.setText(_translate("InstrumentAttributesDialog", "Colour Picker", None))
        self.label_7.setText(_translate("InstrumentAttributesDialog", "Channel 3", None))
        self.PickerButton3.setText(_translate("InstrumentAttributesDialog", "Colour Picker", None))
        self.label_8.setText(_translate("InstrumentAttributesDialog", "Channel 4", None))
        self.PickerButton4.setText(_translate("InstrumentAttributesDialog", "Colour Picker", None))
        self.label_9.setText(_translate("InstrumentAttributesDialog", "Channel 5", None))
        self.PickerButton5.setText(_translate("InstrumentAttributesDialog", "Colour Picker", None))
        self.label_10.setText(_translate("InstrumentAttributesDialog", "Channel 6", None))
        self.PickerButton6.setText(_translate("InstrumentAttributesDialog", "Colour Picker", None))
        self.label_11.setText(_translate("InstrumentAttributesDialog", "Channel 7", None))
        self.PickerButton7.setText(_translate("InstrumentAttributesDialog", "Colour Picker", None))
        self.label_12.setText(_translate("InstrumentAttributesDialog", "Channel 8", None))
        self.PickerButton8.setText(_translate("InstrumentAttributesDialog", "Colour Picker", None))
        self.label_13.setText(_translate("InstrumentAttributesDialog", "Label", None))
        self.label_14.setText(_translate("InstrumentAttributesDialog", "Colour", None))

