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
import os
import xml.etree.ElementTree as ET
import re

from PyQt4 import QtGui, QtCore

import constants
from ui import Ui_InstrumentAttributesDialog

logger = logging.getLogger('instrument.attributes_updater')


class InstrumentAttrib(QtGui.QDialog, Ui_InstrumentAttributesDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        self.home_path = os.path.expanduser('~') + os.path.sep + '.starbasemini' + os.path.sep + 'instruments' + \
                         os.path.sep

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
        self.channel_labels = []
        self.channel_colours = []

        self.response_message = 'ABORT', None
        self.reload = False

        self.starinetaddressbool = True
        self.starinetportbool = True

        for i in range(0, 253):
            self.comboBox.addItem(str(i))

        self.colorDialog = QtGui.QColorDialog()
        self.colorDialog.setOption(QtGui.QColorDialog.ShowAlphaChannel, False)
        self.colorDialog.setOption(QtGui.QColorDialog.DontUseNativeDialog, False)

        self.buttonBox.accepted.connect(self.accept_called)
        self.buttonBox.rejected.connect(self.reject_called)
        self.buttonBox.button(QtGui.QDialogButtonBox.RestoreDefaults).clicked.connect(self.defaults_called)

        self.PickerButton0.clicked.connect(self.chan0_picker)
        self.PickerButton1.clicked.connect(self.chan1_picker)
        self.PickerButton2.clicked.connect(self.chan2_picker)
        self.PickerButton3.clicked.connect(self.chan3_picker)
        self.PickerButton4.clicked.connect(self.chan4_picker)
        self.PickerButton5.clicked.connect(self.chan5_picker)
        self.PickerButton6.clicked.connect(self.chan6_picker)
        self.PickerButton7.clicked.connect(self.chan7_picker)
        self.PickerButton8.clicked.connect(self.chan8_picker)

        self.Chan0LabelEdit.setEnabled(False)
        self.Chan0ColourLineEdit.setEnabled(False)
        self.PickerButton0.setEnabled(False)

        self.Chan1LabelEdit.setEnabled(False)
        self.Chan1ColourLineEdit.setEnabled(False)
        self.PickerButton1.setEnabled(False)

        self.Chan2LabelEdit.setEnabled(False)
        self.Chan2ColourLineEdit.setEnabled(False)
        self.PickerButton2.setEnabled(False)

        self.Chan3LabelEdit.setEnabled(False)
        self.Chan3ColourLineEdit.setEnabled(False)
        self.PickerButton3.setEnabled(False)

        self.Chan4LabelEdit.setEnabled(False)
        self.Chan4ColourLineEdit.setEnabled(False)
        self.PickerButton4.setEnabled(False)

        self.Chan5LabelEdit.setEnabled(False)
        self.Chan5ColourLineEdit.setEnabled(False)
        self.PickerButton5.setEnabled(False)

        self.Chan6LabelEdit.setEnabled(False)
        self.Chan6ColourLineEdit.setEnabled(False)
        self.PickerButton6.setEnabled(False)

        self.Chan7LabelEdit.setEnabled(False)
        self.Chan7ColourLineEdit.setEnabled(False)
        self.PickerButton7.setEnabled(False)

        self.Chan8LabelEdit.setEnabled(False)
        self.Chan8ColourLineEdit.setEnabled(False)
        self.PickerButton8.setEnabled(False)

    def Picker0(self):

        if re.match(constants.channel_hex_color, self.Chan0ColourLineEdit.text()):
            self.PickerButton0.setStyleSheet('QPushButton { background-color: ' + self.Chan0ColourLineEdit.text() + ';' +
                                             'border-width: 1px; border-radius: 3px;' +
                                             'border-color: beige; padding: 5px;' +
                                             'margin-top: 0px; }')
    def Picker1(self):
        if re.match(constants.channel_hex_color, self.Chan1ColourLineEdit.text()):
            self.PickerButton1.setStyleSheet('QPushButton { background-color: ' + self.Chan1ColourLineEdit.text() + ';' +
                                             'border-width: 1px; border-radius: 3px;' +
                                             'border-color: beige; padding: 5px;' +
                                             'margin-top: 0px; }')
    def Picker2(self):
        if re.match(constants.channel_hex_color, self.Chan2ColourLineEdit.text()):
            self.PickerButton2.setStyleSheet('QPushButton { background-color: ' + self.Chan2ColourLineEdit.text() + ';' +
                                             'border-width: 1px; border-radius: 3px;' +
                                             'border-color: beige; padding: 5px;' +
                                             'margin-top: 0px; }')
    def Picker3(self):
        if re.match(constants.channel_hex_color, self.Chan3ColourLineEdit.text()):
            self.PickerButton3.setStyleSheet('QPushButton { background-color: ' + self.Chan3ColourLineEdit.text() + ';' +
                                             'border-width: 1px; border-radius: 3px;' +
                                             'border-color: beige; padding: 5px;' +
                                             'margin-top: 0px; }')

    def Picker4(self):
        if re.match(constants.channel_hex_color, self.Chan4ColourLineEdit.text()):
            self.PickerButton4.setStyleSheet('QPushButton { background-color: ' + self.Chan4ColourLineEdit.text() + ';' +
                                             'border-width: 1px; border-radius: 3px;' +
                                             'border-color: beige; padding: 5px;' +
                                             'margin-top: 0px; }')
    def Picker5(self):
        if re.match(constants.channel_hex_color, self.Chan5ColourLineEdit.text()):
            self.PickerButton5.setStyleSheet('QPushButton { background-color: ' + self.Chan5ColourLineEdit.text() + ';' +
                                             'border-width: 1px; border-radius: 3px;' +
                                             'border-color: beige; padding: 5px;' +
                                             'margin-top: 0px; }')

    def Picker6(self):
        if re.match(constants.channel_hex_color, self.Chan6ColourLineEdit.text()):
            self.PickerButton6.setStyleSheet('QPushButton { background-color: ' + self.Chan6ColourLineEdit.text() + ';' +
                                             'border-width: 1px; border-radius: 3px;' +
                                             'border-color: beige; padding: 5px;' +
                                             'margin-top: 0px; }')

    def Picker7(self):
        if re.match(constants.channel_hex_color, self.Chan7ColourLineEdit.text()):
            self.PickerButton7.setStyleSheet('QPushButton { background-color: ' + self.Chan7ColourLineEdit.text() + ';' +
                                             'border-width: 1px; border-radius: 3px;' +
                                             'border-color: beige; padding: 5px;' +
                                             'margin-top: 0px; }')

    def Picker8(self):
        if re.match(constants.channel_hex_color, self.Chan8ColourLineEdit.text()):
            self.PickerButton8.setStyleSheet('QPushButton { background-color: ' + self.Chan8ColourLineEdit.text() + ';' +
                                             'border-width: 1px; border-radius: 3px;' +
                                             'border-color: beige; padding: 5px;' +
                                             'margin-top: 0px; }')

    def channel0(self):
        self.Chan0LabelEdit.setEnabled(True)
        self.Chan0LabelEdit.setText(self.instrument.channel_names[0])
        Chan0LabelRegex = QtCore.QRegExp(constants.channel_name)
        self.Chan0LabelEdit.setValidator(QtGui.QRegExpValidator(Chan0LabelRegex))
        self.Chan0LabelEdit.textChanged.connect(self.parameter_check_state)
        self.Chan0LabelEdit.textChanged.emit(self.Chan0LabelEdit.text())

        self.Chan0ColourLineEdit.setEnabled(True)
        self.Chan0ColourLineEdit.setText(self.instrument.channel_colours[0])
        Chan0ColourRegex = QtCore.QRegExp(constants.channel_hex_color)
        self.Chan0ColourLineEdit.setValidator(QtGui.QRegExpValidator(Chan0ColourRegex))
        self.Chan0ColourLineEdit.textChanged.connect(self.parameter_check_state)
        self.Chan0ColourLineEdit.textChanged.connect(self.Picker0)
        self.Chan0ColourLineEdit.textChanged.emit(self.Chan0ColourLineEdit.text())

        self.PickerButton0.setEnabled(True)

    def channel1(self):
        self.Chan1LabelEdit.setEnabled(True)
        self.Chan1LabelEdit.setText(self.instrument.channel_names[1])
        Chan1LabelRegex = QtCore.QRegExp(constants.channel_name)
        self.Chan1LabelEdit.setValidator(QtGui.QRegExpValidator(Chan1LabelRegex))
        self.Chan1LabelEdit.textChanged.connect(self.parameter_check_state)
        self.Chan1ColourLineEdit.textChanged.connect(self.Picker1)
        self.Chan1LabelEdit.textChanged.emit(self.Chan1LabelEdit.text())

        self.Chan1ColourLineEdit.setEnabled(True)
        self.Chan1ColourLineEdit.setText(self.instrument.channel_colours[1])
        Chan1ColourRegex = QtCore.QRegExp(constants.channel_hex_color)
        self.Chan1ColourLineEdit.setValidator(QtGui.QRegExpValidator(Chan1ColourRegex))
        self.Chan1ColourLineEdit.textChanged.connect(self.parameter_check_state)
        self.Chan1ColourLineEdit.textChanged.emit(self.Chan1ColourLineEdit.text())

        self.PickerButton1.setEnabled(True)

    def channel2(self):
        self.Chan2LabelEdit.setEnabled(True)
        self.Chan2LabelEdit.setText(self.instrument.channel_names[2])
        Chan2LabelRegex = QtCore.QRegExp(constants.channel_name)
        self.Chan2LabelEdit.setValidator(QtGui.QRegExpValidator(Chan2LabelRegex))
        self.Chan2LabelEdit.textChanged.connect(self.parameter_check_state)
        self.Chan2ColourLineEdit.textChanged.connect(self.Picker2)
        self.Chan2LabelEdit.textChanged.emit(self.Chan2LabelEdit.text())

        self.Chan2ColourLineEdit.setEnabled(True)
        self.Chan2ColourLineEdit.setText(self.instrument.channel_colours[2])
        Chan2ColourRegex = QtCore.QRegExp(constants.channel_hex_color)
        self.Chan2ColourLineEdit.setValidator(QtGui.QRegExpValidator(Chan2ColourRegex))
        self.Chan2ColourLineEdit.textChanged.connect(self.parameter_check_state)
        self.Chan2ColourLineEdit.textChanged.emit(self.Chan2ColourLineEdit.text())

        self.PickerButton2.setEnabled(True)

    def channel3(self):
        self.Chan3LabelEdit.setEnabled(True)
        self.Chan3LabelEdit.setText(self.instrument.channel_names[3])
        Chan3LabelRegex = QtCore.QRegExp(constants.channel_name)
        self.Chan3LabelEdit.setValidator(QtGui.QRegExpValidator(Chan3LabelRegex))
        self.Chan3LabelEdit.textChanged.connect(self.parameter_check_state)
        self.Chan3ColourLineEdit.textChanged.connect(self.Picker3)
        self.Chan3LabelEdit.textChanged.emit(self.Chan3LabelEdit.text())

        self.Chan3ColourLineEdit.setEnabled(True)
        self.Chan3ColourLineEdit.setText(self.instrument.channel_colours[3])
        Chan3ColourRegex = QtCore.QRegExp(constants.channel_hex_color)
        self.Chan3ColourLineEdit.setValidator(QtGui.QRegExpValidator(Chan3ColourRegex))
        self.Chan3ColourLineEdit.textChanged.connect(self.parameter_check_state)
        self.Chan3ColourLineEdit.textChanged.emit(self.Chan3ColourLineEdit.text())

        self.PickerButton3.setEnabled(True)

    def channel4(self):
        self.Chan4LabelEdit.setEnabled(True)
        self.Chan4LabelEdit.setText(self.instrument.channel_names[4])
        Chan4LabelRegex = QtCore.QRegExp(constants.channel_name)
        self.Chan4LabelEdit.setValidator(QtGui.QRegExpValidator(Chan4LabelRegex))
        self.Chan4LabelEdit.textChanged.connect(self.parameter_check_state)
        self.Chan4ColourLineEdit.textChanged.connect(self.Picker4)
        self.Chan4LabelEdit.textChanged.emit(self.Chan4LabelEdit.text())

        self.Chan4ColourLineEdit.setEnabled(True)
        self.Chan4ColourLineEdit.setText(self.instrument.channel_colours[4])
        Chan4ColourRegex = QtCore.QRegExp(constants.channel_hex_color)
        self.Chan4ColourLineEdit.setValidator(QtGui.QRegExpValidator(Chan4ColourRegex))
        self.Chan4ColourLineEdit.textChanged.connect(self.parameter_check_state)
        self.Chan4ColourLineEdit.textChanged.emit(self.Chan4ColourLineEdit.text())

        self.PickerButton4.setEnabled(True)

    def channel5(self):
        self.Chan5LabelEdit.setEnabled(True)
        self.Chan5LabelEdit.setText(self.instrument.channel_names[5])
        Chan5LabelRegex = QtCore.QRegExp(constants.channel_name)
        self.Chan5LabelEdit.setValidator(QtGui.QRegExpValidator(Chan5LabelRegex))
        self.Chan5LabelEdit.textChanged.connect(self.parameter_check_state)
        self.Chan5ColourLineEdit.textChanged.connect(self.Picker5)
        self.Chan5LabelEdit.textChanged.emit(self.Chan5LabelEdit.text())

        self.Chan5ColourLineEdit.setEnabled(True)
        self.Chan5ColourLineEdit.setText(self.instrument.channel_colours[5])
        Chan5ColourRegex = QtCore.QRegExp(constants.channel_hex_color)
        self.Chan5ColourLineEdit.setValidator(QtGui.QRegExpValidator(Chan5ColourRegex))
        self.Chan5ColourLineEdit.textChanged.connect(self.parameter_check_state)
        self.Chan5ColourLineEdit.textChanged.emit(self.Chan5ColourLineEdit.text())

        self.PickerButton5.setEnabled(True)

    def channel6(self):
        self.Chan6LabelEdit.setEnabled(True)
        self.Chan6LabelEdit.setText(self.instrument.channel_names[6])
        Chan6LabelRegex = QtCore.QRegExp(constants.channel_name)
        self.Chan6LabelEdit.setValidator(QtGui.QRegExpValidator(Chan6LabelRegex))
        self.Chan6LabelEdit.textChanged.connect(self.parameter_check_state)
        self.Chan6LabelEdit.textChanged.emit(self.Chan6LabelEdit.text())

        self.Chan6ColourLineEdit.setEnabled(True)
        self.Chan6ColourLineEdit.setText(self.instrument.channel_colours[6])
        Chan6ColourRegex = QtCore.QRegExp(constants.channel_hex_color)
        self.Chan6ColourLineEdit.setValidator(QtGui.QRegExpValidator(Chan6ColourRegex))
        self.Chan6ColourLineEdit.textChanged.connect(self.parameter_check_state)
        self.Chan6ColourLineEdit.textChanged.connect(self.Picker6)
        self.Chan6ColourLineEdit.textChanged.emit(self.Chan6ColourLineEdit.text())

        self.PickerButton6.setEnabled(True)

    def channel7(self):
        self.Chan7LabelEdit.setEnabled(True)
        self.Chan7LabelEdit.setText(self.instrument.channel_names[7])
        Chan7LabelRegex = QtCore.QRegExp(constants.channel_name)
        self.Chan7LabelEdit.setValidator(QtGui.QRegExpValidator(Chan7LabelRegex))
        self.Chan7LabelEdit.textChanged.connect(self.parameter_check_state)
        self.Chan7LabelEdit.textChanged.emit(self.Chan7LabelEdit.text())

        self.Chan7ColourLineEdit.setEnabled(True)
        self.Chan7ColourLineEdit.setText(self.instrument.channel_colours[7])
        Chan7ColourRegex = QtCore.QRegExp(constants.channel_hex_color)
        self.Chan7ColourLineEdit.setValidator(QtGui.QRegExpValidator(Chan7ColourRegex))
        self.Chan7ColourLineEdit.textChanged.connect(self.parameter_check_state)
        self.Chan7ColourLineEdit.textChanged.connect(self.Picker7)
        self.Chan7ColourLineEdit.textChanged.emit(self.Chan7ColourLineEdit.text())

        self.PickerButton7.setEnabled(True)

    def channel8(self):
        self.Chan8LabelEdit.setEnabled(True)
        self.Chan8LabelEdit.setText(self.instrument.channel_names[8])
        Chan8LabelRegex = QtCore.QRegExp(constants.channel_name)
        self.Chan8LabelEdit.setValidator(QtGui.QRegExpValidator(Chan8LabelRegex))
        self.Chan8LabelEdit.textChanged.connect(self.parameter_check_state)
        self.Chan8LabelEdit.textChanged.emit(self.Chan8LabelEdit.text())

        self.Chan8ColourLineEdit.setEnabled(True)
        self.Chan8ColourLineEdit.setText(self.instrument.channel_colours[8])
        Chan8ColourRegex = QtCore.QRegExp(constants.channel_hex_color)
        self.Chan8ColourLineEdit.setValidator(QtGui.QRegExpValidator(Chan8ColourRegex))
        self.Chan8ColourLineEdit.textChanged.connect(self.parameter_check_state)
        self.Chan8ColourLineEdit.textChanged.connect(self.Picker8)
        self.Chan8ColourLineEdit.textChanged.emit(self.Chan8ColourLineEdit.text())

        self.PickerButton8.setEnabled(True)

    def enable_channel_items(self):

        if self.instrument.instrument_number_of_channels == '2':
            self.channel0()
            self.channel1()
        elif self.instrument.instrument_number_of_channels == '3':
            self.channel0()
            self.channel1()
            self.channel2()
        elif self.instrument.instrument_number_of_channels == '4':
            self.channel0()
            self.channel1()
            self.channel2()
            self.channel3()
        elif self.instrument.instrument_number_of_channels == '5':
            self.channel0()
            self.channel1()
            self.channel2()
            self.channel3()
            self.channel4()
        elif self.instrument.instrument_number_of_channels == '6':
            self.channel0()
            self.channel1()
            self.channel2()
            self.channel3()
            self.channel4()
            self.channel5()
        elif self.instrument.instrument_number_of_channels == '7':
            self.channel0()
            self.channel1()
            self.channel2()
            self.channel3()
            self.channel4()
            self.channel5()
            self.channel6()
        elif self.instrument.instrument_number_of_channels == '8':
            self.channel0()
            self.channel1()
            self.channel2()
            self.channel3()
            self.channel4()
            self.channel5()
            self.channel6()
            self.channel7()
        elif self.instrument.instrument_number_of_channels == '9':
            self.channel0()
            self.channel1()
            self.channel2()
            self.channel3()
            self.channel4()
            self.channel5()
            self.channel6()
            self.channel7()
            self.channel8()

    def set(self, instrument, instrument_file):

        self.instrument = instrument
        self.instrument_file = instrument_file

        self.comboBox.setCurrentIndex(int(self.instrument.instrument_staribus_address))

        self.enable_channel_items()

        if self.instrument.instrument_starinet_address == 'None':
            self.StarinetAddressLineEdit.setEnabled(False)
            self.starinetaddressbool = False
        else:
            self.comboBox.setEnabled(False)

            self.StarinetAddressLineEdit.setText(self.instrument.instrument_starinet_address)
            StarinetAddressValidator = QtGui.QRegExpValidator(QtCore.QRegExp(constants.starinet_ip))
            self.StarinetAddressLineEdit.setValidator(StarinetAddressValidator)
            self.StarinetAddressLineEdit.textChanged.connect(self.parameter_check_state)
            self.StarinetAddressLineEdit.textChanged.emit(self.StarinetAddressLineEdit.text())

        if self.instrument.instrument_starinet_port == 'None':
            self.StarinetPortLineEdit.setEnabled(False)
            self.starinetportbool = False
        else:
            self.StarinetPortLineEdit.setText(self.instrument.instrument_starinet_port)

            StarinetPortValidator = QtGui.QRegExpValidator(QtCore.QRegExp(constants.starinet_port))
            self.StarinetPortLineEdit.setValidator(StarinetPortValidator)
            self.StarinetPortLineEdit.textChanged.connect(self.parameter_check_state)
            self.StarinetPortLineEdit.textChanged.emit(self.StarinetPortLineEdit.text())

    def chan0_picker(self):
        colour = self.colorDialog.getColor()

        if colour.isValid():
            self.Chan0ColourLineEdit.setText(colour.name().upper())

    def chan1_picker(self):
        colour = self.colorDialog.getColor()

        if colour.isValid():
            self.Chan1ColourLineEdit.setText(colour.name().upper())

    def chan2_picker(self):
        colour = self.colorDialog.getColor()

        if colour.isValid():
            self.Chan2ColourLineEdit.setText(colour.name().upper())

    def chan3_picker(self):
        colour = self.colorDialog.getColor()

        if colour.isValid():
            self.Chan3ColourLineEdit.setText(colour.name().upper())

    def chan4_picker(self):
        colour = self.colorDialog.getColor()

        if colour.isValid():
            self.Chan4ColourLineEdit.setText(colour.name().upper())

    def chan5_picker(self):
        colour = self.colorDialog.getColor()

        if colour.isValid():
            self.Chan5ColourLineEdit.setText(colour.name().upper())

    def chan6_picker(self):
        colour = self.colorDialog.getColor()

        if colour.isValid():
            self.Chan6ColourLineEdit.setText(colour.name().upper())

    def chan7_picker(self):
        colour = self.colorDialog.getColor()

        if colour.isValid():
            self.Chan7ColourLineEdit.setText(colour.name().upper())

    def chan8_picker(self):
        colour = self.colorDialog.getColor()

        if colour.isValid():
            self.Chan8ColourLineEdit.setText(colour.name().upper())

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
        elif state == QtGui.QValidator.Intermediate and len(sender.text()) == 0:
            color = '#f6989d'  # red
            sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
        elif state == QtGui.QValidator.Intermediate:
            color = '#fff79a'  # yellow
            sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
        else:
            sender.setStyleSheet('QLineEdit { background-color: #f6989d')

    def create_lists(self):

        del self.channel_labels[:]
        del self.channel_colours[:]

        if len(self.Chan0LabelEdit.text()) != 0:
            self.channel_labels.append(self.Chan0LabelEdit.text())

        if len(self.Chan1LabelEdit.text()) != 0:
            self.channel_labels.append(self.Chan1LabelEdit.text())

        if len(self.Chan2LabelEdit.text()) != 0:
            self.channel_labels.append(self.Chan2LabelEdit.text())

        if len(self.Chan3LabelEdit.text()) != 0:
            self.channel_labels.append(self.Chan3LabelEdit.text())

        if len(self.Chan4LabelEdit.text()) != 0:
            self.channel_labels.append(self.Chan4LabelEdit.text())

        if len(self.Chan5LabelEdit.text()) != 0:
            self.channel_labels.append(self.Chan5LabelEdit.text())

        if len(self.Chan6LabelEdit.text()) != 0:
            self.channel_labels.append(self.Chan6LabelEdit.text())

        if len(self.Chan7LabelEdit.text()) != 0:
            self.channel_labels.append(self.Chan7LabelEdit.text())

        if len(self.Chan8LabelEdit.text()) != 0:
            self.channel_labels.append(self.Chan8LabelEdit.text())

        if len(self.Chan0ColourLineEdit.text()) != 0:
            self.channel_colours.append(self.Chan0ColourLineEdit.text())

        if len(self.Chan1ColourLineEdit.text()) != 0:
            self.channel_colours.append(self.Chan1ColourLineEdit.text())

        if len(self.Chan2ColourLineEdit.text()) != 0:
            self.channel_colours.append(self.Chan2ColourLineEdit.text())

        if len(self.Chan3ColourLineEdit.text()) != 0:
            self.channel_colours.append(self.Chan3ColourLineEdit.text())

        if len(self.Chan4ColourLineEdit.text()) != 0:
            self.channel_colours.append(self.Chan4ColourLineEdit.text())

        if len(self.Chan5ColourLineEdit.text()) != 0:
            self.channel_colours.append(self.Chan5ColourLineEdit.text())

        if len(self.Chan6ColourLineEdit.text()) != 0:
            self.channel_colours.append(self.Chan6ColourLineEdit.text())

        if len(self.Chan7ColourLineEdit.text()) != 0:
            self.channel_colours.append(self.Chan7ColourLineEdit.text())

        if len(self.Chan8ColourLineEdit.text()) != 0:
            self.channel_colours.append(self.Chan8ColourLineEdit.text())

    def defaults_called(self):
        self.response_message = 'SUCCESS', 'Instrument attributes reset defaults'

        # get the instrument xml file minus the original path
        file = self.instrument_file.split(os.path.sep)
        file = file[-1]

        # set the new xml to use the users home path location.
        new_file = self.home_path + file

        try:
            if os.path.isfile(new_file):
                os.unlink(new_file)
        except OSError:
            self.response_message = 'ABORT', 'No Instrument attributes need resetting'
        else:
            self.response_message = 'SUCCESS', 'Instrument attributes reset defaults'


        self.hide()

    def reject_called(self):
        self.response_message = 'ABORT', None
        self.reload = False
        self.hide()

    def accept_called(self):

        self.create_lists()

        execute_state = True

        # Check .starbasemini/instruments exists otherwise create.
        if os.path.isdir(self.home_path) is not True:
            os.makedirs(self.home_path)

        # get the instrument xml file minus the original path
        file = self.instrument_file.split(os.path.sep)
        file = file[-1]

        # set the new xml to use the users home path location.
        new_file = self.home_path + file

        #import xml file
        tree = ET.parse(self.instrument_file)

        staribusaddr = self.comboBox.currentText()
        staribusaddr = staribusaddr.zfill(3)

        staribusaddress = tree.find('StaribusAddress')
        staribusaddress.text = staribusaddr

        starinetaddress = tree.find('StarinetAddress')

        if self.starinetaddressbool:
            if len(self.StarinetAddressLineEdit.text()) != 0:
                starinetaddress.text = self.StarinetAddressLineEdit.text()
            else:
                self.warning_message()
                execute_state = False

        starinetport = tree.find('StarinetPort')

        if self.starinetportbool:
            if len(self.StarinetPortLineEdit.text()) != 0:
                starinetport.text = self.StarinetPortLineEdit.text()
            else:
                self.warning_message()
                execute_state = False

        channel_metadata = tree.findall('ChannelMetadata')

        if len(self.channel_labels) == int(self.instrument.instrument_number_of_channels):

            chanidx = 0

            for metadata in channel_metadata:
                ChannelLabel = metadata.find('ChannelLabel')
                ChannelLabel.text = self.channel_labels[chanidx]
                chanidx += 1

        else:
            self.warning_message()
            execute_state = False

        if len(self.channel_colours) == int(self.instrument.instrument_number_of_channels):

            chanidx = 0

            for metadata in channel_metadata:
                ChannelColour = metadata.find('ChannelColour')
                ChannelColour.text = self.channel_colours[chanidx]
                chanidx += 1
        else:
            self.warning_message()
            execute_state = False

        if execute_state:
            self.write(tree, new_file)

    def warning_message(self):
        QtGui.QMessageBox.information(None, 'WARNING', 'Blank fields not allowed')

    def exit_message(self):
        QtGui.QMessageBox.information(None, 'NOTICE', 'Application restart will be need\nfor changes to take effect.')

    def write(self, tree, new_file):

        tree.write(new_file)

        self.response_message = 'SUCCESS', 'Instrument attributes saved, calling reinitialisation.'

        # self.exit_message()

        self.close()
