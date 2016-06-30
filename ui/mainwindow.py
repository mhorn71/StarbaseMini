# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(905, 651)
        MainWindow.setMinimumSize(QtCore.QSize(0, 651))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setMinimumSize(QtCore.QSize(621, 111))
        self.groupBox_3.setMaximumSize(QtCore.QSize(16777215, 111))
        self.groupBox_3.setStyleSheet("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.statusMessage = QtWidgets.QTableWidget(self.groupBox_3)
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
        self.statusMessage.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.statusMessage.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.statusMessage.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.statusMessage.setWordWrap(False)
        self.statusMessage.setColumnCount(5)
        self.statusMessage.setObjectName("statusMessage")
        self.statusMessage.setRowCount(0)
        self.statusMessage.horizontalHeader().setCascadingSectionResizes(True)
        self.statusMessage.horizontalHeader().setDefaultSectionSize(100)
        self.statusMessage.horizontalHeader().setMinimumSectionSize(56)
        self.statusMessage.horizontalHeader().setStretchLastSection(False)
        self.statusMessage.verticalHeader().setVisible(False)
        self.statusMessage.verticalHeader().setStretchLastSection(False)
        self.gridLayout_3.addWidget(self.statusMessage, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_3, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(147, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 131, 581))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolBox = QtWidgets.QToolBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
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
"QToolBox::tab:selected { \n"
"    font: italic;\n"
"    color: green;\n"
"}\n"
"\n"
"QToolBox::tab:!selected {\n"
"    color: black;\n"
"}")
        self.toolBox.setObjectName("toolBox")
        self.UserCtrl = QtWidgets.QWidget()
        self.UserCtrl.setGeometry(QtCore.QRect(0, 0, 98, 28))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.UserCtrl.sizePolicy().hasHeightForWidth())
        self.UserCtrl.setSizePolicy(sizePolicy)
        self.UserCtrl.setObjectName("UserCtrl")
        self.layoutWidget1 = QtWidgets.QWidget(self.UserCtrl)
        self.layoutWidget1.setGeometry(QtCore.QRect(0, 0, 131, 259))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout.setContentsMargins(0, -1, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.moduleCombobox = QtWidgets.QComboBox(self.layoutWidget1)
        self.moduleCombobox.setObjectName("moduleCombobox")
        self.gridLayout.addWidget(self.moduleCombobox, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.commandCombobox = QtWidgets.QComboBox(self.layoutWidget1)
        self.commandCombobox.setObjectName("commandCombobox")
        self.gridLayout.addWidget(self.commandCombobox, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.commandParameter = QtWidgets.QLineEdit(self.layoutWidget1)
        self.commandParameter.setMaxLength(15)
        self.commandParameter.setObjectName("commandParameter")
        self.gridLayout.addWidget(self.commandParameter, 5, 0, 1, 1)
        self.choicesComboBox = QtWidgets.QComboBox(self.layoutWidget1)
        self.choicesComboBox.setObjectName("choicesComboBox")
        self.gridLayout.addWidget(self.choicesComboBox, 6, 0, 1, 1)
        self.executeButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.executeButton.setStyleSheet("")
        self.executeButton.setObjectName("executeButton")
        self.gridLayout.addWidget(self.executeButton, 7, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 1)
        self.toolBox.addItem(self.UserCtrl, "")
        self.UserInst = QtWidgets.QWidget()
        self.UserInst.setGeometry(QtCore.QRect(0, 0, 129, 521))
        self.UserInst.setObjectName("UserInst")
        self.layoutWidget2 = QtWidgets.QWidget(self.UserInst)
        self.layoutWidget2.setGeometry(QtCore.QRect(-3, 30, 121, 327))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.channel7colour = QtWidgets.QCheckBox(self.layoutWidget2)
        self.channel7colour.setMaximumSize(QtCore.QSize(5, 22))
        self.channel7colour.setText("")
        self.channel7colour.setCheckable(False)
        self.channel7colour.setObjectName("channel7colour")
        self.gridLayout_5.addWidget(self.channel7colour, 8, 0, 1, 1)
        self.channel6colour = QtWidgets.QCheckBox(self.layoutWidget2)
        self.channel6colour.setMaximumSize(QtCore.QSize(5, 22))
        self.channel6colour.setText("")
        self.channel6colour.setCheckable(False)
        self.channel6colour.setObjectName("channel6colour")
        self.gridLayout_5.addWidget(self.channel6colour, 7, 0, 1, 1)
        self.showLegend = QtWidgets.QCheckBox(self.layoutWidget2)
        self.showLegend.setObjectName("showLegend")
        self.gridLayout_5.addWidget(self.showLegend, 0, 0, 1, 2)
        self.channel0colour = QtWidgets.QCheckBox(self.layoutWidget2)
        self.channel0colour.setMaximumSize(QtCore.QSize(10, 22))
        self.channel0colour.setText("")
        self.channel0colour.setCheckable(False)
        self.channel0colour.setObjectName("channel0colour")
        self.gridLayout_5.addWidget(self.channel0colour, 1, 0, 1, 1)
        self.channel0Button = QtWidgets.QPushButton(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channel0Button.sizePolicy().hasHeightForWidth())
        self.channel0Button.setSizePolicy(sizePolicy)
        self.channel0Button.setCheckable(True)
        self.channel0Button.setObjectName("channel0Button")
        self.gridLayout_5.addWidget(self.channel0Button, 1, 1, 1, 1)
        self.channel1colour = QtWidgets.QCheckBox(self.layoutWidget2)
        self.channel1colour.setMaximumSize(QtCore.QSize(5, 22))
        self.channel1colour.setText("")
        self.channel1colour.setCheckable(False)
        self.channel1colour.setObjectName("channel1colour")
        self.gridLayout_5.addWidget(self.channel1colour, 2, 0, 1, 1)
        self.channel1Button = QtWidgets.QPushButton(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channel1Button.sizePolicy().hasHeightForWidth())
        self.channel1Button.setSizePolicy(sizePolicy)
        self.channel1Button.setCheckable(True)
        self.channel1Button.setObjectName("channel1Button")
        self.gridLayout_5.addWidget(self.channel1Button, 2, 1, 1, 1)
        self.channel2colour = QtWidgets.QCheckBox(self.layoutWidget2)
        self.channel2colour.setMaximumSize(QtCore.QSize(5, 22))
        self.channel2colour.setText("")
        self.channel2colour.setCheckable(False)
        self.channel2colour.setObjectName("channel2colour")
        self.gridLayout_5.addWidget(self.channel2colour, 3, 0, 1, 1)
        self.channel2Button = QtWidgets.QPushButton(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channel2Button.sizePolicy().hasHeightForWidth())
        self.channel2Button.setSizePolicy(sizePolicy)
        self.channel2Button.setCheckable(True)
        self.channel2Button.setObjectName("channel2Button")
        self.gridLayout_5.addWidget(self.channel2Button, 3, 1, 1, 1)
        self.channel3colour = QtWidgets.QCheckBox(self.layoutWidget2)
        self.channel3colour.setMaximumSize(QtCore.QSize(5, 22))
        self.channel3colour.setText("")
        self.channel3colour.setCheckable(False)
        self.channel3colour.setObjectName("channel3colour")
        self.gridLayout_5.addWidget(self.channel3colour, 4, 0, 1, 1)
        self.channel3Button = QtWidgets.QPushButton(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channel3Button.sizePolicy().hasHeightForWidth())
        self.channel3Button.setSizePolicy(sizePolicy)
        self.channel3Button.setCheckable(True)
        self.channel3Button.setObjectName("channel3Button")
        self.gridLayout_5.addWidget(self.channel3Button, 4, 1, 1, 1)
        self.channel4colour = QtWidgets.QCheckBox(self.layoutWidget2)
        self.channel4colour.setMaximumSize(QtCore.QSize(5, 22))
        self.channel4colour.setText("")
        self.channel4colour.setCheckable(False)
        self.channel4colour.setObjectName("channel4colour")
        self.gridLayout_5.addWidget(self.channel4colour, 5, 0, 1, 1)
        self.channel4Button = QtWidgets.QPushButton(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channel4Button.sizePolicy().hasHeightForWidth())
        self.channel4Button.setSizePolicy(sizePolicy)
        self.channel4Button.setCheckable(True)
        self.channel4Button.setObjectName("channel4Button")
        self.gridLayout_5.addWidget(self.channel4Button, 5, 1, 1, 1)
        self.channel5colour = QtWidgets.QCheckBox(self.layoutWidget2)
        self.channel5colour.setMaximumSize(QtCore.QSize(5, 22))
        self.channel5colour.setText("")
        self.channel5colour.setCheckable(False)
        self.channel5colour.setObjectName("channel5colour")
        self.gridLayout_5.addWidget(self.channel5colour, 6, 0, 1, 1)
        self.channel5Button = QtWidgets.QPushButton(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channel5Button.sizePolicy().hasHeightForWidth())
        self.channel5Button.setSizePolicy(sizePolicy)
        self.channel5Button.setCheckable(True)
        self.channel5Button.setObjectName("channel5Button")
        self.gridLayout_5.addWidget(self.channel5Button, 6, 1, 1, 1)
        self.channel6Button = QtWidgets.QPushButton(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channel6Button.sizePolicy().hasHeightForWidth())
        self.channel6Button.setSizePolicy(sizePolicy)
        self.channel6Button.setCheckable(True)
        self.channel6Button.setObjectName("channel6Button")
        self.gridLayout_5.addWidget(self.channel6Button, 7, 1, 1, 1)
        self.channel7Button = QtWidgets.QPushButton(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channel7Button.sizePolicy().hasHeightForWidth())
        self.channel7Button.setSizePolicy(sizePolicy)
        self.channel7Button.setCheckable(True)
        self.channel7Button.setObjectName("channel7Button")
        self.gridLayout_5.addWidget(self.channel7Button, 8, 1, 1, 1)
        self.channel8colour = QtWidgets.QCheckBox(self.layoutWidget2)
        self.channel8colour.setMaximumSize(QtCore.QSize(5, 22))
        self.channel8colour.setText("")
        self.channel8colour.setCheckable(False)
        self.channel8colour.setObjectName("channel8colour")
        self.gridLayout_5.addWidget(self.channel8colour, 9, 0, 1, 1)
        self.channel8Button = QtWidgets.QPushButton(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channel8Button.sizePolicy().hasHeightForWidth())
        self.channel8Button.setSizePolicy(sizePolicy)
        self.channel8Button.setCheckable(True)
        self.channel8Button.setObjectName("channel8Button")
        self.gridLayout_5.addWidget(self.channel8Button, 9, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem1, 10, 1, 1, 1)
        self.toolBox.addItem(self.UserInst, "")
        self.verticalLayout.addWidget(self.toolBox)
        self.gridLayout_2.addWidget(self.groupBox_2, 0, 1, 2, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setStyleSheet("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.mplwindow = QtWidgets.QWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mplwindow.sizePolicy().hasHeightForWidth())
        self.mplwindow.setSizePolicy(sizePolicy)
        self.mplwindow.setStyleSheet("")
        self.mplwindow.setObjectName("mplwindow")
        self.mplvl = QtWidgets.QVBoxLayout(self.mplwindow)
        self.mplvl.setContentsMargins(9, 9, 9, 9)
        self.mplvl.setSpacing(9)
        self.mplvl.setObjectName("mplvl")
        self.gridLayout_4.addWidget(self.mplwindow, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 905, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuInstrument = QtWidgets.QMenu(self.menubar)
        self.menuInstrument.setObjectName("menuInstrument")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuSegment_Data = QtWidgets.QMenu(self.menuTools)
        self.menuSegment_Data.setObjectName("menuSegment_Data")
        self.menuRawData = QtWidgets.QMenu(self.menuSegment_Data)
        self.menuRawData.setObjectName("menuRawData")
        self.menuProcessedData = QtWidgets.QMenu(self.menuSegment_Data)
        self.menuProcessedData.setObjectName("menuProcessedData")
        self.menuData_Filters = QtWidgets.QMenu(self.menuTools)
        self.menuData_Filters.setObjectName("menuData_Filters")
        self.menuData_Viewers = QtWidgets.QMenu(self.menuTools)
        self.menuData_Viewers.setObjectName("menuData_Viewers")
        MainWindow.setMenuBar(self.menubar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionConfiguration = QtWidgets.QAction(MainWindow)
        self.actionConfiguration.setObjectName("actionConfiguration")
        self.actionControllerEditor = QtWidgets.QAction(MainWindow)
        self.actionControllerEditor.setObjectName("actionControllerEditor")
        self.actionObserveratory = QtWidgets.QAction(MainWindow)
        self.actionObserveratory.setObjectName("actionObserveratory")
        self.actionManual = QtWidgets.QAction(MainWindow)
        self.actionManual.setObjectName("actionManual")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.actionInstrumentBuilder = QtWidgets.QAction(MainWindow)
        self.actionInstrumentBuilder.setObjectName("actionInstrumentBuilder")
        self.actionInstrument_Attributes = QtWidgets.QAction(MainWindow)
        self.actionInstrument_Attributes.setObjectName("actionInstrument_Attributes")
        self.actionInstrument_Attrib = QtWidgets.QAction(MainWindow)
        self.actionInstrument_Attrib.setObjectName("actionInstrument_Attrib")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionReleaseNotes = QtWidgets.QAction(MainWindow)
        self.actionReleaseNotes.setObjectName("actionReleaseNotes")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave_RawData = QtWidgets.QAction(MainWindow)
        self.actionSave_RawData.setObjectName("actionSave_RawData")
        self.actionSave_Processed_Data = QtWidgets.QAction(MainWindow)
        self.actionSave_Processed_Data.setObjectName("actionSave_Processed_Data")
        self.actionDay = QtWidgets.QAction(MainWindow)
        self.actionDay.setObjectName("actionDay")
        self.actionWeek = QtWidgets.QAction(MainWindow)
        self.actionWeek.setObjectName("actionWeek")
        self.actionMetadata = QtWidgets.QAction(MainWindow)
        self.actionMetadata.setObjectName("actionMetadata")
        self.SegmentRawDataDay = QtWidgets.QAction(MainWindow)
        self.SegmentRawDataDay.setObjectName("SegmentRawDataDay")
        self.SegmentRawDataWeek = QtWidgets.QAction(MainWindow)
        self.SegmentRawDataWeek.setObjectName("SegmentRawDataWeek")
        self.SegmentProcessDataDay = QtWidgets.QAction(MainWindow)
        self.SegmentProcessDataDay.setObjectName("SegmentProcessDataDay")
        self.SegmentProcessDataWeek = QtWidgets.QAction(MainWindow)
        self.SegmentProcessDataWeek.setObjectName("SegmentProcessDataWeek")
        self.actionNon_Linear_Static_Remover = QtWidgets.QAction(MainWindow)
        self.actionNon_Linear_Static_Remover.setObjectName("actionNon_Linear_Static_Remover")
        self.actionPeak_Extractor = QtWidgets.QAction(MainWindow)
        self.actionPeak_Extractor.setObjectName("actionPeak_Extractor")
        self.actionRunning_Average = QtWidgets.QAction(MainWindow)
        self.actionRunning_Average.setObjectName("actionRunning_Average")
        self.actionWeighted_Running_Average = QtWidgets.QAction(MainWindow)
        self.actionWeighted_Running_Average.setObjectName("actionWeighted_Running_Average")
        self.actionRaw_Data = QtWidgets.QAction(MainWindow)
        self.actionRaw_Data.setObjectName("actionRaw_Data")
        self.actionProcessed_Data = QtWidgets.QAction(MainWindow)
        self.actionProcessed_Data.setObjectName("actionProcessed_Data")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave_RawData)
        self.menuFile.addAction(self.actionSave_Processed_Data)
        self.menuFile.addAction(self.actionConfiguration)
        self.menuFile.addAction(self.actionExit)
        self.menuAbout.addAction(self.actionAbout)
        self.menuAbout.addAction(self.actionReleaseNotes)
        self.menuEdit.addAction(self.actionInstrument_Attrib)
        self.menuRawData.addAction(self.SegmentRawDataDay)
        self.menuRawData.addAction(self.SegmentRawDataWeek)
        self.menuProcessedData.addAction(self.SegmentProcessDataDay)
        self.menuProcessedData.addAction(self.SegmentProcessDataWeek)
        self.menuSegment_Data.addAction(self.menuRawData.menuAction())
        self.menuSegment_Data.addAction(self.menuProcessedData.menuAction())
        self.menuData_Filters.addAction(self.actionNon_Linear_Static_Remover)
        self.menuData_Filters.addAction(self.actionPeak_Extractor)
        self.menuData_Filters.addAction(self.actionRunning_Average)
        self.menuData_Filters.addAction(self.actionWeighted_Running_Average)
        self.menuData_Viewers.addAction(self.actionRaw_Data)
        self.menuData_Viewers.addAction(self.actionProcessed_Data)
        self.menuTools.addAction(self.menuData_Filters.menuAction())
        self.menuTools.addAction(self.menuData_Viewers.menuAction())
        self.menuTools.addAction(self.actionMetadata)
        self.menuTools.addAction(self.menuSegment_Data.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuInstrument.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(1)
        self.toolBox.layout().setSpacing(4)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Status"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Control Panel"))
        self.label.setText(_translate("MainWindow", "Module"))
        self.label_3.setText(_translate("MainWindow", "Command"))
        self.label_2.setText(_translate("MainWindow", "Parameter"))
        self.executeButton.setText(_translate("MainWindow", "Execute"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.UserCtrl), _translate("MainWindow", "Instrument"))
        self.showLegend.setText(_translate("MainWindow", "Show Legend"))
        self.channel0Button.setText(_translate("MainWindow", "PushButton"))
        self.channel1Button.setText(_translate("MainWindow", "PushButton"))
        self.channel2Button.setText(_translate("MainWindow", "PushButton"))
        self.channel3Button.setText(_translate("MainWindow", "PushButton"))
        self.channel4Button.setText(_translate("MainWindow", "PushButton"))
        self.channel5Button.setText(_translate("MainWindow", "PushButton"))
        self.channel6Button.setText(_translate("MainWindow", "PushButton"))
        self.channel7Button.setText(_translate("MainWindow", "PushButton"))
        self.channel8Button.setText(_translate("MainWindow", "PushButton"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.UserInst), _translate("MainWindow", "Chart Control"))
        self.groupBox.setTitle(_translate("MainWindow", "Chart"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "Info"))
        self.menuEdit.setTitle(_translate("MainWindow", "Instrument Attributes"))
        self.menuInstrument.setTitle(_translate("MainWindow", "Instruments"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuSegment_Data.setTitle(_translate("MainWindow", "Segment Data"))
        self.menuRawData.setTitle(_translate("MainWindow", "RawData"))
        self.menuProcessedData.setTitle(_translate("MainWindow", "ProcessedData"))
        self.menuData_Filters.setTitle(_translate("MainWindow", "Data Filters"))
        self.menuData_Viewers.setTitle(_translate("MainWindow", "Data Viewers"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionConfiguration.setText(_translate("MainWindow", "Configuration"))
        self.actionControllerEditor.setText(_translate("MainWindow", "Futurlec Controller"))
        self.actionObserveratory.setText(_translate("MainWindow", "Observeratory"))
        self.actionManual.setText(_translate("MainWindow", "Manual"))
        self.action.setText(_translate("MainWindow", "About"))
        self.actionInstrumentBuilder.setText(_translate("MainWindow", "Instrument Builder"))
        self.actionInstrument_Attributes.setText(_translate("MainWindow", "Instrument Attributes"))
        self.actionInstrument_Attrib.setText(_translate("MainWindow", "Instrument Attributes"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionReleaseNotes.setText(_translate("MainWindow", "ReleaseNotes"))
        self.actionOpen.setText(_translate("MainWindow", "Import Data"))
        self.actionSave_RawData.setText(_translate("MainWindow", "Export Raw Data"))
        self.actionSave_Processed_Data.setText(_translate("MainWindow", "Export Processed Data"))
        self.actionDay.setText(_translate("MainWindow", "Day"))
        self.actionWeek.setText(_translate("MainWindow", "Week"))
        self.actionMetadata.setText(_translate("MainWindow", "Metadata"))
        self.SegmentRawDataDay.setText(_translate("MainWindow", "Day"))
        self.SegmentRawDataWeek.setText(_translate("MainWindow", "Week"))
        self.SegmentProcessDataDay.setText(_translate("MainWindow", "Day"))
        self.SegmentProcessDataWeek.setText(_translate("MainWindow", "Week"))
        self.actionNon_Linear_Static_Remover.setText(_translate("MainWindow", "Non Linear Static Remover"))
        self.actionPeak_Extractor.setText(_translate("MainWindow", "Peak Extractor"))
        self.actionRunning_Average.setText(_translate("MainWindow", "Running Average"))
        self.actionWeighted_Running_Average.setText(_translate("MainWindow", "Weighted Running Average"))
        self.actionRaw_Data.setText(_translate("MainWindow", "RawData"))
        self.actionProcessed_Data.setText(_translate("MainWindow", "ProcessedData"))

