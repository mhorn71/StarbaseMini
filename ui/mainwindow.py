# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Sat May  7 18:48:49 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(905, 651)
        MainWindow.setMinimumSize(QtCore.QSize(0, 651))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setMinimumSize(QtCore.QSize(621, 61))
        self.groupBox_3.setMaximumSize(QtCore.QSize(16777215, 111))
        self.groupBox_3.setStyleSheet("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.statusMessage = QtGui.QTableWidget(self.groupBox_3)
        self.statusMessage.setStyleSheet("QTableWidget {\n"
"    font-size: 11px;\n"
"    background-color: \'#FFFFE0\';\n"
"}\n"
"\n"
"QTableWidget QHeaderView {\n"
"    font-size: 11px;\n"
"}\n"
"\n"
"QTableWidget QHeaderView::section {\n"
"    height: 18px;\n"
"}")
        self.statusMessage.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.statusMessage.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.statusMessage.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.statusMessage.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.statusMessage.setWordWrap(False)
        self.statusMessage.setColumnCount(5)
        self.statusMessage.setObjectName("statusMessage")
        self.statusMessage.setColumnCount(5)
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
        self.groupBox_2.setObjectName("groupBox_2")
        self.layoutWidget = QtGui.QWidget(self.groupBox_2)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 131, 581))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolBox = QtGui.QToolBox(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toolBox.setStyleSheet("QToolBox::tab {\n"
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
"}")
        self.toolBox.setObjectName("toolBox")
        self.UserCtrl = QtGui.QWidget()
        self.UserCtrl.setGeometry(QtCore.QRect(0, 0, 129, 521))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.UserCtrl.sizePolicy().hasHeightForWidth())
        self.UserCtrl.setSizePolicy(sizePolicy)
        self.UserCtrl.setObjectName("UserCtrl")
        self.layoutWidget1 = QtGui.QWidget(self.UserCtrl)
        self.layoutWidget1.setGeometry(QtCore.QRect(0, 0, 131, 259))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.moduleCombobox = QtGui.QComboBox(self.layoutWidget1)
        self.moduleCombobox.setObjectName("moduleCombobox")
        self.gridLayout.addWidget(self.moduleCombobox, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.commandCombobox = QtGui.QComboBox(self.layoutWidget1)
        self.commandCombobox.setObjectName("commandCombobox")
        self.gridLayout.addWidget(self.commandCombobox, 3, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.commandParameter = QtGui.QLineEdit(self.layoutWidget1)
        self.commandParameter.setMaxLength(15)
        self.commandParameter.setObjectName("commandParameter")
        self.gridLayout.addWidget(self.commandParameter, 5, 0, 1, 1)
        self.choicesComboBox = QtGui.QComboBox(self.layoutWidget1)
        self.choicesComboBox.setObjectName("choicesComboBox")
        self.gridLayout.addWidget(self.choicesComboBox, 6, 0, 1, 1)
        self.executeButton = QtGui.QPushButton(self.layoutWidget1)
        self.executeButton.setObjectName("executeButton")
        self.gridLayout.addWidget(self.executeButton, 7, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 1)
        self.toolBox.addItem(self.UserCtrl, "")
        self.UserInst = QtGui.QWidget()
        self.UserInst.setGeometry(QtCore.QRect(0, 0, 129, 521))
        self.UserInst.setObjectName("UserInst")
        self.layoutWidget2 = QtGui.QWidget(self.UserInst)
        self.layoutWidget2.setGeometry(QtCore.QRect(0, 2, 124, 443))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_5 = QtGui.QGridLayout(self.layoutWidget2)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.chartDecimateCheckBox = QtGui.QCheckBox(self.layoutWidget2)
        self.chartDecimateCheckBox.setObjectName("chartDecimateCheckBox")
        self.verticalLayout_2.addWidget(self.chartDecimateCheckBox)
        self.chartAutoRangeCheckBox = QtGui.QCheckBox(self.layoutWidget2)
        self.chartAutoRangeCheckBox.setObjectName("chartAutoRangeCheckBox")
        self.verticalLayout_2.addWidget(self.chartAutoRangeCheckBox)
        self.showLegend = QtGui.QCheckBox(self.layoutWidget2)
        self.showLegend.setObjectName("showLegend")
        self.verticalLayout_2.addWidget(self.showLegend)
        self.gridLayout_5.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.channel0colour = QtGui.QCheckBox(self.layoutWidget2)
        self.channel0colour.setMaximumSize(QtCore.QSize(5, 22))
        self.channel0colour.setText("")
        self.channel0colour.setCheckable(False)
        self.channel0colour.setObjectName("channel0colour")
        self.horizontalLayout.addWidget(self.channel0colour)
        self.channel0Button = QtGui.QPushButton(self.layoutWidget2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channel0Button.sizePolicy().hasHeightForWidth())
        self.channel0Button.setSizePolicy(sizePolicy)
        self.channel0Button.setCheckable(True)
        self.channel0Button.setObjectName("channel0Button")
        self.horizontalLayout.addWidget(self.channel0Button)
        self.gridLayout_5.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.channel1colour = QtGui.QCheckBox(self.layoutWidget2)
        self.channel1colour.setMaximumSize(QtCore.QSize(5, 22))
        self.channel1colour.setText("")
        self.channel1colour.setCheckable(False)
        self.channel1colour.setObjectName("channel1colour")
        self.horizontalLayout_2.addWidget(self.channel1colour)
        self.channel1Button = QtGui.QPushButton(self.layoutWidget2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channel1Button.sizePolicy().hasHeightForWidth())
        self.channel1Button.setSizePolicy(sizePolicy)
        self.channel1Button.setCheckable(True)
        self.channel1Button.setObjectName("channel1Button")
        self.horizontalLayout_2.addWidget(self.channel1Button)
        self.gridLayout_5.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.channel2colour = QtGui.QCheckBox(self.layoutWidget2)
        self.channel2colour.setMaximumSize(QtCore.QSize(5, 22))
        self.channel2colour.setText("")
        self.channel2colour.setCheckable(False)
        self.channel2colour.setObjectName("channel2colour")
        self.horizontalLayout_3.addWidget(self.channel2colour)
        self.channel2Button = QtGui.QPushButton(self.layoutWidget2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channel2Button.sizePolicy().hasHeightForWidth())
        self.channel2Button.setSizePolicy(sizePolicy)
        self.channel2Button.setCheckable(True)
        self.channel2Button.setObjectName("channel2Button")
        self.horizontalLayout_3.addWidget(self.channel2Button)
        self.gridLayout_5.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.channel3colour = QtGui.QCheckBox(self.layoutWidget2)
        self.channel3colour.setMaximumSize(QtCore.QSize(5, 22))
        self.channel3colour.setText("")
        self.channel3colour.setCheckable(False)
        self.channel3colour.setObjectName("channel3colour")
        self.horizontalLayout_4.addWidget(self.channel3colour)
        self.channel3Button = QtGui.QPushButton(self.layoutWidget2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channel3Button.sizePolicy().hasHeightForWidth())
        self.channel3Button.setSizePolicy(sizePolicy)
        self.channel3Button.setCheckable(True)
        self.channel3Button.setObjectName("channel3Button")
        self.horizontalLayout_4.addWidget(self.channel3Button)
        self.gridLayout_5.addLayout(self.horizontalLayout_4, 4, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.channel4colour = QtGui.QCheckBox(self.layoutWidget2)
        self.channel4colour.setMaximumSize(QtCore.QSize(5, 22))
        self.channel4colour.setText("")
        self.channel4colour.setCheckable(False)
        self.channel4colour.setObjectName("channel4colour")
        self.horizontalLayout_5.addWidget(self.channel4colour)
        self.channel4Button = QtGui.QPushButton(self.layoutWidget2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channel4Button.sizePolicy().hasHeightForWidth())
        self.channel4Button.setSizePolicy(sizePolicy)
        self.channel4Button.setCheckable(True)
        self.channel4Button.setObjectName("channel4Button")
        self.horizontalLayout_5.addWidget(self.channel4Button)
        self.gridLayout_5.addLayout(self.horizontalLayout_5, 5, 0, 1, 1)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.channel5colour = QtGui.QCheckBox(self.layoutWidget2)
        self.channel5colour.setMaximumSize(QtCore.QSize(5, 22))
        self.channel5colour.setText("")
        self.channel5colour.setCheckable(False)
        self.channel5colour.setObjectName("channel5colour")
        self.horizontalLayout_6.addWidget(self.channel5colour)
        self.channel5Button = QtGui.QPushButton(self.layoutWidget2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channel5Button.sizePolicy().hasHeightForWidth())
        self.channel5Button.setSizePolicy(sizePolicy)
        self.channel5Button.setCheckable(True)
        self.channel5Button.setObjectName("channel5Button")
        self.horizontalLayout_6.addWidget(self.channel5Button)
        self.gridLayout_5.addLayout(self.horizontalLayout_6, 6, 0, 1, 1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.channel6colour = QtGui.QCheckBox(self.layoutWidget2)
        self.channel6colour.setMaximumSize(QtCore.QSize(5, 22))
        self.channel6colour.setText("")
        self.channel6colour.setCheckable(False)
        self.channel6colour.setObjectName("channel6colour")
        self.horizontalLayout_7.addWidget(self.channel6colour)
        self.channel6Button = QtGui.QPushButton(self.layoutWidget2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channel6Button.sizePolicy().hasHeightForWidth())
        self.channel6Button.setSizePolicy(sizePolicy)
        self.channel6Button.setCheckable(True)
        self.channel6Button.setObjectName("channel6Button")
        self.horizontalLayout_7.addWidget(self.channel6Button)
        self.gridLayout_5.addLayout(self.horizontalLayout_7, 7, 0, 1, 1)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.channel7colour = QtGui.QCheckBox(self.layoutWidget2)
        self.channel7colour.setMaximumSize(QtCore.QSize(5, 22))
        self.channel7colour.setText("")
        self.channel7colour.setCheckable(False)
        self.channel7colour.setObjectName("channel7colour")
        self.horizontalLayout_8.addWidget(self.channel7colour)
        self.channel7Button = QtGui.QPushButton(self.layoutWidget2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channel7Button.sizePolicy().hasHeightForWidth())
        self.channel7Button.setSizePolicy(sizePolicy)
        self.channel7Button.setCheckable(True)
        self.channel7Button.setObjectName("channel7Button")
        self.horizontalLayout_8.addWidget(self.channel7Button)
        self.gridLayout_5.addLayout(self.horizontalLayout_8, 8, 0, 1, 1)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.channel8colour = QtGui.QCheckBox(self.layoutWidget2)
        self.channel8colour.setMaximumSize(QtCore.QSize(5, 22))
        self.channel8colour.setText("")
        self.channel8colour.setCheckable(False)
        self.channel8colour.setObjectName("channel8colour")
        self.horizontalLayout_9.addWidget(self.channel8colour)
        self.channel8Button = QtGui.QPushButton(self.layoutWidget2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channel8Button.sizePolicy().hasHeightForWidth())
        self.channel8Button.setSizePolicy(sizePolicy)
        self.channel8Button.setCheckable(True)
        self.channel8Button.setObjectName("channel8Button")
        self.horizontalLayout_9.addWidget(self.channel8Button)
        self.gridLayout_5.addLayout(self.horizontalLayout_9, 9, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem1, 10, 0, 1, 1)
        self.toolBox.addItem(self.UserInst, "")
        self.verticalLayout.addWidget(self.toolBox)
        self.gridLayout_2.addWidget(self.groupBox_2, 0, 1, 2, 1)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setStyleSheet("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.mplwindow = QtGui.QWidget(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mplwindow.sizePolicy().hasHeightForWidth())
        self.mplwindow.setSizePolicy(sizePolicy)
        self.mplwindow.setStyleSheet("")
        self.mplwindow.setObjectName("mplwindow")
        self.mplvl = QtGui.QVBoxLayout(self.mplwindow)
        self.mplvl.setContentsMargins(0, 0, 0, 0)
        self.mplvl.setObjectName("mplvl")
        self.gridLayout_4.addWidget(self.mplwindow, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 905, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuInstrument = QtGui.QMenu(self.menubar)
        self.menuInstrument.setObjectName("menuInstrument")
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuSegment_Data = QtGui.QMenu(self.menuTools)
        self.menuSegment_Data.setObjectName("menuSegment_Data")
        MainWindow.setMenuBar(self.menubar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionConfiguration = QtGui.QAction(MainWindow)
        self.actionConfiguration.setObjectName("actionConfiguration")
        self.actionControllerEditor = QtGui.QAction(MainWindow)
        self.actionControllerEditor.setObjectName("actionControllerEditor")
        self.actionObserveratory = QtGui.QAction(MainWindow)
        self.actionObserveratory.setObjectName("actionObserveratory")
        self.actionManual = QtGui.QAction(MainWindow)
        self.actionManual.setObjectName("actionManual")
        self.action = QtGui.QAction(MainWindow)
        self.action.setObjectName("action")
        self.actionInstrumentBuilder = QtGui.QAction(MainWindow)
        self.actionInstrumentBuilder.setObjectName("actionInstrumentBuilder")
        self.actionInstrument_Attributes = QtGui.QAction(MainWindow)
        self.actionInstrument_Attributes.setObjectName("actionInstrument_Attributes")
        self.actionInstrument_Attrib = QtGui.QAction(MainWindow)
        self.actionInstrument_Attrib.setObjectName("actionInstrument_Attrib")
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionReleaseNotes = QtGui.QAction(MainWindow)
        self.actionReleaseNotes.setObjectName("actionReleaseNotes")
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave_RawData = QtGui.QAction(MainWindow)
        self.actionSave_RawData.setObjectName("actionSave_RawData")
        self.actionSave_Processed_Data = QtGui.QAction(MainWindow)
        self.actionSave_Processed_Data.setObjectName("actionSave_Processed_Data")
        self.actionDay = QtGui.QAction(MainWindow)
        self.actionDay.setObjectName("actionDay")
        self.actionWeek = QtGui.QAction(MainWindow)
        self.actionWeek.setObjectName("actionWeek")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave_RawData)
        self.menuFile.addAction(self.actionSave_Processed_Data)
        self.menuFile.addAction(self.actionConfiguration)
        self.menuFile.addAction(self.actionExit)
        self.menuAbout.addAction(self.actionAbout)
        self.menuAbout.addAction(self.actionReleaseNotes)
        self.menuEdit.addAction(self.actionInstrument_Attrib)
        self.menuSegment_Data.addAction(self.actionDay)
        self.menuSegment_Data.addAction(self.actionWeek)
        self.menuTools.addAction(self.menuSegment_Data.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuInstrument.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        self.toolBox.layout().setSpacing(4)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("MainWindow", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Control Panel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Module", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Command", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Parameter", None, QtGui.QApplication.UnicodeUTF8))
        self.executeButton.setText(QtGui.QApplication.translate("MainWindow", "Execute", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.UserCtrl), QtGui.QApplication.translate("MainWindow", "Instrument", None, QtGui.QApplication.UnicodeUTF8))
        self.chartDecimateCheckBox.setText(QtGui.QApplication.translate("MainWindow", "Decimate", None, QtGui.QApplication.UnicodeUTF8))
        self.chartAutoRangeCheckBox.setText(QtGui.QApplication.translate("MainWindow", "AutoRange", None, QtGui.QApplication.UnicodeUTF8))
        self.showLegend.setText(QtGui.QApplication.translate("MainWindow", "Show Legend", None, QtGui.QApplication.UnicodeUTF8))
        self.channel0Button.setText(QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.channel1Button.setText(QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.channel2Button.setText(QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.channel3Button.setText(QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.channel4Button.setText(QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.channel5Button.setText(QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.channel6Button.setText(QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.channel7Button.setText(QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.channel8Button.setText(QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.UserInst), QtGui.QApplication.translate("MainWindow", "Chart Control", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Chart", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setTitle(QtGui.QApplication.translate("MainWindow", "Info", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", " Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuInstrument.setTitle(QtGui.QApplication.translate("MainWindow", "Instruments", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSegment_Data.setTitle(QtGui.QApplication.translate("MainWindow", "Segment Data", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConfiguration.setText(QtGui.QApplication.translate("MainWindow", "Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.actionControllerEditor.setText(QtGui.QApplication.translate("MainWindow", "Futurlec Controller", None, QtGui.QApplication.UnicodeUTF8))
        self.actionObserveratory.setText(QtGui.QApplication.translate("MainWindow", "Observeratory", None, QtGui.QApplication.UnicodeUTF8))
        self.actionManual.setText(QtGui.QApplication.translate("MainWindow", "Manual", None, QtGui.QApplication.UnicodeUTF8))
        self.action.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInstrumentBuilder.setText(QtGui.QApplication.translate("MainWindow", "Instrument Builder", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInstrument_Attributes.setText(QtGui.QApplication.translate("MainWindow", "Instrument Attributes", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInstrument_Attrib.setText(QtGui.QApplication.translate("MainWindow", "Instrument Attributes", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReleaseNotes.setText(QtGui.QApplication.translate("MainWindow", "ReleaseNotes", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_RawData.setText(QtGui.QApplication.translate("MainWindow", "Save Raw Data", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Processed_Data.setText(QtGui.QApplication.translate("MainWindow", "Save Processed Data", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDay.setText(QtGui.QApplication.translate("MainWindow", "Day", None, QtGui.QApplication.UnicodeUTF8))
        self.actionWeek.setText(QtGui.QApplication.translate("MainWindow", "Week", None, QtGui.QApplication.UnicodeUTF8))

