__author__ = 'mark'
# StarbaseMini Staribus/Starinet Client for the British Astronomical Association Staribus Protocol
# Copyright (C) 2015  Mark Horn
#
# This file is part of StarbaseMini.
#
# StarbaseMini is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# StarbaseMini is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with StarbaseMini.  If not, see <http://www.gnu.org/licenses/>.

import sys
import logging

from PyQt4 import QtGui, QtCore

import constants
from ui import Ui_InstrumentAttributesDialog

logger = logging.getLogger('instrument.builder')


class InstrumentAttrib(QtGui.QDialog, Ui_InstrumentAttributesDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        # Style sheets
        stylebool = False

        if sys.platform.startswith('darwin'):
            stylesheet = 'css/macStyle.css'
            stylebool = True
        elif sys.platform.startswith('win32'):
            stylesheet = 'css/winStyle.css'
            stylebool = True
        elif sys.platform.startswith('linux'):
            stylesheet = 'css/nixStyle.css'
            stylebool = True

        if stylebool:
            with open(stylesheet, 'r') as style:
                self.setStyleSheet(style.read())

        self.instrument = None
        self.instrument_file = None

        self.staribus_address_orig = None
        self.starinet_address_orig = None
        self.starinet_port_orig = None

        for i in range(0, 253):
            self.comboBox.addItem(str(i))

        self.PickerButton0.clicked.connect(self.colour_picker)
        self.PickerButton1.clicked.connect(self.colour_picker)
        self.PickerButton2.clicked.connect(self.colour_picker)
        self.PickerButton3.clicked.connect(self.colour_picker)
        self.PickerButton4.clicked.connect(self.colour_picker)
        self.PickerButton5.clicked.connect(self.colour_picker)
        self.PickerButton6.clicked.connect(self.colour_picker)
        self.PickerButton7.clicked.connect(self.colour_picker)
        self.PickerButton8.clicked.connect(self.colour_picker)



    def set(self, instrument, instrument_file):
        self.instrument = instrument
        self.instrument_file = instrument_file

        self.comboBox.setCurrentIndex(int(self.instrument.instrument_staribus_address))
        self.staribus_address_orig = self.instrument.instrument_staribus_address

        # OyLatitudeLineEditRegexp = QtCore.QRegExp(constants.observatory_latitude)
        # OyLatitudeLineEditValidator = QtGui.QRegExpValidator(OyLatitudeLineEditRegexp)
        # self.OyLatitudeLineEdit.setValidator(OyLatitudeLineEditValidator)
        # self.OyLatitudeLineEdit.textChanged.connect(self.parameter_check_state)
        # self.OyLatitudeLineEdit.textChanged.emit(self.OyLatitudeLineEdit.text())

        if self.instrument.instrument_starinet_address == 'None':
            self.StarinetAddressLineEdit.setEnabled(False)
        else:
            self.comboBox.setEnabled(False)
            self.starinet_address_orig = self.instrument.instrument_starinet_address
            self.StarinetAddressLineEdit.setText(self.instrument.instrument_starinet_address)
            StarinetAddressRegex = QtCore.QRegExp(constants.starinet_ip)
            StarinetAddressValidator = QtGui.QRegExpValidator(StarinetAddressRegex)
            self.StarinetAddressLineEdit.setValidator(StarinetAddressValidator)
            self.StarinetAddressLineEdit.textChanged.connect(self.parameter_check_state)
            self.StarinetAddressLineEdit.textChanged.emit(self.StarinetAddressLineEdit.text())

        if self.instrument.instrument_starinet_port == 'None':
            self.StarinetPortLineEdit.setEnabled(False)
        else:
            self.StarinetPortLineEdit.setText(self.instrument.instrument_starinet_port)
            self.starinet_port_orig = self.instrument.instrument_starinet_port
            StarinetPortRegex = QtCore.QRegExp(constants.starinet_port)
            StarinetPortValidator = QtGui.QRegExpValidator(StarinetPortRegex)
            self.StarinetPortLineEdit.setValidator(StarinetPortValidator)
            self.StarinetPortLineEdit.textChanged.connect(self.parameter_check_state)
            self.StarinetPortLineEdit.textChanged.emit(self.StarinetPortLineEdit.text())

    def colour_picker(self):
        print('colour picker selected...')

    def parameter_check_state(self, *args, **kwargs):

        # This bit is a bit of bodge as parameter check state will trigger when loading and raise
        # AttributeError so we just ignore it, not ideal!

        try:
            sender = self.sender()
            validator = sender.validator()
            state = validator.validate(sender.text(), 0)[0]
        except AttributeError:
            pass

        if state == QtGui.QValidator.Acceptable and len(sender.text()) == 0:
            color = '#ffffff'  # white
            sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
        elif state == QtGui.QValidator.Acceptable:
            color = '#c4df9b'  # green
            sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
        elif state == QtGui.QValidator.Intermediate:
            color = '#fff79a'  # yellow
            sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
        else:
            sender.setStyleSheet('QLineEdit { background-color: #f6989d')