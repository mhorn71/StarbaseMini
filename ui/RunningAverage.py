# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RunningAverage.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RunningAverageDialog(object):
    def setupUi(self, RunningAverageDialog):
        RunningAverageDialog.setObjectName("RunningAverageDialog")
        RunningAverageDialog.resize(275, 84)
        self.gridLayout = QtWidgets.QGridLayout(RunningAverageDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(RunningAverageDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(RunningAverageDialog)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(RunningAverageDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(RunningAverageDialog)
        self.buttonBox.accepted.connect(RunningAverageDialog.accept)
        self.buttonBox.rejected.connect(RunningAverageDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RunningAverageDialog)

    def retranslateUi(self, RunningAverageDialog):
        _translate = QtCore.QCoreApplication.translate
        RunningAverageDialog.setWindowTitle(_translate("RunningAverageDialog", "Running Average"))
        self.label.setText(_translate("RunningAverageDialog", "Average over n sequential samples"))

