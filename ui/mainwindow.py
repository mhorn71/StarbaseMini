# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Mon Sep 14 17:39:14 2015
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(905, 651)
        MainWindow.setMinimumSize(QtCore.QSize(0, 651))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(_fromUtf8(""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setMinimumSize(QtCore.QSize(621, 61))
        self.groupBox_3.setMaximumSize(QtCore.QSize(16777215, 111))
        self.groupBox_3.setStyleSheet(_fromUtf8(""))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.statusMessage = QtGui.QTableWidget(self.groupBox_3)
        self.statusMessage.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.statusMessage.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.statusMessage.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.statusMessage.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.statusMessage.setWordWrap(False)
        self.statusMessage.setColumnCount(5)
        self.statusMessage.setObjectName(_fromUtf8("statusMessage"))
        self.statusMessage.setRowCount(0)
        self.statusMessage.horizontalHeader().setCascadingSectionResizes(True)
        self.statusMessage.horizontalHeader().setDefaultSectionSize(100)
        self.statusMessage.horizontalHeader().setMinimumSectionSize(56)
        self.statusMessage.horizontalHeader().setStretchLastSection(False)
        self.statusMessage.verticalHeader().setVisible(False)
        self.statusMessage.verticalHeader().setStretchLastSection(False)
        self.gridLayout_3.addWidget(self.statusMessage, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_3, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(147, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.groupBox_2.setStyleSheet(_fromUtf8("QGroupBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 9px;\n"
"    margin-top: 0.5em;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 3px 3px 0 3px;\n"
"}"))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.layoutWidget = QtGui.QWidget(self.groupBox_2)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 131, 581))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.toolBox = QtGui.QToolBox(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toolBox.setStyleSheet(_fromUtf8("QToolBox::tab {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"    border-radius: 5px;\n"
"    color: darkgray;\n"
"}\n"
"\n"
"QToolBox::tab:selected { /* italicize selected tabs */\n"
"    font: italic;\n"
"    color: black;\n"
"}"))
        self.toolBox.setObjectName(_fromUtf8("toolBox"))
        self.UserCtrl = QtGui.QWidget()
        self.UserCtrl.setGeometry(QtCore.QRect(0, 0, 129, 521))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.UserCtrl.sizePolicy().hasHeightForWidth())
        self.UserCtrl.setSizePolicy(sizePolicy)
        self.UserCtrl.setObjectName(_fromUtf8("UserCtrl"))
        self.layoutWidget1 = QtGui.QWidget(self.UserCtrl)
        self.layoutWidget1.setGeometry(QtCore.QRect(0, 0, 131, 259))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget1)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.layoutWidget1)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.moduleCombobox = QtGui.QComboBox(self.layoutWidget1)
        self.moduleCombobox.setObjectName(_fromUtf8("moduleCombobox"))
        self.gridLayout.addWidget(self.moduleCombobox, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget1)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.commandCombobox = QtGui.QComboBox(self.layoutWidget1)
        self.commandCombobox.setObjectName(_fromUtf8("commandCombobox"))
        self.gridLayout.addWidget(self.commandCombobox, 3, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.commandParameter = QtGui.QLineEdit(self.layoutWidget1)
        self.commandParameter.setObjectName(_fromUtf8("commandParameter"))
        self.gridLayout.addWidget(self.commandParameter, 5, 0, 1, 1)
        self.choicesComboBox = QtGui.QComboBox(self.layoutWidget1)
        self.choicesComboBox.setObjectName(_fromUtf8("choicesComboBox"))
        self.gridLayout.addWidget(self.choicesComboBox, 6, 0, 1, 1)
        self.executeButton = QtGui.QPushButton(self.layoutWidget1)
        self.executeButton.setObjectName(_fromUtf8("executeButton"))
        self.gridLayout.addWidget(self.executeButton, 7, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 1)
        self.toolBox.addItem(self.UserCtrl, _fromUtf8(""))
        self.UserInst = QtGui.QWidget()
        self.UserInst.setGeometry(QtCore.QRect(0, 0, 129, 521))
        self.UserInst.setObjectName(_fromUtf8("UserInst"))
        self.layoutWidget2 = QtGui.QWidget(self.UserInst)
        self.layoutWidget2.setGeometry(QtCore.QRect(1, 1, 128, 373))
        self.layoutWidget2.setObjectName(_fromUtf8("layoutWidget2"))
        self.gridLayout_5 = QtGui.QGridLayout(self.layoutWidget2)
        self.gridLayout_5.setMargin(0)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.chartDecimateCheckBox = QtGui.QCheckBox(self.layoutWidget2)
        self.chartDecimateCheckBox.setObjectName(_fromUtf8("chartDecimateCheckBox"))
        self.gridLayout_5.addWidget(self.chartDecimateCheckBox, 0, 0, 1, 1)
        self.chartAutoRangeCheckBox = QtGui.QCheckBox(self.layoutWidget2)
        self.chartAutoRangeCheckBox.setObjectName(_fromUtf8("chartAutoRangeCheckBox"))
        self.gridLayout_5.addWidget(self.chartAutoRangeCheckBox, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.channel0colour = QtGui.QCheckBox(self.layoutWidget2)
        self.channel0colour.setMaximumSize(QtCore.QSize(21, 22))
        self.channel0colour.setText(_fromUtf8(""))
        self.channel0colour.setCheckable(False)
        self.channel0colour.setObjectName(_fromUtf8("channel0colour"))
        self.horizontalLayout.addWidget(self.channel0colour)
        self.channel0Button = QtGui.QPushButton(self.layoutWidget2)
        self.channel0Button.setCheckable(True)
        self.channel0Button.setObjectName(_fromUtf8("channel0Button"))
        self.horizontalLayout.addWidget(self.channel0Button)
        self.gridLayout_5.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.channel1colour = QtGui.QCheckBox(self.layoutWidget2)
        self.channel1colour.setMaximumSize(QtCore.QSize(21, 22))
        self.channel1colour.setText(_fromUtf8(""))
        self.channel1colour.setCheckable(False)
        self.channel1colour.setObjectName(_fromUtf8("channel1colour"))
        self.horizontalLayout_2.addWidget(self.channel1colour)
        self.channel1Button = QtGui.QPushButton(self.layoutWidget2)
        self.channel1Button.setCheckable(True)
        self.channel1Button.setObjectName(_fromUtf8("channel1Button"))
        self.horizontalLayout_2.addWidget(self.channel1Button)
        self.gridLayout_5.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.channel2colour = QtGui.QCheckBox(self.layoutWidget2)
        self.channel2colour.setMaximumSize(QtCore.QSize(21, 22))
        self.channel2colour.setText(_fromUtf8(""))
        self.channel2colour.setCheckable(False)
        self.channel2colour.setObjectName(_fromUtf8("channel2colour"))
        self.horizontalLayout_3.addWidget(self.channel2colour)
        self.channel2Button = QtGui.QPushButton(self.layoutWidget2)
        self.channel2Button.setCheckable(True)
        self.channel2Button.setObjectName(_fromUtf8("channel2Button"))
        self.horizontalLayout_3.addWidget(self.channel2Button)
        self.gridLayout_5.addLayout(self.horizontalLayout_3, 4, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.channel3colour = QtGui.QCheckBox(self.layoutWidget2)
        self.channel3colour.setMaximumSize(QtCore.QSize(21, 22))
        self.channel3colour.setText(_fromUtf8(""))
        self.channel3colour.setCheckable(False)
        self.channel3colour.setObjectName(_fromUtf8("channel3colour"))
        self.horizontalLayout_4.addWidget(self.channel3colour)
        self.channel3Button = QtGui.QPushButton(self.layoutWidget2)
        self.channel3Button.setCheckable(True)
        self.channel3Button.setObjectName(_fromUtf8("channel3Button"))
        self.horizontalLayout_4.addWidget(self.channel3Button)
        self.gridLayout_5.addLayout(self.horizontalLayout_4, 5, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.channel4colour = QtGui.QCheckBox(self.layoutWidget2)
        self.channel4colour.setMaximumSize(QtCore.QSize(21, 22))
        self.channel4colour.setText(_fromUtf8(""))
        self.channel4colour.setCheckable(False)
        self.channel4colour.setObjectName(_fromUtf8("channel4colour"))
        self.horizontalLayout_5.addWidget(self.channel4colour)
        self.channel4Button = QtGui.QPushButton(self.layoutWidget2)
        self.channel4Button.setCheckable(True)
        self.channel4Button.setObjectName(_fromUtf8("channel4Button"))
        self.horizontalLayout_5.addWidget(self.channel4Button)
        self.gridLayout_5.addLayout(self.horizontalLayout_5, 6, 0, 1, 1)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.channel5colour = QtGui.QCheckBox(self.layoutWidget2)
        self.channel5colour.setMaximumSize(QtCore.QSize(21, 22))
        self.channel5colour.setText(_fromUtf8(""))
        self.channel5colour.setCheckable(False)
        self.channel5colour.setObjectName(_fromUtf8("channel5colour"))
        self.horizontalLayout_6.addWidget(self.channel5colour)
        self.channel5Button = QtGui.QPushButton(self.layoutWidget2)
        self.channel5Button.setCheckable(True)
        self.channel5Button.setObjectName(_fromUtf8("channel5Button"))
        self.horizontalLayout_6.addWidget(self.channel5Button)
        self.gridLayout_5.addLayout(self.horizontalLayout_6, 7, 0, 1, 1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.channel6colour = QtGui.QCheckBox(self.layoutWidget2)
        self.channel6colour.setMaximumSize(QtCore.QSize(21, 22))
        self.channel6colour.setText(_fromUtf8(""))
        self.channel6colour.setCheckable(False)
        self.channel6colour.setObjectName(_fromUtf8("channel6colour"))
        self.horizontalLayout_7.addWidget(self.channel6colour)
        self.channel6Button = QtGui.QPushButton(self.layoutWidget2)
        self.channel6Button.setCheckable(True)
        self.channel6Button.setObjectName(_fromUtf8("channel6Button"))
        self.horizontalLayout_7.addWidget(self.channel6Button)
        self.gridLayout_5.addLayout(self.horizontalLayout_7, 8, 0, 1, 1)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.channel7colour = QtGui.QCheckBox(self.layoutWidget2)
        self.channel7colour.setMaximumSize(QtCore.QSize(21, 22))
        self.channel7colour.setText(_fromUtf8(""))
        self.channel7colour.setCheckable(False)
        self.channel7colour.setObjectName(_fromUtf8("channel7colour"))
        self.horizontalLayout_8.addWidget(self.channel7colour)
        self.channel7Button = QtGui.QPushButton(self.layoutWidget2)
        self.channel7Button.setCheckable(True)
        self.channel7Button.setObjectName(_fromUtf8("channel7Button"))
        self.horizontalLayout_8.addWidget(self.channel7Button)
        self.gridLayout_5.addLayout(self.horizontalLayout_8, 9, 0, 1, 1)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.channel8colour = QtGui.QCheckBox(self.layoutWidget2)
        self.channel8colour.setMaximumSize(QtCore.QSize(21, 22))
        self.channel8colour.setText(_fromUtf8(""))
        self.channel8colour.setCheckable(False)
        self.channel8colour.setObjectName(_fromUtf8("channel8colour"))
        self.horizontalLayout_9.addWidget(self.channel8colour)
        self.channel8Button = QtGui.QPushButton(self.layoutWidget2)
        self.channel8Button.setCheckable(True)
        self.channel8Button.setObjectName(_fromUtf8("channel8Button"))
        self.horizontalLayout_9.addWidget(self.channel8Button)
        self.gridLayout_5.addLayout(self.horizontalLayout_9, 10, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem1, 11, 0, 1, 1)
        self.toolBox.addItem(self.UserInst, _fromUtf8(""))
        self.verticalLayout.addWidget(self.toolBox)
        self.gridLayout_2.addWidget(self.groupBox_2, 0, 1, 2, 1)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setStyleSheet(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.mplwindow = QtGui.QWidget(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mplwindow.sizePolicy().hasHeightForWidth())
        self.mplwindow.setSizePolicy(sizePolicy)
        self.mplwindow.setStyleSheet(_fromUtf8(""))
        self.mplwindow.setObjectName(_fromUtf8("mplwindow"))
        self.mplvl = QtGui.QVBoxLayout(self.mplwindow)
        self.mplvl.setMargin(0)
        self.mplvl.setObjectName(_fromUtf8("mplvl"))
        self.gridLayout_4.addWidget(self.mplwindow, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 905, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuMetadata = QtGui.QMenu(self.menubar)
        self.menuMetadata.setObjectName(_fromUtf8("menuMetadata"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        MainWindow.setMenuBar(self.menubar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionConfiguration = QtGui.QAction(MainWindow)
        self.actionConfiguration.setObjectName(_fromUtf8("actionConfiguration"))
        self.actionControllerEditor = QtGui.QAction(MainWindow)
        self.actionControllerEditor.setObjectName(_fromUtf8("actionControllerEditor"))
        self.actionObserveratory = QtGui.QAction(MainWindow)
        self.actionObserveratory.setObjectName(_fromUtf8("actionObserveratory"))
        self.actionManual = QtGui.QAction(MainWindow)
        self.actionManual.setObjectName(_fromUtf8("actionManual"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionInstrumentBuilder = QtGui.QAction(MainWindow)
        self.actionInstrumentBuilder.setObjectName(_fromUtf8("actionInstrumentBuilder"))
        self.actionInstrument_Attributes = QtGui.QAction(MainWindow)
        self.actionInstrument_Attributes.setObjectName(_fromUtf8("actionInstrument_Attributes"))
        self.actionInstrument_Attrib = QtGui.QAction(MainWindow)
        self.actionInstrument_Attrib.setObjectName(_fromUtf8("actionInstrument_Attrib"))
        self.menuFile.addAction(self.actionConfiguration)
        self.menuFile.addAction(self.actionExit)
        self.menuMetadata.addAction(self.actionInstrumentBuilder)
        self.menuHelp.addAction(self.actionManual)
        self.menuHelp.addAction(self.actionAbout)
        self.menuEdit.addAction(self.actionInstrument_Attrib)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuMetadata.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        self.toolBox.layout().setSpacing(4)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Status", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Control Panel", None))
        self.label.setText(_translate("MainWindow", "Module", None))
        self.label_3.setText(_translate("MainWindow", "Command", None))
        self.label_2.setText(_translate("MainWindow", "Parameter", None))
        self.executeButton.setText(_translate("MainWindow", "Execute", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.UserCtrl), _translate("MainWindow", "Instrument", None))
        self.chartDecimateCheckBox.setText(_translate("MainWindow", "Decimate", None))
        self.chartAutoRangeCheckBox.setText(_translate("MainWindow", "AutoRange", None))
        self.channel0Button.setText(_translate("MainWindow", "PushButton", None))
        self.channel1Button.setText(_translate("MainWindow", "PushButton", None))
        self.channel2Button.setText(_translate("MainWindow", "PushButton", None))
        self.channel3Button.setText(_translate("MainWindow", "PushButton", None))
        self.channel4Button.setText(_translate("MainWindow", "PushButton", None))
        self.channel5Button.setText(_translate("MainWindow", "PushButton", None))
        self.channel6Button.setText(_translate("MainWindow", "PushButton", None))
        self.channel7Button.setText(_translate("MainWindow", "PushButton", None))
        self.channel8Button.setText(_translate("MainWindow", "PushButton", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.UserInst), _translate("MainWindow", "Chart Control", None))
        self.groupBox.setTitle(_translate("MainWindow", "Chart", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuMetadata.setTitle(_translate("MainWindow", "Tools", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.menuEdit.setTitle(_translate("MainWindow", " Edit", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionConfiguration.setText(_translate("MainWindow", "Configuration", None))
        self.actionControllerEditor.setText(_translate("MainWindow", "Futurlec Controller", None))
        self.actionObserveratory.setText(_translate("MainWindow", "Observeratory", None))
        self.actionManual.setText(_translate("MainWindow", "Manual", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
        self.actionInstrumentBuilder.setText(_translate("MainWindow", "Instrument Builder", None))
        self.actionInstrument_Attributes.setText(_translate("MainWindow", "Instrument Attributes", None))
        self.actionInstrument_Attrib.setText(_translate("MainWindow", "Instrument Attributes", None))

