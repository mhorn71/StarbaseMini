# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dataViewer.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DataViewerDialog(object):
    def setupUi(self, DataViewerDialog):
        DataViewerDialog.setObjectName("DataViewerDialog")
        DataViewerDialog.resize(640, 480)
        self.gridLayout = QtWidgets.QGridLayout(DataViewerDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.DataViewTableWidget = QtWidgets.QTableWidget(DataViewerDialog)
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
        self.DataViewTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.DataViewTableWidget.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        self.DataViewTableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.DataViewTableWidget.setObjectName("DataViewTableWidget")
        self.DataViewTableWidget.setColumnCount(0)
        self.DataViewTableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.DataViewTableWidget, 0, 0, 1, 1)

        self.retranslateUi(DataViewerDialog)
        QtCore.QMetaObject.connectSlotsByName(DataViewerDialog)

    def retranslateUi(self, DataViewerDialog):
        _translate = QtCore.QCoreApplication.translate
        DataViewerDialog.setWindowTitle(_translate("DataViewerDialog", "Dialog"))

