# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'instrumentAttributes.ui'
#
# Created: Mon May 16 15:20:35 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_InstrumentAttributesDialog(object):
    def setupUi(self, InstrumentAttributesDialog):
        InstrumentAttributesDialog.setObjectName("InstrumentAttributesDialog")
        InstrumentAttributesDialog.resize(523, 624)
        InstrumentAttributesDialog.setMinimumSize(QtCore.QSize(500, 603))
        InstrumentAttributesDialog.setMaximumSize(QtCore.QSize(1000, 1000))
        self.gridLayout_3 = QtGui.QGridLayout(InstrumentAttributesDialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtGui.QGroupBox(InstrumentAttributesDialog)
        self.groupBox.setStyleSheet("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.gridLayout_2.addLayout(self.horizontalLayout_13, 1, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setMinimumSize(QtCore.QSize(30, 35))
        self.label_4.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.Chan0LabelEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan0LabelEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan0LabelEdit.setMaximumSize(QtCore.QSize(160, 16777215))
        self.Chan0LabelEdit.setMaxLength(12)
        self.Chan0LabelEdit.setObjectName("Chan0LabelEdit")
        self.horizontalLayout_4.addWidget(self.Chan0LabelEdit)
        self.label_13 = QtGui.QLabel(self.groupBox)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_4.addWidget(self.label_13)
        self.Chan0ColourLineEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan0ColourLineEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan0ColourLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Chan0ColourLineEdit.setMaxLength(7)
        self.Chan0ColourLineEdit.setObjectName("Chan0ColourLineEdit")
        self.horizontalLayout_4.addWidget(self.Chan0ColourLineEdit)
        self.PickerButton0 = QtGui.QPushButton(self.groupBox)
        self.PickerButton0.setMinimumSize(QtCore.QSize(107, 27))
        self.PickerButton0.setMaximumSize(QtCore.QSize(100, 16777215))
        self.PickerButton0.setObjectName("PickerButton0")
        self.horizontalLayout_4.addWidget(self.PickerButton0)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setMinimumSize(QtCore.QSize(30, 35))
        self.label_9.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_9.addWidget(self.label_9)
        self.Chan5LabelEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan5LabelEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan5LabelEdit.setMaximumSize(QtCore.QSize(160, 16777215))
        self.Chan5LabelEdit.setMaxLength(12)
        self.Chan5LabelEdit.setObjectName("Chan5LabelEdit")
        self.horizontalLayout_9.addWidget(self.Chan5LabelEdit)
        self.label_22 = QtGui.QLabel(self.groupBox)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_9.addWidget(self.label_22)
        self.Chan5ColourLineEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan5ColourLineEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan5ColourLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Chan5ColourLineEdit.setMaxLength(7)
        self.Chan5ColourLineEdit.setObjectName("Chan5ColourLineEdit")
        self.horizontalLayout_9.addWidget(self.Chan5ColourLineEdit)
        self.PickerButton5 = QtGui.QPushButton(self.groupBox)
        self.PickerButton5.setMinimumSize(QtCore.QSize(107, 27))
        self.PickerButton5.setMaximumSize(QtCore.QSize(100, 16777215))
        self.PickerButton5.setObjectName("PickerButton5")
        self.horizontalLayout_9.addWidget(self.PickerButton5)
        self.gridLayout_2.addLayout(self.horizontalLayout_9, 7, 0, 1, 1)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_11 = QtGui.QLabel(self.groupBox)
        self.label_11.setMinimumSize(QtCore.QSize(30, 35))
        self.label_11.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_11.addWidget(self.label_11)
        self.Chan7LabelEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan7LabelEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan7LabelEdit.setMaximumSize(QtCore.QSize(160, 16777215))
        self.Chan7LabelEdit.setMaxLength(12)
        self.Chan7LabelEdit.setObjectName("Chan7LabelEdit")
        self.horizontalLayout_11.addWidget(self.Chan7LabelEdit)
        self.label_24 = QtGui.QLabel(self.groupBox)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_11.addWidget(self.label_24)
        self.Chan7ColourLineEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan7ColourLineEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan7ColourLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Chan7ColourLineEdit.setMaxLength(7)
        self.Chan7ColourLineEdit.setObjectName("Chan7ColourLineEdit")
        self.horizontalLayout_11.addWidget(self.Chan7ColourLineEdit)
        self.PickerButton7 = QtGui.QPushButton(self.groupBox)
        self.PickerButton7.setMinimumSize(QtCore.QSize(107, 27))
        self.PickerButton7.setMaximumSize(QtCore.QSize(100, 16777215))
        self.PickerButton7.setObjectName("PickerButton7")
        self.horizontalLayout_11.addWidget(self.PickerButton7)
        self.gridLayout_2.addLayout(self.horizontalLayout_11, 9, 0, 1, 1)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_12 = QtGui.QLabel(self.groupBox)
        self.label_12.setMinimumSize(QtCore.QSize(30, 35))
        self.label_12.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_12.addWidget(self.label_12)
        self.Chan8LabelEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan8LabelEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan8LabelEdit.setMaximumSize(QtCore.QSize(160, 16777215))
        self.Chan8LabelEdit.setMaxLength(12)
        self.Chan8LabelEdit.setObjectName("Chan8LabelEdit")
        self.horizontalLayout_12.addWidget(self.Chan8LabelEdit)
        self.label_25 = QtGui.QLabel(self.groupBox)
        self.label_25.setObjectName("label_25")
        self.horizontalLayout_12.addWidget(self.label_25)
        self.Chan8ColourLineEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan8ColourLineEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan8ColourLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Chan8ColourLineEdit.setMaxLength(7)
        self.Chan8ColourLineEdit.setObjectName("Chan8ColourLineEdit")
        self.horizontalLayout_12.addWidget(self.Chan8ColourLineEdit)
        self.PickerButton8 = QtGui.QPushButton(self.groupBox)
        self.PickerButton8.setMinimumSize(QtCore.QSize(107, 27))
        self.PickerButton8.setMaximumSize(QtCore.QSize(100, 16777215))
        self.PickerButton8.setObjectName("PickerButton8")
        self.horizontalLayout_12.addWidget(self.PickerButton8)
        self.gridLayout_2.addLayout(self.horizontalLayout_12, 10, 0, 1, 1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setMinimumSize(QtCore.QSize(30, 35))
        self.label_7.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_7.addWidget(self.label_7)
        self.Chan3LabelEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan3LabelEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan3LabelEdit.setMaximumSize(QtCore.QSize(160, 16777215))
        self.Chan3LabelEdit.setMaxLength(12)
        self.Chan3LabelEdit.setObjectName("Chan3LabelEdit")
        self.horizontalLayout_7.addWidget(self.Chan3LabelEdit)
        self.label_20 = QtGui.QLabel(self.groupBox)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_7.addWidget(self.label_20)
        self.Chan3ColourLineEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan3ColourLineEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan3ColourLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Chan3ColourLineEdit.setMaxLength(7)
        self.Chan3ColourLineEdit.setObjectName("Chan3ColourLineEdit")
        self.horizontalLayout_7.addWidget(self.Chan3ColourLineEdit)
        self.PickerButton3 = QtGui.QPushButton(self.groupBox)
        self.PickerButton3.setMinimumSize(QtCore.QSize(107, 27))
        self.PickerButton3.setMaximumSize(QtCore.QSize(100, 16777215))
        self.PickerButton3.setObjectName("PickerButton3")
        self.horizontalLayout_7.addWidget(self.PickerButton3)
        self.gridLayout_2.addLayout(self.horizontalLayout_7, 5, 0, 1, 1)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_10 = QtGui.QLabel(self.groupBox)
        self.label_10.setMinimumSize(QtCore.QSize(30, 34))
        self.label_10.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_10.addWidget(self.label_10)
        self.Chan6LabelEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan6LabelEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan6LabelEdit.setMaximumSize(QtCore.QSize(160, 16777215))
        self.Chan6LabelEdit.setMaxLength(12)
        self.Chan6LabelEdit.setObjectName("Chan6LabelEdit")
        self.horizontalLayout_10.addWidget(self.Chan6LabelEdit)
        self.label_23 = QtGui.QLabel(self.groupBox)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_10.addWidget(self.label_23)
        self.Chan6ColourLineEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan6ColourLineEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan6ColourLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Chan6ColourLineEdit.setMaxLength(7)
        self.Chan6ColourLineEdit.setObjectName("Chan6ColourLineEdit")
        self.horizontalLayout_10.addWidget(self.Chan6ColourLineEdit)
        self.PickerButton6 = QtGui.QPushButton(self.groupBox)
        self.PickerButton6.setMinimumSize(QtCore.QSize(107, 27))
        self.PickerButton6.setMaximumSize(QtCore.QSize(100, 16777215))
        self.PickerButton6.setObjectName("PickerButton6")
        self.horizontalLayout_10.addWidget(self.PickerButton6)
        self.gridLayout_2.addLayout(self.horizontalLayout_10, 8, 0, 1, 1)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setMinimumSize(QtCore.QSize(30, 35))
        self.label_8.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_8.addWidget(self.label_8)
        self.Chan4LabelEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan4LabelEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan4LabelEdit.setMaximumSize(QtCore.QSize(160, 16777215))
        self.Chan4LabelEdit.setMaxLength(12)
        self.Chan4LabelEdit.setObjectName("Chan4LabelEdit")
        self.horizontalLayout_8.addWidget(self.Chan4LabelEdit)
        self.label_21 = QtGui.QLabel(self.groupBox)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_8.addWidget(self.label_21)
        self.Chan4ColourLineEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan4ColourLineEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan4ColourLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Chan4ColourLineEdit.setMaxLength(7)
        self.Chan4ColourLineEdit.setObjectName("Chan4ColourLineEdit")
        self.horizontalLayout_8.addWidget(self.Chan4ColourLineEdit)
        self.PickerButton4 = QtGui.QPushButton(self.groupBox)
        self.PickerButton4.setMinimumSize(QtCore.QSize(107, 27))
        self.PickerButton4.setMaximumSize(QtCore.QSize(100, 16777215))
        self.PickerButton4.setObjectName("PickerButton4")
        self.horizontalLayout_8.addWidget(self.PickerButton4)
        self.gridLayout_2.addLayout(self.horizontalLayout_8, 6, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setMinimumSize(QtCore.QSize(30, 35))
        self.label_5.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.Chan1LabelEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan1LabelEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan1LabelEdit.setMaximumSize(QtCore.QSize(160, 16777215))
        self.Chan1LabelEdit.setMaxLength(12)
        self.Chan1LabelEdit.setObjectName("Chan1LabelEdit")
        self.horizontalLayout_5.addWidget(self.Chan1LabelEdit)
        self.label_18 = QtGui.QLabel(self.groupBox)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_5.addWidget(self.label_18)
        self.Chan1ColourLineEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan1ColourLineEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan1ColourLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Chan1ColourLineEdit.setMaxLength(7)
        self.Chan1ColourLineEdit.setObjectName("Chan1ColourLineEdit")
        self.horizontalLayout_5.addWidget(self.Chan1ColourLineEdit)
        self.PickerButton1 = QtGui.QPushButton(self.groupBox)
        self.PickerButton1.setMinimumSize(QtCore.QSize(107, 27))
        self.PickerButton1.setMaximumSize(QtCore.QSize(100, 16777215))
        self.PickerButton1.setObjectName("PickerButton1")
        self.horizontalLayout_5.addWidget(self.PickerButton1)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 3, 0, 1, 1)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setMinimumSize(QtCore.QSize(30, 34))
        self.label_6.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.Chan2LabelEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan2LabelEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan2LabelEdit.setMaximumSize(QtCore.QSize(160, 16777215))
        self.Chan2LabelEdit.setMaxLength(12)
        self.Chan2LabelEdit.setObjectName("Chan2LabelEdit")
        self.horizontalLayout_6.addWidget(self.Chan2LabelEdit)
        self.label_19 = QtGui.QLabel(self.groupBox)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_6.addWidget(self.label_19)
        self.Chan2ColourLineEdit = QtGui.QLineEdit(self.groupBox)
        self.Chan2ColourLineEdit.setMinimumSize(QtCore.QSize(120, 27))
        self.Chan2ColourLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Chan2ColourLineEdit.setMaxLength(7)
        self.Chan2ColourLineEdit.setObjectName("Chan2ColourLineEdit")
        self.horizontalLayout_6.addWidget(self.Chan2ColourLineEdit)
        self.PickerButton2 = QtGui.QPushButton(self.groupBox)
        self.PickerButton2.setMinimumSize(QtCore.QSize(107, 27))
        self.PickerButton2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.PickerButton2.setObjectName("PickerButton2")
        self.horizontalLayout_6.addWidget(self.PickerButton2)
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 4, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 3, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_15 = QtGui.QLabel(self.groupBox)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout.addWidget(self.label_15)
        self.StaribusPortLineEdit = QtGui.QLineEdit(self.groupBox)
        self.StaribusPortLineEdit.setObjectName("StaribusPortLineEdit")
        self.horizontalLayout.addWidget(self.StaribusPortLineEdit)
        self.RS485checkBox = QtGui.QCheckBox(self.groupBox)
        self.RS485checkBox.setObjectName("RS485checkBox")
        self.horizontalLayout.addWidget(self.RS485checkBox)
        self.StaribusAutodetectCheckBox = QtGui.QCheckBox(self.groupBox)
        self.StaribusAutodetectCheckBox.setObjectName("StaribusAutodetectCheckBox")
        self.horizontalLayout.addWidget(self.StaribusAutodetectCheckBox)
        self.Staribus2StarinetCheckBox = QtGui.QCheckBox(self.groupBox)
        self.Staribus2StarinetCheckBox.setObjectName("Staribus2StarinetCheckBox")
        self.horizontalLayout.addWidget(self.Staribus2StarinetCheckBox)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setMinimumSize(QtCore.QSize(102, 0))
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.comboBox = QtGui.QComboBox(self.groupBox)
        self.comboBox.setMaxCount(253)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.label_16 = QtGui.QLabel(self.groupBox)
        self.label_16.setMinimumSize(QtCore.QSize(56, 0))
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_2.addWidget(self.label_16)
        self.BaudrateCombobox = QtGui.QComboBox(self.groupBox)
        self.BaudrateCombobox.setObjectName("BaudrateCombobox")
        self.horizontalLayout_2.addWidget(self.BaudrateCombobox)
        self.label_17 = QtGui.QLabel(self.groupBox)
        self.label_17.setMinimumSize(QtCore.QSize(53, 0))
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_2.addWidget(self.label_17)
        self.TimeoutCombobox = QtGui.QComboBox(self.groupBox)
        self.TimeoutCombobox.setObjectName("TimeoutCombobox")
        self.horizontalLayout_2.addWidget(self.TimeoutCombobox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.StarinetAddressLineEdit = QtGui.QLineEdit(self.groupBox)
        self.StarinetAddressLineEdit.setMinimumSize(QtCore.QSize(129, 27))
        self.StarinetAddressLineEdit.setMaxLength(15)
        self.StarinetAddressLineEdit.setObjectName("StarinetAddressLineEdit")
        self.horizontalLayout_3.addWidget(self.StarinetAddressLineEdit)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.StarinetPortLineEdit = QtGui.QLineEdit(self.groupBox)
        self.StarinetPortLineEdit.setMinimumSize(QtCore.QSize(50, 27))
        self.StarinetPortLineEdit.setMaxLength(5)
        self.StarinetPortLineEdit.setObjectName("StarinetPortLineEdit")
        self.horizontalLayout_3.addWidget(self.StarinetPortLineEdit)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 2, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem2, 4, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(InstrumentAttributesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.RestoreDefaults)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_3.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(InstrumentAttributesDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), InstrumentAttributesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), InstrumentAttributesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InstrumentAttributesDialog)

    def retranslateUi(self, InstrumentAttributesDialog):
        InstrumentAttributesDialog.setWindowTitle(QtGui.QApplication.translate("InstrumentAttributesDialog", "Instrument Attributes", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("InstrumentAttributesDialog", "Instrument Attributes", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Label 0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Colour", None, QtGui.QApplication.UnicodeUTF8))
        self.PickerButton0.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Colour Picker", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Label 5", None, QtGui.QApplication.UnicodeUTF8))
        self.label_22.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Colour", None, QtGui.QApplication.UnicodeUTF8))
        self.PickerButton5.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Colour Picker", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Label 7", None, QtGui.QApplication.UnicodeUTF8))
        self.label_24.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Colour", None, QtGui.QApplication.UnicodeUTF8))
        self.PickerButton7.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Colour Picker", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Label 8", None, QtGui.QApplication.UnicodeUTF8))
        self.label_25.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Colour", None, QtGui.QApplication.UnicodeUTF8))
        self.PickerButton8.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Colour Picker", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Label 3", None, QtGui.QApplication.UnicodeUTF8))
        self.label_20.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Colour", None, QtGui.QApplication.UnicodeUTF8))
        self.PickerButton3.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Colour Picker", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Label 6", None, QtGui.QApplication.UnicodeUTF8))
        self.label_23.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Colour", None, QtGui.QApplication.UnicodeUTF8))
        self.PickerButton6.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Colour Picker", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Label 4", None, QtGui.QApplication.UnicodeUTF8))
        self.label_21.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Colour", None, QtGui.QApplication.UnicodeUTF8))
        self.PickerButton4.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Colour Picker", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Label 1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Colour", None, QtGui.QApplication.UnicodeUTF8))
        self.PickerButton1.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Colour Picker", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Label 2", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Colour", None, QtGui.QApplication.UnicodeUTF8))
        self.PickerButton2.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Colour Picker", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Staribus Port", None, QtGui.QApplication.UnicodeUTF8))
        self.RS485checkBox.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "RS485", None, QtGui.QApplication.UnicodeUTF8))
        self.StaribusAutodetectCheckBox.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Autodetect", None, QtGui.QApplication.UnicodeUTF8))
        self.Staribus2StarinetCheckBox.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Staribus2Starinet", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Staribus Address", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Baudrate", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Timeout", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Starinet IP Address", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("InstrumentAttributesDialog", "Starinet Port", None, QtGui.QApplication.UnicodeUTF8))

