# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configuration.ui'
#
# Created: Tue Sep 15 19:30:17 2015
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

class Ui_ConfigurationDialog(object):
    def setupUi(self, ConfigurationDialog):
        ConfigurationDialog.setObjectName(_fromUtf8("ConfigurationDialog"))
        ConfigurationDialog.resize(699, 619)
        self.gridLayout = QtGui.QGridLayout(ConfigurationDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(ConfigurationDialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tab)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.groupBox_3 = QtGui.QGroupBox(self.tab)
        self.groupBox_3.setStyleSheet(_fromUtf8(""))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.horizontalLayout_30 = QtGui.QHBoxLayout()
        self.horizontalLayout_30.setObjectName(_fromUtf8("horizontalLayout_30"))
        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_30.addWidget(self.label_4)
        self.relayCheckBox = QtGui.QCheckBox(self.groupBox_3)
        self.relayCheckBox.setObjectName(_fromUtf8("relayCheckBox"))
        self.horizontalLayout_30.addWidget(self.relayCheckBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_30.addItem(spacerItem)
        self.gridLayout_5.addLayout(self.horizontalLayout_30, 0, 0, 1, 1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_7 = QtGui.QLabel(self.groupBox_3)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_7.addWidget(self.label_7)
        self.ipAddressLineEdit = QtGui.QLineEdit(self.groupBox_3)
        self.ipAddressLineEdit.setObjectName(_fromUtf8("ipAddressLineEdit"))
        self.horizontalLayout_7.addWidget(self.ipAddressLineEdit)
        self.label_8 = QtGui.QLabel(self.groupBox_3)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout_7.addWidget(self.label_8)
        self.portLineEdit = QtGui.QLineEdit(self.groupBox_3)
        self.portLineEdit.setObjectName(_fromUtf8("portLineEdit"))
        self.horizontalLayout_7.addWidget(self.portLineEdit)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.gridLayout_5.addLayout(self.horizontalLayout_7, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_3, 2, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(self.tab)
        self.groupBox_2.setStyleSheet(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_5.addWidget(self.label_5)
        self.baudrateComboBox = QtGui.QComboBox(self.groupBox_2)
        self.baudrateComboBox.setObjectName(_fromUtf8("baudrateComboBox"))
        self.horizontalLayout_5.addWidget(self.baudrateComboBox)
        self.baudrateDefaultCheckBox = QtGui.QCheckBox(self.groupBox_2)
        self.baudrateDefaultCheckBox.setObjectName(_fromUtf8("baudrateDefaultCheckBox"))
        self.horizontalLayout_5.addWidget(self.baudrateDefaultCheckBox)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.gridLayout_3.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_4.addWidget(self.label_3)
        self.serialPortLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.serialPortLineEdit.setObjectName(_fromUtf8("serialPortLineEdit"))
        self.horizontalLayout_4.addWidget(self.serialPortLineEdit)
        self.detectInstrumentPortCheckBox = QtGui.QCheckBox(self.groupBox_2)
        self.detectInstrumentPortCheckBox.setObjectName(_fromUtf8("detectInstrumentPortCheckBox"))
        self.horizontalLayout_4.addWidget(self.detectInstrumentPortCheckBox)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.gridLayout_3.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_6.addWidget(self.label_6)
        self.timeoutComboBox = QtGui.QComboBox(self.groupBox_2)
        self.timeoutComboBox.setObjectName(_fromUtf8("timeoutComboBox"))
        self.horizontalLayout_6.addWidget(self.timeoutComboBox)
        self.serialPortTimeoutCheckBox = QtGui.QCheckBox(self.groupBox_2)
        self.serialPortTimeoutCheckBox.setObjectName(_fromUtf8("serialPortTimeoutCheckBox"))
        self.horizontalLayout_6.addWidget(self.serialPortTimeoutCheckBox)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.gridLayout_3.addLayout(self.horizontalLayout_6, 2, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.groupBox_4 = QtGui.QGroupBox(self.tab)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.horizontalLayout_32 = QtGui.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_32.setObjectName(_fromUtf8("horizontalLayout_32"))
        self.horizontalLayout_31 = QtGui.QHBoxLayout()
        self.horizontalLayout_31.setObjectName(_fromUtf8("horizontalLayout_31"))
        self.S2SCheckBox = QtGui.QCheckBox(self.groupBox_4)
        self.S2SCheckBox.setObjectName(_fromUtf8("S2SCheckBox"))
        self.horizontalLayout_31.addWidget(self.S2SCheckBox)
        self.label_31 = QtGui.QLabel(self.groupBox_4)
        self.label_31.setObjectName(_fromUtf8("label_31"))
        self.horizontalLayout_31.addWidget(self.label_31)
        self.S2SIpAddressLineEdit = QtGui.QLineEdit(self.groupBox_4)
        self.S2SIpAddressLineEdit.setObjectName(_fromUtf8("S2SIpAddressLineEdit"))
        self.horizontalLayout_31.addWidget(self.S2SIpAddressLineEdit)
        self.label_32 = QtGui.QLabel(self.groupBox_4)
        self.label_32.setObjectName(_fromUtf8("label_32"))
        self.horizontalLayout_31.addWidget(self.label_32)
        self.S2SPort = QtGui.QLineEdit(self.groupBox_4)
        self.S2SPort.setObjectName(_fromUtf8("S2SPort"))
        self.horizontalLayout_31.addWidget(self.S2SPort)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_31.addItem(spacerItem5)
        self.horizontalLayout_32.addLayout(self.horizontalLayout_31)
        self.gridLayout_4.addWidget(self.groupBox_4, 3, 0, 1, 1)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem6, 5, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(self.tab)
        self.groupBox.setStyleSheet(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.savepathLineEdit = QtGui.QLineEdit(self.groupBox)
        self.savepathLineEdit.setObjectName(_fromUtf8("savepathLineEdit"))
        self.horizontalLayout_2.addWidget(self.savepathLineEdit)
        self.chooserButton = QtGui.QPushButton(self.groupBox)
        self.chooserButton.setObjectName(_fromUtf8("chooserButton"))
        self.horizontalLayout_2.addWidget(self.chooserButton)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.instrumentComboBox = QtGui.QComboBox(self.groupBox)
        self.instrumentComboBox.setObjectName(_fromUtf8("instrumentComboBox"))
        self.horizontalLayout_3.addWidget(self.instrumentComboBox)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.horizontalLayout_22 = QtGui.QHBoxLayout()
        self.horizontalLayout_22.setObjectName(_fromUtf8("horizontalLayout_22"))
        self.label_30 = QtGui.QLabel(self.groupBox)
        self.label_30.setObjectName(_fromUtf8("label_30"))
        self.horizontalLayout_22.addWidget(self.label_30)
        self.loglevelComboBox = QtGui.QComboBox(self.groupBox)
        self.loglevelComboBox.setObjectName(_fromUtf8("loglevelComboBox"))
        self.horizontalLayout_22.addWidget(self.loglevelComboBox)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_22.addItem(spacerItem8)
        self.gridLayout_2.addLayout(self.horizontalLayout_22, 2, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_5 = QtGui.QGroupBox(self.tab)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.gridLayout_8 = QtGui.QGridLayout(self.groupBox_5)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.horizontalLayout_33 = QtGui.QHBoxLayout()
        self.horizontalLayout_33.setObjectName(_fromUtf8("horizontalLayout_33"))
        self.label_33 = QtGui.QLabel(self.groupBox_5)
        self.label_33.setObjectName(_fromUtf8("label_33"))
        self.horizontalLayout_33.addWidget(self.label_33)
        self.legendLocationComboBox = QtGui.QComboBox(self.groupBox_5)
        self.legendLocationComboBox.setObjectName(_fromUtf8("legendLocationComboBox"))
        self.horizontalLayout_33.addWidget(self.legendLocationComboBox)
        self.label_34 = QtGui.QLabel(self.groupBox_5)
        self.label_34.setObjectName(_fromUtf8("label_34"))
        self.horizontalLayout_33.addWidget(self.label_34)
        self.LegendColSpinBox = QtGui.QSpinBox(self.groupBox_5)
        self.LegendColSpinBox.setMaximum(4)
        self.LegendColSpinBox.setObjectName(_fromUtf8("LegendColSpinBox"))
        self.horizontalLayout_33.addWidget(self.LegendColSpinBox)
        self.label_35 = QtGui.QLabel(self.groupBox_5)
        self.label_35.setObjectName(_fromUtf8("label_35"))
        self.horizontalLayout_33.addWidget(self.label_35)
        self.LegendFontComboBox = QtGui.QComboBox(self.groupBox_5)
        self.LegendFontComboBox.setObjectName(_fromUtf8("LegendFontComboBox"))
        self.horizontalLayout_33.addWidget(self.LegendFontComboBox)
        spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_33.addItem(spacerItem9)
        self.gridLayout_8.addLayout(self.horizontalLayout_33, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_5, 4, 0, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayout_6 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_9 = QtGui.QLabel(self.tab_2)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_8.addWidget(self.label_9)
        self.OyNameLineEdit = QtGui.QLineEdit(self.tab_2)
        self.OyNameLineEdit.setObjectName(_fromUtf8("OyNameLineEdit"))
        self.horizontalLayout_8.addWidget(self.OyNameLineEdit)
        self.gridLayout_6.addLayout(self.horizontalLayout_8, 0, 0, 1, 1)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.label_10 = QtGui.QLabel(self.tab_2)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout_9.addWidget(self.label_10)
        self.OyDescriptionLineEdit = QtGui.QLineEdit(self.tab_2)
        self.OyDescriptionLineEdit.setObjectName(_fromUtf8("OyDescriptionLineEdit"))
        self.horizontalLayout_9.addWidget(self.OyDescriptionLineEdit)
        self.gridLayout_6.addLayout(self.horizontalLayout_9, 1, 0, 1, 1)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.label_11 = QtGui.QLabel(self.tab_2)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout_10.addWidget(self.label_11)
        self.OyEmailLineEdit = QtGui.QLineEdit(self.tab_2)
        self.OyEmailLineEdit.setObjectName(_fromUtf8("OyEmailLineEdit"))
        self.horizontalLayout_10.addWidget(self.OyEmailLineEdit)
        self.gridLayout_6.addLayout(self.horizontalLayout_10, 2, 0, 1, 1)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.label_12 = QtGui.QLabel(self.tab_2)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.horizontalLayout_11.addWidget(self.label_12)
        self.OyTelephoneLineEdit = QtGui.QLineEdit(self.tab_2)
        self.OyTelephoneLineEdit.setObjectName(_fromUtf8("OyTelephoneLineEdit"))
        self.horizontalLayout_11.addWidget(self.OyTelephoneLineEdit)
        self.gridLayout_6.addLayout(self.horizontalLayout_11, 3, 0, 1, 1)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.label_13 = QtGui.QLabel(self.tab_2)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.horizontalLayout_12.addWidget(self.label_13)
        self.OyUrlLineEdit = QtGui.QLineEdit(self.tab_2)
        self.OyUrlLineEdit.setObjectName(_fromUtf8("OyUrlLineEdit"))
        self.horizontalLayout_12.addWidget(self.OyUrlLineEdit)
        self.gridLayout_6.addLayout(self.horizontalLayout_12, 4, 0, 1, 1)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.label_14 = QtGui.QLabel(self.tab_2)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.horizontalLayout_13.addWidget(self.label_14)
        self.OyCountryLineEdit = QtGui.QLineEdit(self.tab_2)
        self.OyCountryLineEdit.setObjectName(_fromUtf8("OyCountryLineEdit"))
        self.horizontalLayout_13.addWidget(self.OyCountryLineEdit)
        self.gridLayout_6.addLayout(self.horizontalLayout_13, 5, 0, 1, 1)
        self.horizontalLayout_14 = QtGui.QHBoxLayout()
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.label_15 = QtGui.QLabel(self.tab_2)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.horizontalLayout_14.addWidget(self.label_15)
        self.OyTimezoneLineEdit = QtGui.QLineEdit(self.tab_2)
        self.OyTimezoneLineEdit.setObjectName(_fromUtf8("OyTimezoneLineEdit"))
        self.horizontalLayout_14.addWidget(self.OyTimezoneLineEdit)
        self.gridLayout_6.addLayout(self.horizontalLayout_14, 6, 0, 1, 1)
        self.horizontalLayout_15 = QtGui.QHBoxLayout()
        self.horizontalLayout_15.setObjectName(_fromUtf8("horizontalLayout_15"))
        self.label_20 = QtGui.QLabel(self.tab_2)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.horizontalLayout_15.addWidget(self.label_20)
        self.OyLongitudeLineEdit = QtGui.QLineEdit(self.tab_2)
        self.OyLongitudeLineEdit.setObjectName(_fromUtf8("OyLongitudeLineEdit"))
        self.horizontalLayout_15.addWidget(self.OyLongitudeLineEdit)
        self.gridLayout_6.addLayout(self.horizontalLayout_15, 7, 0, 1, 1)
        self.horizontalLayout_16 = QtGui.QHBoxLayout()
        self.horizontalLayout_16.setObjectName(_fromUtf8("horizontalLayout_16"))
        self.label_21 = QtGui.QLabel(self.tab_2)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.horizontalLayout_16.addWidget(self.label_21)
        self.OyLatitudeLineEdit = QtGui.QLineEdit(self.tab_2)
        self.OyLatitudeLineEdit.setObjectName(_fromUtf8("OyLatitudeLineEdit"))
        self.horizontalLayout_16.addWidget(self.OyLatitudeLineEdit)
        self.gridLayout_6.addLayout(self.horizontalLayout_16, 8, 0, 1, 1)
        self.horizontalLayout_17 = QtGui.QHBoxLayout()
        self.horizontalLayout_17.setObjectName(_fromUtf8("horizontalLayout_17"))
        self.label_22 = QtGui.QLabel(self.tab_2)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.horizontalLayout_17.addWidget(self.label_22)
        self.OyHaslLineEdit = QtGui.QLineEdit(self.tab_2)
        self.OyHaslLineEdit.setObjectName(_fromUtf8("OyHaslLineEdit"))
        self.horizontalLayout_17.addWidget(self.OyHaslLineEdit)
        self.gridLayout_6.addLayout(self.horizontalLayout_17, 9, 0, 1, 1)
        self.horizontalLayout_18 = QtGui.QHBoxLayout()
        self.horizontalLayout_18.setObjectName(_fromUtf8("horizontalLayout_18"))
        self.label_16 = QtGui.QLabel(self.tab_2)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.horizontalLayout_18.addWidget(self.label_16)
        self.OyDatumLineEdit = QtGui.QLineEdit(self.tab_2)
        self.OyDatumLineEdit.setObjectName(_fromUtf8("OyDatumLineEdit"))
        self.horizontalLayout_18.addWidget(self.OyDatumLineEdit)
        self.gridLayout_6.addLayout(self.horizontalLayout_18, 10, 0, 1, 1)
        self.horizontalLayout_19 = QtGui.QHBoxLayout()
        self.horizontalLayout_19.setObjectName(_fromUtf8("horizontalLayout_19"))
        self.label_19 = QtGui.QLabel(self.tab_2)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.horizontalLayout_19.addWidget(self.label_19)
        self.OyModelLineEdit = QtGui.QLineEdit(self.tab_2)
        self.OyModelLineEdit.setObjectName(_fromUtf8("OyModelLineEdit"))
        self.horizontalLayout_19.addWidget(self.OyModelLineEdit)
        self.gridLayout_6.addLayout(self.horizontalLayout_19, 11, 0, 1, 1)
        self.horizontalLayout_20 = QtGui.QHBoxLayout()
        self.horizontalLayout_20.setObjectName(_fromUtf8("horizontalLayout_20"))
        self.label_17 = QtGui.QLabel(self.tab_2)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.horizontalLayout_20.addWidget(self.label_17)
        self.OyMagLongitudeLineEdit = QtGui.QLineEdit(self.tab_2)
        self.OyMagLongitudeLineEdit.setObjectName(_fromUtf8("OyMagLongitudeLineEdit"))
        self.horizontalLayout_20.addWidget(self.OyMagLongitudeLineEdit)
        self.gridLayout_6.addLayout(self.horizontalLayout_20, 12, 0, 1, 1)
        self.horizontalLayout_21 = QtGui.QHBoxLayout()
        self.horizontalLayout_21.setObjectName(_fromUtf8("horizontalLayout_21"))
        self.label_18 = QtGui.QLabel(self.tab_2)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.horizontalLayout_21.addWidget(self.label_18)
        self.OyMagLatitudeLineEdit = QtGui.QLineEdit(self.tab_2)
        self.OyMagLatitudeLineEdit.setObjectName(_fromUtf8("OyMagLatitudeLineEdit"))
        self.horizontalLayout_21.addWidget(self.OyMagLatitudeLineEdit)
        self.gridLayout_6.addLayout(self.horizontalLayout_21, 13, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.gridLayout_7 = QtGui.QGridLayout(self.tab_3)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.horizontalLayout_23 = QtGui.QHBoxLayout()
        self.horizontalLayout_23.setObjectName(_fromUtf8("horizontalLayout_23"))
        self.label_23 = QtGui.QLabel(self.tab_3)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.horizontalLayout_23.addWidget(self.label_23)
        self.ObNameLineEdit = QtGui.QLineEdit(self.tab_3)
        self.ObNameLineEdit.setObjectName(_fromUtf8("ObNameLineEdit"))
        self.horizontalLayout_23.addWidget(self.ObNameLineEdit)
        self.gridLayout_7.addLayout(self.horizontalLayout_23, 0, 0, 1, 1)
        self.horizontalLayout_24 = QtGui.QHBoxLayout()
        self.horizontalLayout_24.setObjectName(_fromUtf8("horizontalLayout_24"))
        self.label_24 = QtGui.QLabel(self.tab_3)
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.horizontalLayout_24.addWidget(self.label_24)
        self.ObDescriptionLineEdit = QtGui.QLineEdit(self.tab_3)
        self.ObDescriptionLineEdit.setObjectName(_fromUtf8("ObDescriptionLineEdit"))
        self.horizontalLayout_24.addWidget(self.ObDescriptionLineEdit)
        self.gridLayout_7.addLayout(self.horizontalLayout_24, 1, 0, 1, 1)
        self.horizontalLayout_26 = QtGui.QHBoxLayout()
        self.horizontalLayout_26.setObjectName(_fromUtf8("horizontalLayout_26"))
        self.label_26 = QtGui.QLabel(self.tab_3)
        self.label_26.setObjectName(_fromUtf8("label_26"))
        self.horizontalLayout_26.addWidget(self.label_26)
        self.ObTelephoneLineEdit = QtGui.QLineEdit(self.tab_3)
        self.ObTelephoneLineEdit.setObjectName(_fromUtf8("ObTelephoneLineEdit"))
        self.horizontalLayout_26.addWidget(self.ObTelephoneLineEdit)
        self.gridLayout_7.addLayout(self.horizontalLayout_26, 3, 0, 1, 1)
        self.horizontalLayout_25 = QtGui.QHBoxLayout()
        self.horizontalLayout_25.setObjectName(_fromUtf8("horizontalLayout_25"))
        self.label_25 = QtGui.QLabel(self.tab_3)
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.horizontalLayout_25.addWidget(self.label_25)
        self.ObEmailLineEdit = QtGui.QLineEdit(self.tab_3)
        self.ObEmailLineEdit.setObjectName(_fromUtf8("ObEmailLineEdit"))
        self.horizontalLayout_25.addWidget(self.ObEmailLineEdit)
        self.gridLayout_7.addLayout(self.horizontalLayout_25, 2, 0, 1, 1)
        self.horizontalLayout_28 = QtGui.QHBoxLayout()
        self.horizontalLayout_28.setObjectName(_fromUtf8("horizontalLayout_28"))
        self.label_28 = QtGui.QLabel(self.tab_3)
        self.label_28.setObjectName(_fromUtf8("label_28"))
        self.horizontalLayout_28.addWidget(self.label_28)
        self.ObCountryLineEdit = QtGui.QLineEdit(self.tab_3)
        self.ObCountryLineEdit.setObjectName(_fromUtf8("ObCountryLineEdit"))
        self.horizontalLayout_28.addWidget(self.ObCountryLineEdit)
        self.gridLayout_7.addLayout(self.horizontalLayout_28, 5, 0, 1, 1)
        self.horizontalLayout_27 = QtGui.QHBoxLayout()
        self.horizontalLayout_27.setObjectName(_fromUtf8("horizontalLayout_27"))
        self.label_27 = QtGui.QLabel(self.tab_3)
        self.label_27.setObjectName(_fromUtf8("label_27"))
        self.horizontalLayout_27.addWidget(self.label_27)
        self.ObUrlLineEdit = QtGui.QLineEdit(self.tab_3)
        self.ObUrlLineEdit.setObjectName(_fromUtf8("ObUrlLineEdit"))
        self.horizontalLayout_27.addWidget(self.ObUrlLineEdit)
        self.gridLayout_7.addLayout(self.horizontalLayout_27, 4, 0, 1, 1)
        self.horizontalLayout_29 = QtGui.QHBoxLayout()
        self.horizontalLayout_29.setObjectName(_fromUtf8("horizontalLayout_29"))
        self.label_29 = QtGui.QLabel(self.tab_3)
        self.label_29.setObjectName(_fromUtf8("label_29"))
        self.horizontalLayout_29.addWidget(self.label_29)
        self.ObNotesLineEdit = QtGui.QLineEdit(self.tab_3)
        self.ObNotesLineEdit.setObjectName(_fromUtf8("ObNotesLineEdit"))
        self.horizontalLayout_29.addWidget(self.ObNotesLineEdit)
        self.gridLayout_7.addLayout(self.horizontalLayout_29, 6, 0, 1, 1)
        spacerItem10 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_7.addItem(spacerItem10, 7, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem11 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem11)
        self.saveButton = QtGui.QPushButton(ConfigurationDialog)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout.addWidget(self.saveButton)
        self.cancelButton = QtGui.QPushButton(ConfigurationDialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(ConfigurationDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ConfigurationDialog)

    def retranslateUi(self, ConfigurationDialog):
        ConfigurationDialog.setWindowTitle(_translate("ConfigurationDialog", "Configuration", None))
        self.groupBox_3.setTitle(_translate("ConfigurationDialog", "Staribus/ Starinet Relay", None))
        self.label_4.setText(_translate("ConfigurationDialog", "Relay", None))
        self.relayCheckBox.setText(_translate("ConfigurationDialog", "Active", None))
        self.label_7.setText(_translate("ConfigurationDialog", "IP Address", None))
        self.label_8.setText(_translate("ConfigurationDialog", "Port", None))
        self.groupBox_2.setTitle(_translate("ConfigurationDialog", "Staribus Port", None))
        self.label_5.setText(_translate("ConfigurationDialog", "Baudrate", None))
        self.baudrateDefaultCheckBox.setText(_translate("ConfigurationDialog", "Default", None))
        self.label_3.setText(_translate("ConfigurationDialog", "Serial Port", None))
        self.detectInstrumentPortCheckBox.setText(_translate("ConfigurationDialog", "Detect Staribus Port", None))
        self.label_6.setText(_translate("ConfigurationDialog", "Timeout", None))
        self.serialPortTimeoutCheckBox.setText(_translate("ConfigurationDialog", "Default", None))
        self.groupBox_4.setTitle(_translate("ConfigurationDialog", "Staribus to Starinet Instrument Converter", None))
        self.S2SCheckBox.setText(_translate("ConfigurationDialog", "Enable", None))
        self.label_31.setText(_translate("ConfigurationDialog", "IP Address", None))
        self.label_32.setText(_translate("ConfigurationDialog", "Port", None))
        self.groupBox.setTitle(_translate("ConfigurationDialog", "General", None))
        self.label.setText(_translate("ConfigurationDialog", "Data Save Path", None))
        self.chooserButton.setText(_translate("ConfigurationDialog", "Chooser", None))
        self.label_2.setText(_translate("ConfigurationDialog", "Instrument", None))
        self.label_30.setText(_translate("ConfigurationDialog", "Log Level", None))
        self.groupBox_5.setTitle(_translate("ConfigurationDialog", "Chart Legend Attributes", None))
        self.label_33.setText(_translate("ConfigurationDialog", "Legend Location", None))
        self.label_34.setText(_translate("ConfigurationDialog", "Columns", None))
        self.label_35.setText(_translate("ConfigurationDialog", "Font Size", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("ConfigurationDialog", "General", None))
        self.label_9.setText(_translate("ConfigurationDialog", "Name", None))
        self.label_10.setText(_translate("ConfigurationDialog", "Description", None))
        self.label_11.setText(_translate("ConfigurationDialog", "Email", None))
        self.label_12.setText(_translate("ConfigurationDialog", "Telephone", None))
        self.label_13.setText(_translate("ConfigurationDialog", "URL", None))
        self.label_14.setText(_translate("ConfigurationDialog", "Country", None))
        self.label_15.setText(_translate("ConfigurationDialog", "Time Zone", None))
        self.label_20.setText(_translate("ConfigurationDialog", "Longitude", None))
        self.label_21.setText(_translate("ConfigurationDialog", "Latitude", None))
        self.label_22.setText(_translate("ConfigurationDialog", "Height Above Sea Level", None))
        self.label_16.setText(_translate("ConfigurationDialog", "Geodetic Datum", None))
        self.label_19.setText(_translate("ConfigurationDialog", "Geomagnetic Model", None))
        self.label_17.setText(_translate("ConfigurationDialog", "Geomagnetic Longitude", None))
        self.label_18.setText(_translate("ConfigurationDialog", "Geomagnetic Latitude", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("ConfigurationDialog", "Observatory Metadata", None))
        self.label_23.setText(_translate("ConfigurationDialog", "Name", None))
        self.label_24.setText(_translate("ConfigurationDialog", "Description", None))
        self.label_26.setText(_translate("ConfigurationDialog", "Telephone", None))
        self.label_25.setText(_translate("ConfigurationDialog", "Email", None))
        self.label_28.setText(_translate("ConfigurationDialog", "Country", None))
        self.label_27.setText(_translate("ConfigurationDialog", "URL", None))
        self.label_29.setText(_translate("ConfigurationDialog", "Notes", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("ConfigurationDialog", "Observer Metadata", None))
        self.saveButton.setText(_translate("ConfigurationDialog", "Save", None))
        self.cancelButton.setText(_translate("ConfigurationDialog", "Cancel", None))

