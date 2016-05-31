# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dataViewer.ui'
#
# Created: Tue May 31 14:43:57 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DataViewerDialog(object):
    def setupUi(self, DataViewerDialog):
        DataViewerDialog.setObjectName("DataViewerDialog")
        DataViewerDialog.resize(640, 480)
        self.gridLayout = QtGui.QGridLayout(DataViewerDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.DataViewTableWidget = QtGui.QTableWidget(DataViewerDialog)
        self.DataViewTableWidget.setStyleSheet("QTableWidget {\n"
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
        self.DataViewTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.DataViewTableWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.DataViewTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.DataViewTableWidget.setObjectName("DataViewTableWidget")
        self.DataViewTableWidget.setColumnCount(0)
        self.DataViewTableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.DataViewTableWidget, 0, 0, 1, 1)

        self.retranslateUi(DataViewerDialog)
        QtCore.QMetaObject.connectSlotsByName(DataViewerDialog)

    def retranslateUi(self, DataViewerDialog):
        DataViewerDialog.setWindowTitle(QtGui.QApplication.translate("DataViewerDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

