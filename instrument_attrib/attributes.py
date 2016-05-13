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
    def __init__(self, parent=None):
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

        # Timeout combobox setup
        self.timeouts = ['5','10','20', '30', '40', '50', '60']
        self.TimeoutCombobox.setToolTip('The default Staribus port timeout is 20 seconds')
        self.TimeoutCombobox.addItems(self.timeouts)

        # Baudrates
        self.baudrates = ['9600', '19200', '38400', '57600', '115200']

        # Staribus Address combobox tooltip
        self.comboBox.setToolTip('The instrument address, Starinet will always be 0 whereas Staribus can be\n'
                                 'between range 1 - 253\nWARNING: '
                                 'You will need to use Starbase to set the actual instrument address')

        # ColorDialog setup used for picking the channel colours.
        self.colorDialog = QtGui.QColorDialog()
        self.colorDialog.setOption(QtGui.QColorDialog.ShowAlphaChannel, False)
        self.colorDialog.setOption(QtGui.QColorDialog.DontUseNativeDialog, False)

        # self.buttonBox.accepted.connect(self.accept_called)
        self.buttonBox.rejected.connect(self.reject_called)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.accept_called)
        self.buttonBox.button(QtGui.QDialogButtonBox.RestoreDefaults).clicked.connect(self.defaults_called)

        # Setup picker triggers
        self.PickerButton0.clicked.connect(self.chan0_picker)
        self.PickerButton1.clicked.connect(self.chan1_picker)
        self.PickerButton2.clicked.connect(self.chan2_picker)
        self.PickerButton3.clicked.connect(self.chan3_picker)
        self.PickerButton4.clicked.connect(self.chan4_picker)
        self.PickerButton5.clicked.connect(self.chan5_picker)
        self.PickerButton6.clicked.connect(self.chan6_picker)
        self.PickerButton7.clicked.connect(self.chan7_picker)
        self.PickerButton8.clicked.connect(self.chan8_picker)

        # TODO Enabled state

        # State change triggers
        self.StaribusAutodetectCheckBox.stateChanged.connect(self.autodetect_checkbox)
        self.Staribus2StarinetCheckBox.stateChanged.connect(self.Staribus2Starinet_checkbox)

        self.home_path = None

        self.instrument = None

        self.instrument_file = None

        # Original Staribus Port

        self.StaribusPortOriginal = None

        # Original Staribus Baudrate

        self.StaribusBaudrateOriginal = None

        # Accept called state
        self.accept_called_state = False

        # Either Staribus or Starinet.
        self.instrument_type = 'staribus'

        self.original_channel_labels = []
        self.channel_labels = []

        self.original_channel_colours = []
        self.channel_colours = []

        self.response_message = 'ABORT', None
        self.reload = False

        # Starinet Address Signals
        self.StarinetAddressLineEdit.blockSignals(True)
        self.StarinetAddressLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.starinet_ip)))
        self.StarinetAddressLineEdit.textChanged.connect(self.parameter_check_state)
        self.StarinetAddressLineEdit.textChanged.emit(self.StarinetAddressLineEdit.text())

        # Starinet Port Signals
        self.StarinetPortLineEdit.blockSignals(True)
        self.StarinetPortLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.starinet_port)))
        self.StarinetPortLineEdit.textChanged.connect(self.parameter_check_state)
        self.StarinetPortLineEdit.textChanged.emit(self.StarinetPortLineEdit.text())

        # Staribus Port Signals
        self.StaribusPortLineEdit.blockSignals(True)
        self.StaribusPortLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.staribus_port)))
        self.StaribusPortLineEdit.textChanged.connect(self.parameter_check_state)
        self.StaribusPortLineEdit.textChanged.emit(self.StaribusPortLineEdit.text())

        # Channel Label and Channel Colour Signals

        self.Chan0LabelEdit.blockSignals(True)
        self.Chan0LabelEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.channel_name)))
        self.Chan0LabelEdit.textChanged.connect(self.parameter_check_state)
        self.Chan0LabelEdit.textChanged.emit(self.Chan0LabelEdit.text())

        self.Chan0ColourLineEdit.blockSignals(True)
        self.Chan0ColourLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.channel_hex_color)))
        self.Chan0ColourLineEdit.textChanged.connect(self.parameter_check_state)
        self.Chan0ColourLineEdit.textChanged.connect(self.Picker0)
        self.Chan0ColourLineEdit.textChanged.emit(self.Chan0ColourLineEdit.text())

        self.Chan1LabelEdit.blockSignals(True)
        self.Chan1LabelEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.channel_name)))
        self.Chan1LabelEdit.textChanged.connect(self.parameter_check_state)
        self.Chan1LabelEdit.textChanged.emit(self.Chan1LabelEdit.text())

        self.Chan1ColourLineEdit.blockSignals(True)
        self.Chan1ColourLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.channel_hex_color)))
        self.Chan1ColourLineEdit.textChanged.connect(self.parameter_check_state)
        self.Chan1ColourLineEdit.textChanged.connect(self.Picker1)
        self.Chan1ColourLineEdit.textChanged.emit(self.Chan1ColourLineEdit.text())

        self.Chan2LabelEdit.blockSignals(True)
        self.Chan2LabelEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.channel_name)))
        self.Chan2LabelEdit.textChanged.connect(self.parameter_check_state)
        self.Chan2LabelEdit.textChanged.emit(self.Chan2LabelEdit.text())

        self.Chan2ColourLineEdit.blockSignals(True)
        self.Chan2ColourLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.channel_hex_color)))
        self.Chan2ColourLineEdit.textChanged.connect(self.parameter_check_state)
        self.Chan2ColourLineEdit.textChanged.connect(self.Picker2)
        self.Chan2ColourLineEdit.textChanged.emit(self.Chan2ColourLineEdit.text())

        self.Chan3LabelEdit.blockSignals(True)
        self.Chan3LabelEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.channel_name)))
        self.Chan3LabelEdit.textChanged.connect(self.parameter_check_state)
        self.Chan3LabelEdit.textChanged.emit(self.Chan3LabelEdit.text())

        self.Chan3ColourLineEdit.blockSignals(True)
        self.Chan3ColourLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.channel_hex_color)))
        self.Chan3ColourLineEdit.textChanged.connect(self.parameter_check_state)
        self.Chan3ColourLineEdit.textChanged.connect(self.Picker3)
        self.Chan3ColourLineEdit.textChanged.emit(self.Chan3ColourLineEdit.text())

        self.Chan4LabelEdit.blockSignals(True)
        self.Chan4LabelEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.channel_name)))
        self.Chan4LabelEdit.textChanged.connect(self.parameter_check_state)
        self.Chan4LabelEdit.textChanged.emit(self.Chan4LabelEdit.text())

        self.Chan4ColourLineEdit.blockSignals(True)
        self.Chan4ColourLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.channel_hex_color)))
        self.Chan4ColourLineEdit.textChanged.connect(self.parameter_check_state)
        self.Chan4ColourLineEdit.textChanged.connect(self.Picker4)
        self.Chan4ColourLineEdit.textChanged.emit(self.Chan4ColourLineEdit.text())

        self.Chan5LabelEdit.blockSignals(True)
        self.Chan5LabelEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.channel_name)))
        self.Chan5LabelEdit.textChanged.connect(self.parameter_check_state)
        self.Chan5LabelEdit.textChanged.emit(self.Chan5LabelEdit.text())

        self.Chan5ColourLineEdit.blockSignals(True)
        self.Chan5ColourLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.channel_hex_color)))
        self.Chan5ColourLineEdit.textChanged.connect(self.parameter_check_state)
        self.Chan5ColourLineEdit.textChanged.connect(self.Picker5)
        self.Chan5ColourLineEdit.textChanged.emit(self.Chan5ColourLineEdit.text())

        self.Chan6LabelEdit.blockSignals(True)
        self.Chan6LabelEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.channel_name)))
        self.Chan6LabelEdit.textChanged.connect(self.parameter_check_state)
        self.Chan6LabelEdit.textChanged.emit(self.Chan6LabelEdit.text())

        self.Chan6ColourLineEdit.blockSignals(True)
        self.Chan6ColourLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.channel_hex_color)))
        self.Chan6ColourLineEdit.textChanged.connect(self.parameter_check_state)
        self.Chan6ColourLineEdit.textChanged.connect(self.Picker6)
        self.Chan6ColourLineEdit.textChanged.emit(self.Chan6ColourLineEdit.text())

        self.Chan7LabelEdit.blockSignals(True)
        self.Chan7LabelEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.channel_name)))
        self.Chan7LabelEdit.textChanged.connect(self.parameter_check_state)
        self.Chan7LabelEdit.textChanged.emit(self.Chan7LabelEdit.text())

        self.Chan7ColourLineEdit.blockSignals(True)
        self.Chan7ColourLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.channel_hex_color)))
        self.Chan7ColourLineEdit.textChanged.connect(self.parameter_check_state)
        self.Chan7ColourLineEdit.textChanged.connect(self.Picker7)
        self.Chan7ColourLineEdit.textChanged.emit(self.Chan7ColourLineEdit.text())

        self.Chan8LabelEdit.blockSignals(True)
        self.Chan8LabelEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.channel_name)))
        self.Chan8LabelEdit.textChanged.connect(self.parameter_check_state)
        self.Chan8LabelEdit.textChanged.emit(self.Chan8LabelEdit.text())

        self.Chan8ColourLineEdit.blockSignals(True)
        self.Chan8ColourLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.channel_hex_color)))
        self.Chan8ColourLineEdit.textChanged.connect(self.parameter_check_state)
        self.Chan8ColourLineEdit.textChanged.connect(self.Picker8)
        self.Chan8ColourLineEdit.textChanged.emit(self.Chan8ColourLineEdit.text())

    def reset_dialog(self):

        self.home_path = None

        self.instrument = None
        self.instrument_file = None

        # Accept called state
        self.accept_called_state = False

        # Either Staribus or Starinet.
        self.instrument_type = 'staribus'

        self.original_channel_labels.clear()
        self.channel_labels.clear()

        self.original_channel_colours.clear()
        self.channel_colours.clear()

        self.response_message = 'ABORT', None

        self.reload = False

        # StaribusPort Line Edit

        self.StaribusPortLineEdit.blockSignals(True)
        self.StaribusPortLineEdit.clear()
        self.StaribusPortLineEdit.setEnabled(False)
        self.StaribusPortLineEdit.setStyleSheet('QLineEdit { background-color: }')

        # RS485 Checkbox

        self.RS485checkBox.blockSignals(True)
        self.RS485checkBox.setChecked(False)
        self.RS485checkBox.setEnabled(False)

        # Staribus Auto Detect Checkbox

        self.StaribusAutodetectCheckBox.blockSignals(True)
        self.StaribusAutodetectCheckBox.setChecked(False)
        self.StaribusAutodetectCheckBox.setEnabled(False)

        # Staribus 2 Starinet Checkbox

        self.Staribus2StarinetCheckBox.blockSignals(True)
        self.Staribus2StarinetCheckBox.setChecked(False)
        self.Staribus2StarinetCheckBox.setEnabled(False)

        # Staribus Address Combobox

        self.comboBox.blockSignals(True)
        self.comboBox.clear()
        self.comboBox.setEnabled(False)

        # Staribus Baudrate Combobox

        self.BaudrateCombobox.blockSignals(True)
        self.BaudrateCombobox.clear()
        self.BaudrateCombobox.setEnabled(False)

        # Starinet IP Line Edit

        self.StarinetAddressLineEdit.blockSignals(True)
        self.StarinetAddressLineEdit.clear()
        self.StarinetAddressLineEdit.setEnabled(False)
        self.StarinetAddressLineEdit.setStyleSheet('QLineEdit { background-color: }')

        # Starinet Port Line Edit

        self.StarinetPortLineEdit.blockSignals(True)
        self.StarinetPortLineEdit.clear()
        self.StarinetPortLineEdit.setEnabled(False)
        self.StarinetPortLineEdit.setStyleSheet('QLineEdit { background-color: }')

        # Disable all the channel labels and buttons as we enable them when we load the instrument XML

        # Channel 0

        self.Chan0LabelEdit.blockSignals(True)
        self.Chan0ColourLineEdit.blockSignals(True)

        self.Chan0LabelEdit.setEnabled(False)
        self.Chan0LabelEdit.clear()
        self.Chan0LabelEdit.setStyleSheet('QLineEdit { background-color: }')

        self.Chan0ColourLineEdit.setEnabled(False)
        self.Chan0ColourLineEdit.clear()
        self.Chan0ColourLineEdit.setStyleSheet('QLineEdit { background-color: }')

        self.PickerButton0.setEnabled(False)
        self.PickerButton0.setStyleSheet('QPushButton { background-color: }')

        # Channel 1

        self.Chan1LabelEdit.blockSignals(True)
        self.Chan1ColourLineEdit.blockSignals(True)

        self.Chan1LabelEdit.setEnabled(False)
        self.Chan1LabelEdit.clear()
        self.Chan1LabelEdit.setStyleSheet('QLineEdit { background-color: }')

        self.Chan1ColourLineEdit.setEnabled(False)
        self.Chan1ColourLineEdit.clear()
        self.Chan1ColourLineEdit.setStyleSheet('QLineEdit { background-color: }')

        self.PickerButton1.setEnabled(False)
        self.PickerButton1.setStyleSheet('QPushButton { background-color: }')

        # Channel 2

        self.Chan2LabelEdit.blockSignals(True)
        self.Chan2ColourLineEdit.blockSignals(True)

        self.Chan2LabelEdit.setEnabled(False)
        self.Chan2LabelEdit.clear()
        self.Chan2LabelEdit.setStyleSheet('QLineEdit { background-color: }')

        self.Chan2ColourLineEdit.setEnabled(False)
        self.Chan2ColourLineEdit.clear()
        self.Chan2ColourLineEdit.setStyleSheet('QLineEdit { background-color: }')

        self.PickerButton2.setEnabled(False)
        self.PickerButton2.setStyleSheet('QPushButton { background-color: }')

        # Channel 3

        self.Chan3LabelEdit.blockSignals(True)
        self.Chan3ColourLineEdit.blockSignals(True)

        self.Chan3LabelEdit.setEnabled(False)
        self.Chan3LabelEdit.clear()
        self.Chan3LabelEdit.setStyleSheet('QLineEdit { background-color: }')

        self.Chan3ColourLineEdit.setEnabled(False)
        self.Chan3ColourLineEdit.clear()
        self.Chan3ColourLineEdit.setStyleSheet('QLineEdit { background-color: }')

        self.PickerButton3.setEnabled(False)
        self.PickerButton3.setStyleSheet('QPushButton { background-color: }')

        # Channel 4

        self.Chan4LabelEdit.blockSignals(True)
        self.Chan4ColourLineEdit.blockSignals(True)

        self.Chan4LabelEdit.setEnabled(False)
        self.Chan4LabelEdit.clear()
        self.Chan4LabelEdit.setStyleSheet('QLineEdit { background-color: }')

        self.Chan4ColourLineEdit.setEnabled(False)
        self.Chan4ColourLineEdit.clear()
        self.Chan4ColourLineEdit.setStyleSheet('QLineEdit { background-color: }')

        self.PickerButton4.setEnabled(False)
        self.PickerButton4.setStyleSheet('QPushButton { background-color: }')

        # Channel 5

        self.Chan5LabelEdit.blockSignals(True)
        self.Chan5ColourLineEdit.blockSignals(True)

        self.Chan5LabelEdit.setEnabled(False)
        self.Chan5LabelEdit.clear()
        self.Chan5LabelEdit.setStyleSheet('QLineEdit { background-color: }')

        self.Chan5ColourLineEdit.setEnabled(False)
        self.Chan5ColourLineEdit.clear()
        self.Chan5ColourLineEdit.setStyleSheet('QLineEdit { background-color: }')

        self.PickerButton5.setEnabled(False)
        self.PickerButton5.setStyleSheet('QPushButton { background-color: }')

        # Channel 6

        self.Chan6LabelEdit.blockSignals(True)
        self.Chan6ColourLineEdit.blockSignals(True)

        self.Chan6LabelEdit.setEnabled(False)
        self.Chan6LabelEdit.clear()
        self.Chan6LabelEdit.setStyleSheet('QLineEdit { background-color: }')

        self.Chan6ColourLineEdit.setEnabled(False)
        self.Chan6ColourLineEdit.clear()
        self.Chan6ColourLineEdit.setStyleSheet('QLineEdit { background-color: }')

        self.PickerButton6.setEnabled(False)
        self.PickerButton6.setStyleSheet('QPushButton { background-color: }')

        # Channel 7

        self.Chan7LabelEdit.blockSignals(True)
        self.Chan7ColourLineEdit.blockSignals(True)

        self.Chan7LabelEdit.setEnabled(False)
        self.Chan7LabelEdit.clear()
        self.Chan7LabelEdit.setStyleSheet('QLineEdit { background-color: }')

        self.Chan7ColourLineEdit.setEnabled(False)
        self.Chan7ColourLineEdit.clear()
        self.Chan7ColourLineEdit.setStyleSheet('QLineEdit { background-color: }')

        self.PickerButton7.setEnabled(False)
        self.PickerButton7.setStyleSheet('QPushButton { background-color: }')

        # Channel 8

        self.Chan8LabelEdit.blockSignals(True)
        self.Chan8ColourLineEdit.blockSignals(True)

        self.Chan8LabelEdit.setEnabled(False)
        self.Chan8LabelEdit.clear()
        self.Chan8LabelEdit.setStyleSheet('QLineEdit { background-color: }')

        self.Chan8ColourLineEdit.setEnabled(False)
        self.Chan8ColourLineEdit.clear()
        self.Chan8ColourLineEdit.setStyleSheet('QLineEdit { background-color: }')

        self.PickerButton8.setEnabled(False)
        self.PickerButton8.setStyleSheet('QPushButton { background-color: }')

    # This gets run first so we can populate the UI and set the original configuration state.

    def set(self, instrument, instrument_file, user_home):

        # Set user home location
        self.home_path = user_home + 'instruments' + os.path.sep

        # Either Staribus or Starinet.
        self.instrument_type = 'staribus'

        self.instrument = instrument
        self.instrument_file = instrument_file

        # Create both channel label and colour list, one to change and one to check against.

        self.original_channel_colours.clear()
        self.channel_colours.clear()
        self.original_channel_labels.clear()
        self.channel_labels.clear()

        for labels in self.instrument.channel_names:
            self.original_channel_labels.append(labels)
            self.channel_labels.append(labels)

        for colours in self.instrument.channel_colours:
            self.original_channel_colours.append(colours)
            self.channel_colours.append(colours)

        # See if we have a Staribus or Starinet instrument and setup the instrument specific attributes.

        if self.instrument.instrument_staribus_address == '000':

            self.instrument_type = 'starinet'

            # Fill the contents of the UI and setup triggers #

            # Staribus Address will be zero as Starinet
            self.comboBox.addItem('0')
            self.comboBox.setCurrentIndex(0)

            # Starinet Address
            self.StarinetAddressLineEdit.blockSignals(False)
            self.StarinetAddressLineEdit.setEnabled(True)
            self.StarinetAddressLineEdit.setText(self.instrument.instrument_starinet_address)

            # Starinet Address tooltips
            self.StarinetAddressLineEdit.setToolTip('Any valid IPv4 address')

            # Starinet Port
            self.StarinetPortLineEdit.blockSignals(False)
            self.StarinetPortLineEdit.setEnabled(True)
            self.StarinetPortLineEdit.setText(self.instrument.instrument_starinet_port)

            # Starinet Port tooltips
            self.StarinetPortLineEdit.setToolTip('Must be in range 1 - 65535')

        else:

            self.instrument_type = 'staribus'

            # Staribus type in development so checkbox disabled.

            ################################
            # self.RS485checkBox.setEnabled(False)

            # Fill the contents of the UI and setup triggers #

            # Staribus Port
            self.StaribusPortLineEdit.setEnabled(True)

            self.StaribusPortLineEdit.blockSignals(False)

            self.StaribusPortLineEdit.setText(self.instrument.instrument_staribus_port)

            ##################################
            # Serial interface type
            # if self.instrument.instrument_staribus_type == 'RS232':
            #
            #     self.RS485checkBox.setChecked(False)
            #
            # else:
            #
            #     self.RS485checkBox.setChecked(True)

            # Staribus port autodetect

            self.StaribusAutodetectCheckBox.blockSignals(False)

            self.StaribusAutodetectCheckBox.setEnabled(True)

            if self.instrument.instrument_staribus_autodetect == 'False':

                self.StaribusAutodetectCheckBox.setChecked(False)

            elif self.instrument.instrument_staribus_autodetect == 'True':

                self.StaribusAutodetectCheckBox.setChecked(True)

                self.StaribusPortLineEdit.clear()

                self.StaribusPortLineEdit.setStyleSheet('QLineEdit { background-color: }')

                self.StaribusPortLineEdit.setEnabled(False)  # Disable port entry box if auto detect is true.

            # Staribus baudrate

            self.BaudrateCombobox.addItems(self.baudrates)

            self.BaudrateCombobox.setEnabled(True)

            self.BaudrateCombobox.setCurrentIndex(
                self.baudrates.index(self.instrument.instrument_staribus_baudrate))

            # Staribus2Starinet interface setup

            self.Staribus2StarinetCheckBox.setEnabled(True)

            self.Staribus2StarinetCheckBox.blockSignals(False)

            if self.instrument.instrument_staribus2starinet == 'True':

                self.Staribus2StarinetCheckBox.setEnabled(True)

                self.Staribus2StarinetCheckBox.setChecked(True)

                # Disable StaribusPort

                self.StaribusPortLineEdit.blockSignals(True)
                self.StaribusPortLineEdit.setEnabled(False)
                self.StaribusPortLineEdit.setStyleSheet('QLineEdit { background-color: }')

                # Autodetect

                self.StaribusAutodetectCheckBox.setEnabled(False)

                # Baudrate combobox

                self.BaudrateCombobox.setEnabled(False)

                # Starinet Address

                self.StarinetAddressLineEdit.blockSignals(False)

                self.StarinetAddressLineEdit.setEnabled(True)

                self.StarinetAddressLineEdit.setText(self.instrument.instrument_starinet_address)

                # Starinet Port

                self.StarinetPortLineEdit.blockSignals(False)

                self.StarinetPortLineEdit.setEnabled(True)

                self.StarinetPortLineEdit.setText(self.instrument.instrument_starinet_port)

            # TODO we need to change below so we can't select address 0 when Staribus Instrument is selected.

            # Staribus address, comboBox is the Staribus Address.
            for i in range(1, 253):
                self.comboBox.addItem(str(i))

            self.comboBox.setEnabled(True)

            # Here we take one away from the set staribus address to get the correct combobox index as the Staribus,
            # address range runs from one to two hundred and fifty three not from zero.

            self.comboBox.setCurrentIndex(int(self.instrument.instrument_staribus_address) - 1)

            # Staribus tooltips.

            if sys.platform.startswith('win32'):

                self.StaribusPortLineEdit.setToolTip('The com port to which the instrument is attached, such as COM1')

            else:

                self.StaribusPortLineEdit.setToolTip('The full path and serial port name the instrument is attached to.')

            # self.RS485checkBox.setToolTip('The type of interface being used RS232 or RS485')
            self.RS485checkBox.setToolTip('Not currently available under development.')

            self.StaribusAutodetectCheckBox.setToolTip(
                'Will check each attached serial port for the configured instrument'
                '\nNote : The configured instrument must be attached.')

            self.BaudrateCombobox.setToolTip('The default baudrate is normally 57600')

        # Set the value of the Staribus timeouts combobox

        self.TimeoutCombobox.setCurrentIndex(self.timeouts.index(self.instrument.instrument_staribus_timeout))

        # Setup the channel labels and colour boxes

        self.enable_channel_items()

    # This sets the state of the StaribusLineEdit box dependng on the autodetect checkbox state.

    def autodetect_checkbox(self):

        if self.StaribusAutodetectCheckBox.isChecked():

            self.StaribusPortLineEdit.setStyleSheet('QLineEdit { background-color: }')

            self.StaribusPortLineEdit.setEnabled(False)

        else:

            self.StaribusPortLineEdit.setEnabled(True)

            self.StaribusPortLineEdit.clear()

            self.StaribusPortLineEdit.setText(self.instrument.instrument_staribus_port)

        self.configuration_check()

    # This set the state of of StarinetLineEdit and StarinetPortLineEdits depends on checkbox condition.

    def Staribus2Starinet_checkbox(self):


        if self.Staribus2StarinetCheckBox.isChecked():

            self.StaribusPortLineEdit.blockSignals(True)
            self.StaribusPortLineEdit.setEnabled(False)
            self.StaribusPortLineEdit.setStyleSheet('QLineEdit { background-color: }')

            self.BaudrateCombobox.setEnabled(False)

            self.StarinetAddressLineEdit.blockSignals(False)
            self.StarinetAddressLineEdit.setEnabled(True)

            if self.instrument.instrument_starinet_address == 'None':

                self.StarinetAddressLineEdit.setText('0')
                self.StarinetAddressLineEdit.clear()

            else:

                self.StarinetAddressLineEdit.clear()
                self.StarinetAddressLineEdit.setText(self.instrument.instrument_starinet_address)

            self.StarinetPortLineEdit.blockSignals(False)
            self.StarinetPortLineEdit.setEnabled(True)

            if self.instrument.instrument_starinet_port == 'None':

                self.StarinetPortLineEdit.setText('0')
                self.StarinetPortLineEdit.clear()
                self.StarinetPortLineEdit.setText('1205')

            else:

                self.StarinetPortLineEdit.clear()
                self.StarinetPortLineEdit.setText(self.instrument.instrument_starinet_port)

        else:
            self.StaribusPortLineEdit.blockSignals(False)
            self.StaribusPortLineEdit.setEnabled(True)
            self.StaribusPortLineEdit.clear()
            self.StaribusPortLineEdit.setText(self.instrument.instrument_staribus_port)

            self.BaudrateCombobox.setEnabled(True)

            self.StarinetAddressLineEdit.blockSignals(True)
            self.StarinetAddressLineEdit.setEnabled(False)
            self.StarinetAddressLineEdit.clear()
            self.StarinetAddressLineEdit.setStyleSheet('QLineEdit { background-color: }')

            self.StarinetPortLineEdit.blockSignals(True)
            self.StarinetPortLineEdit.setEnabled(False)
            self.StarinetPortLineEdit.clear()
            self.StarinetPortLineEdit.setStyleSheet('QLineEdit { background-color: }')

    def configuration_changed(self):

        # TODO this still trips when it shouldn't.

        # Check to see if the channel colours have changed.
        result = [i for i, j in zip(self.channel_colours, self.original_channel_colours) if i == j]

        if len(result) != int(self.instrument.instrument_number_of_channels):
            return False

        # Check to see if the channel labels have changed.
        result = [i for i, j in zip(self.channel_labels, self.original_channel_labels) if i == j]

        if len(result) != int(self.instrument.instrument_number_of_channels):
            return False

        # Check to see if the staribus address has changed.
        if self.instrument.instrument_staribus_address != 'None':
            if self.comboBox.currentText().zfill(3) != self.instrument.instrument_staribus_address:
                return False

        # Check to see if the staribus port has changed.
        if self.instrument.instrument_staribus_port != 'None':
            if self.StaribusPortLineEdit.text() != self.instrument.instrument_staribus_port:
                return False

        # Check to see if the staribus autodetect has changed.
        if self.instrument.instrument_staribus_autodetect != 'None':
            if self.StaribusAutodetectCheckBox.isChecked():
                autodetect = 'True'
            else:
                autodetect = 'False'

            if autodetect != self.instrument.instrument_staribus_autodetect:
                return False

        # Check to see if staribus to Starinet has changed.
        if self.instrument.instrument_staribus2starinet != 'None':
            if self.StaribusAutodetectCheckBox.isChecked():
                staribus2starinet = 'True'
            else:
                staribus2starinet = 'False'

            if staribus2starinet != self.instrument.instrument_staribus2starinet:
                return False

        # if self.instrument.instrument_staribus_type != 'None':
        #     self.original_staribus_type = self.instrument.instrument_staribus_type

        # Check to see if the staribus baudrate has changed.
        if self.instrument.instrument_staribus_baudrate != 'None':
            if self.BaudrateCombobox.currentText() != self.instrument.instrument_staribus_baudrate:
                return False

        # Check to see if the staribus timeout has changed.
        if self.instrument.instrument_staribus_timeout != 'None':
            if self.TimeoutCombobox.currentText() != self.instrument.instrument_staribus_timeout:
                return False

        # Check to see if the starinet address has changed.
        if self.instrument.instrument_starinet_address != 'None':
            if self.StarinetAddressLineEdit.text() != self.instrument.instrument_starinet_address:
                return False

        # Check to see if the starinet port has changed.
        if self.instrument.instrument_starinet_port != 'None':
            if self.StarinetPortLineEdit.text() != self.instrument.instrument_starinet_port:
                return False

        return True

    def configuration_check(self):

        trip = 5

        # Check to see if the channel colours are valid.
        for channel_colour in self.channel_colours:
            if not re.match(constants.channel_hex_color, channel_colour):
                trip -= 1

        # Check to see if the channel labels are valid.
        for channel_label in self.channel_labels:
            if not re.match(constants.channel_name, channel_label) or len(channel_label) == 0:
                trip -= 1

        # Check to see if the staribus port are valid.
        if self.instrument.instrument_staribus_port != 'None':
            if not re.match(constants.staribus_port, self.StaribusPortLineEdit.text()):
                trip -= 1

        # Check to see if the starinet address are valid.
        if self.instrument.instrument_starinet_address != 'None':
            if not re.match(constants.starinet_ip, self.StarinetAddressLineEdit.text()):
                trip -= 1

        # Check to see if the starinet port are valid.
        if self.instrument.instrument_starinet_port != 'None':
            if not re.match(constants.starinet_port, self.StarinetPortLineEdit.text()):
                trip -= 1

        # Check to see if Staribus2Starinet makes sense.
        if self.Staribus2StarinetCheckBox.isChecked():
            if not re.match(constants.starinet_ip, self.StarinetAddressLineEdit.text()) or not \
                    re.match(constants.starinet_port, self.StarinetPortLineEdit.text()):

                trip -=1

        if trip == 5:

            return True

        else:

            return False

    # Run the configuration check routine and depending on response set OK button setEnabled true or false.
    def save_button_state(self):

        if self.configuration_check():
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)

    # Set the colour picker chooser buttons so they're the colour the channel line is set to.
    def Picker0(self):
        if re.match(constants.channel_hex_color, self.Chan0ColourLineEdit.text()):
            self.channel_colours[0] = self.Chan0ColourLineEdit.text()
            self.PickerButton0.setStyleSheet(
                'QPushButton { background-color: ' + self.Chan0ColourLineEdit.text() + ';' +
                'border-width: 1px; border-radius: 3px;' +
                'border-color: beige; padding: 5px;' +
                'margin-top: 0px; }')
            self.save_button_state()

    def Picker1(self):
        if re.match(constants.channel_hex_color, self.Chan1ColourLineEdit.text()):
            self.channel_colours[1] = self.Chan1ColourLineEdit.text()
            self.PickerButton1.setStyleSheet(
                'QPushButton { background-color: ' + self.Chan1ColourLineEdit.text() + ';' +
                'border-width: 1px; border-radius: 3px;' +
                'border-color: beige; padding: 5px;' +
                'margin-top: 0px; }')
            self.save_button_state()

    def Picker2(self):
        if re.match(constants.channel_hex_color, self.Chan2ColourLineEdit.text()):
            self.channel_colours[2] = self.Chan2ColourLineEdit.text()
            self.PickerButton2.setStyleSheet(
                'QPushButton { background-color: ' + self.Chan2ColourLineEdit.text() + ';' +
                'border-width: 1px; border-radius: 3px;' +
                'border-color: beige; padding: 5px;' +
                'margin-top: 0px; }')
            self.save_button_state()

    def Picker3(self):
        if re.match(constants.channel_hex_color, self.Chan3ColourLineEdit.text()):
            self.channel_colours[3] = self.Chan3ColourLineEdit.text()
            self.PickerButton3.setStyleSheet(
                'QPushButton { background-color: ' + self.Chan3ColourLineEdit.text() + ';' +
                'border-width: 1px; border-radius: 3px;' +
                'border-color: beige; padding: 5px;' +
                'margin-top: 0px; }')
            self.save_button_state()

    def Picker4(self):
        if re.match(constants.channel_hex_color, self.Chan4ColourLineEdit.text()):
            self.channel_colours[4] = self.Chan4ColourLineEdit.text()
            self.PickerButton4.setStyleSheet(
                'QPushButton { background-color: ' + self.Chan4ColourLineEdit.text() + ';' +
                'border-width: 1px; border-radius: 3px;' +
                'border-color: beige; padding: 5px;' +
                'margin-top: 0px; }')
            self.save_button_state()

    def Picker5(self):
        if re.match(constants.channel_hex_color, self.Chan5ColourLineEdit.text()):
            self.channel_colours[5] = self.Chan5ColourLineEdit.text()
            self.PickerButton5.setStyleSheet(
                'QPushButton { background-color: ' + self.Chan5ColourLineEdit.text() + ';' +
                'border-width: 1px; border-radius: 3px;' +
                'border-color: beige; padding: 5px;' +
                'margin-top: 0px; }')
            self.save_button_state()

    def Picker6(self):
        if re.match(constants.channel_hex_color, self.Chan6ColourLineEdit.text()):
            self.channel_colours[6] = self.Chan6ColourLineEdit.text()
            self.PickerButton6.setStyleSheet(
                'QPushButton { background-color: ' + self.Chan6ColourLineEdit.text() + ';' +
                'border-width: 1px; border-radius: 3px;' +
                'border-color: beige; padding: 5px;' +
                'margin-top: 0px; }')
            self.save_button_state()

    def Picker7(self):
        if re.match(constants.channel_hex_color, self.Chan7ColourLineEdit.text()):
            self.channel_colours[7] = self.Chan7ColourLineEdit.text()
            self.PickerButton7.setStyleSheet(
                'QPushButton { background-color: ' + self.Chan7ColourLineEdit.text() + ';' +
                'border-width: 1px; border-radius: 3px;' +
                'border-color: beige; padding: 5px;' +
                'margin-top: 0px; }')
            self.save_button_state()

    def Picker8(self):
        if re.match(constants.channel_hex_color, self.Chan8ColourLineEdit.text()):
            self.channel_colours[8] = self.Chan8ColourLineEdit.text()
            self.PickerButton8.setStyleSheet(
                'QPushButton { background-color: ' + self.Chan8ColourLineEdit.text() + ';' +
                'border-width: 1px; border-radius: 3px;' +
                'border-color: beige; padding: 5px;' +
                'margin-top: 0px; }')
            self.save_button_state()

    # channel pickers.
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

    # Set the current channel labels in the channel_labels list

    def channel_lists(self):

        if self.instrument.instrument_number_of_channels == '2':

            self.channel_labels[0] = self.Chan0LabelEdit.text()
            self.channel_labels[1] = self.Chan1LabelEdit.text()

            self.channel_colours[0] = self.Chan0ColourLineEdit.text()
            self.channel_colours[1] = self.Chan1ColourLineEdit.text()

        elif self.instrument.instrument_number_of_channels == '3':

            self.channel_labels[0] = self.Chan0LabelEdit.text()
            self.channel_labels[1] = self.Chan1LabelEdit.text()
            self.channel_labels[2] = self.Chan2LabelEdit.text()

            self.channel_colours[0] = self.Chan0ColourLineEdit.text()
            self.channel_colours[1] = self.Chan1ColourLineEdit.text()
            self.channel_colours[2] = self.Chan2ColourLineEdit.text()

        elif self.instrument.instrument_number_of_channels == '4':

            self.channel_labels[0] = self.Chan0LabelEdit.text()
            self.channel_labels[1] = self.Chan1LabelEdit.text()
            self.channel_labels[2] = self.Chan2LabelEdit.text()
            self.channel_labels[3] = self.Chan3LabelEdit.text()

            self.channel_colours[0] = self.Chan0ColourLineEdit.text()
            self.channel_colours[1] = self.Chan1ColourLineEdit.text()
            self.channel_colours[2] = self.Chan2ColourLineEdit.text()
            self.channel_colours[3] = self.Chan3ColourLineEdit.text()

        elif self.instrument.instrument_number_of_channels == '5':

            self.channel_labels[0] = self.Chan0LabelEdit.text()
            self.channel_labels[1] = self.Chan1LabelEdit.text()
            self.channel_labels[2] = self.Chan2LabelEdit.text()
            self.channel_labels[3] = self.Chan3LabelEdit.text()
            self.channel_labels[4] = self.Chan4LabelEdit.text()

            self.channel_colours[0] = self.Chan0ColourLineEdit.text()
            self.channel_colours[1] = self.Chan1ColourLineEdit.text()
            self.channel_colours[2] = self.Chan2ColourLineEdit.text()
            self.channel_colours[3] = self.Chan3ColourLineEdit.text()
            self.channel_colours[4] = self.Chan4ColourLineEdit.text()

        elif self.instrument.instrument_number_of_channels == '6':

            self.channel_labels[0] = self.Chan0LabelEdit.text()
            self.channel_labels[1] = self.Chan1LabelEdit.text()
            self.channel_labels[2] = self.Chan2LabelEdit.text()
            self.channel_labels[3] = self.Chan3LabelEdit.text()
            self.channel_labels[4] = self.Chan4LabelEdit.text()
            self.channel_labels[5] = self.Chan5LabelEdit.text()

            self.channel_colours[0] = self.Chan0ColourLineEdit.text()
            self.channel_colours[1] = self.Chan1ColourLineEdit.text()
            self.channel_colours[2] = self.Chan2ColourLineEdit.text()
            self.channel_colours[3] = self.Chan3ColourLineEdit.text()
            self.channel_colours[4] = self.Chan4ColourLineEdit.text()
            self.channel_colours[5] = self.Chan5ColourLineEdit.text()

        elif self.instrument.instrument_number_of_channels == '7':

            self.channel_labels[0] = self.Chan0LabelEdit.text()
            self.channel_labels[1] = self.Chan1LabelEdit.text()
            self.channel_labels[2] = self.Chan2LabelEdit.text()
            self.channel_labels[3] = self.Chan3LabelEdit.text()
            self.channel_labels[4] = self.Chan4LabelEdit.text()
            self.channel_labels[5] = self.Chan5LabelEdit.text()
            self.channel_labels[6] = self.Chan6LabelEdit.text()

            self.channel_colours[0] = self.Chan0ColourLineEdit.text()
            self.channel_colours[1] = self.Chan1ColourLineEdit.text()
            self.channel_colours[2] = self.Chan2ColourLineEdit.text()
            self.channel_colours[3] = self.Chan3ColourLineEdit.text()
            self.channel_colours[4] = self.Chan4ColourLineEdit.text()
            self.channel_colours[5] = self.Chan5ColourLineEdit.text()
            self.channel_colours[6] = self.Chan6ColourLineEdit.text()

        elif self.instrument.instrument_number_of_channels == '8':

            self.channel_labels[0] = self.Chan0LabelEdit.text()
            self.channel_labels[1] = self.Chan1LabelEdit.text()
            self.channel_labels[2] = self.Chan2LabelEdit.text()
            self.channel_labels[3] = self.Chan3LabelEdit.text()
            self.channel_labels[4] = self.Chan4LabelEdit.text()
            self.channel_labels[5] = self.Chan5LabelEdit.text()
            self.channel_labels[6] = self.Chan6LabelEdit.text()
            self.channel_labels[7] = self.Chan7LabelEdit.text()

            self.channel_colours[0] = self.Chan0ColourLineEdit.text()
            self.channel_colours[1] = self.Chan1ColourLineEdit.text()
            self.channel_colours[2] = self.Chan2ColourLineEdit.text()
            self.channel_colours[3] = self.Chan3ColourLineEdit.text()
            self.channel_colours[4] = self.Chan4ColourLineEdit.text()
            self.channel_colours[5] = self.Chan5ColourLineEdit.text()
            self.channel_colours[6] = self.Chan6ColourLineEdit.text()
            self.channel_colours[7] = self.Chan7ColourLineEdit.text()

        elif self.instrument.instrument_number_of_channels == '9':

            self.channel_labels[0] = self.Chan0LabelEdit.text()
            self.channel_labels[1] = self.Chan1LabelEdit.text()
            self.channel_labels[2] = self.Chan2LabelEdit.text()
            self.channel_labels[3] = self.Chan3LabelEdit.text()
            self.channel_labels[4] = self.Chan4LabelEdit.text()
            self.channel_labels[5] = self.Chan5LabelEdit.text()
            self.channel_labels[6] = self.Chan6LabelEdit.text()
            self.channel_labels[7] = self.Chan7LabelEdit.text()
            self.channel_labels[8] = self.Chan8LabelEdit.text()

            self.channel_colours[0] = self.Chan0ColourLineEdit.text()
            self.channel_colours[1] = self.Chan1ColourLineEdit.text()
            self.channel_colours[2] = self.Chan2ColourLineEdit.text()
            self.channel_colours[3] = self.Chan3ColourLineEdit.text()
            self.channel_colours[4] = self.Chan4ColourLineEdit.text()
            self.channel_colours[5] = self.Chan5ColourLineEdit.text()
            self.channel_colours[6] = self.Chan6ColourLineEdit.text()
            self.channel_colours[7] = self.Chan7ColourLineEdit.text()
            self.channel_colours[8] = self.Chan8ColourLineEdit.text()

    # The channel entry sections setup routines.

    def channel0(self):

        self.Chan0LabelEdit.setEnabled(True)

        self.Chan0LabelEdit.blockSignals(False)

        self.Chan0LabelEdit.setText(self.instrument.channel_names[0])

        self.PickerButton0.setEnabled(True)

        self.Chan0ColourLineEdit.setEnabled(True)

        self.Chan0ColourLineEdit.blockSignals(False)

        self.Chan0ColourLineEdit.setText(self.instrument.channel_colours[0])

    def channel1(self):

        self.Chan1LabelEdit.setEnabled(True)

        self.Chan1LabelEdit.blockSignals(False)

        self.Chan1LabelEdit.setText(self.instrument.channel_names[1])

        self.PickerButton1.setEnabled(True)

        self.Chan1ColourLineEdit.setEnabled(True)

        self.Chan1ColourLineEdit.blockSignals(False)

        self.Chan1ColourLineEdit.setText(self.instrument.channel_colours[1])

    def channel2(self):

        self.Chan2LabelEdit.setEnabled(True)

        self.Chan2LabelEdit.blockSignals(False)

        self.Chan2LabelEdit.setText(self.instrument.channel_names[2])

        self.PickerButton2.setEnabled(True)

        self.Chan2ColourLineEdit.setEnabled(True)

        self.Chan2ColourLineEdit.blockSignals(False)

        self.Chan2ColourLineEdit.setText(self.instrument.channel_colours[2])

    def channel3(self):

        self.Chan3LabelEdit.setEnabled(True)

        self.Chan3LabelEdit.blockSignals(False)

        self.Chan3LabelEdit.setText(self.instrument.channel_names[3])

        self.PickerButton3.setEnabled(True)

        self.Chan3ColourLineEdit.setEnabled(True)

        self.Chan3ColourLineEdit.blockSignals(False)

        self.Chan3ColourLineEdit.setText(self.instrument.channel_colours[3])

    def channel4(self):

        self.Chan4LabelEdit.setEnabled(True)

        self.Chan4LabelEdit.blockSignals(False)

        self.Chan4LabelEdit.setText(self.instrument.channel_names[4])

        self.PickerButton4.setEnabled(True)

        self.Chan4ColourLineEdit.setEnabled(True)

        self.Chan4ColourLineEdit.blockSignals(False)

        self.Chan4ColourLineEdit.setText(self.instrument.channel_colours[4])

    def channel5(self):

        self.Chan5LabelEdit.setEnabled(True)

        self.Chan5LabelEdit.blockSignals(False)

        self.Chan5LabelEdit.setText(self.instrument.channel_names[5])

        self.PickerButton5.setEnabled(True)

        self.Chan5ColourLineEdit.setEnabled(True)

        self.Chan5ColourLineEdit.blockSignals(False)

        self.Chan5ColourLineEdit.setText(self.instrument.channel_colours[5])

    def channel6(self):

        self.Chan6LabelEdit.setEnabled(True)

        self.Chan6LabelEdit.blockSignals(False)

        self.Chan6LabelEdit.setText(self.instrument.channel_names[6])

        self.PickerButton6.setEnabled(True)

        self.Chan6ColourLineEdit.setEnabled(True)

        self.Chan6ColourLineEdit.blockSignals(False)

        self.Chan6ColourLineEdit.setText(self.instrument.channel_colours[6])

    def channel7(self):

        self.Chan7LabelEdit.setEnabled(True)

        self.Chan7LabelEdit.blockSignals(False)

        self.Chan7LabelEdit.setText(self.instrument.channel_names[7])

        self.PickerButton7.setEnabled(True)

        self.Chan7ColourLineEdit.setEnabled(True)

        self.Chan7ColourLineEdit.blockSignals(False)

        self.Chan7ColourLineEdit.setText(self.instrument.channel_colours[7])

    def channel8(self):

        self.Chan8LabelEdit.setEnabled(True)

        self.Chan8LabelEdit.blockSignals(False)

        self.Chan8LabelEdit.setText(self.instrument.channel_names[8])

        self.PickerButton8.setEnabled(True)

        self.Chan8ColourLineEdit.setEnabled(True)

        self.Chan8ColourLineEdit.blockSignals(False)

        self.Chan8ColourLineEdit.setText(self.instrument.channel_colours[8])

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
            # red
            sender.setStyleSheet('QLineEdit { background-color: #f6989d }')
            self.accepted_state = False
        elif state == QtGui.QValidator.Acceptable:
            # green
            sender.setStyleSheet('QLineEdit { background-color: #c4df9b }')
            self.accepted_state = True
        elif state == QtGui.QValidator.Intermediate and len(sender.text()) == 0:
            # red
            sender.setStyleSheet('QLineEdit { background-color: #f6989d }')
            self.accepted_state = False
        elif state == QtGui.QValidator.Intermediate:
            # yellow
            sender.setStyleSheet('QLineEdit { background-color: #fff79a }')
        else:
            sender.setStyleSheet('QLineEdit { background-color: #f6989d }')

        self.channel_lists()
        self.save_button_state()


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

    def closeEvent(self, event):

        if self.accept_called_state is False:

            if self.configuration_changed() is True:
                self.response_message = 'ABORT', None
                self.reload = False
                self.hide()
            elif self.configuration_changed() is False and self.configuration_check() is False:
                self.response_message = 'ABORT', None
                self.reload = False
                self.hide()
            elif self.configuration_changed() is False:
                result = QtGui.QMessageBox.warning(None,
                                                   None,
                                                   "<br><br>Save changes?",
                                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

                if result == QtGui.QMessageBox.Yes:
                    self.accept_called()
                else:
                    self.response_message = 'ABORT', None
                    self.reload = False
                    self.hide()

    def reject_called(self):

        if self.configuration_changed() is True:
            self.response_message = 'ABORT', None
            self.reload = False
            self.hide()
        elif self.configuration_changed() is False and self.configuration_check() is False:
            self.response_message = 'ABORT', None
            self.reload = False
            self.hide()
        elif self.configuration_changed() is False:
            result = QtGui.QMessageBox.warning(None,
                                               None,
                                               "<br><br>Save changes?",
                                               QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

            if result == QtGui.QMessageBox.Yes:
                self.accept_called()
            else:
                self.response_message = 'ABORT', None
                self.reload = False
                self.hide()

    def accept_called(self):

        self.accept_called_state = True

        # Check .starbasemini/instruments exists otherwise create.
        if os.path.isdir(self.home_path) is not True:
            os.makedirs(self.home_path)

        # get the instrument xml file minus the original path
        file = self.instrument_file.split(os.path.sep)
        file = file[-1]

        # set the new xml to use the users home path location.
        new_file = self.home_path + file

        # import xml file
        tree = ET.parse(self.instrument_file)

        # TODO Move Staribus2Starinet Parameters to XML

        # http://stackoverflow.com/questions/22772739/python-xml-etree-elementtree-append-to-subelement

        root = tree.getroot()

        if self.Staribus2StarinetCheckBox.isChecked():

            if tree.find('Staribus2Starinet') is None:

                staribus2starinet = ET.SubElement(root, 'Staribus2Starinet')
                staribus2starinet.text = 'True'

                staribus2starinetAddress = ET.SubElement(root, 'StarinetAddress')
                staribus2starinetAddress.text = self.StarinetAddressLineEdit.text()

                staribus2starinetPort = ET.SubElement(root, 'StarinetPort')
                staribus2starinetPort.text = self.StarinetPortLineEdit.text()

            else:

                staribus2starinet = tree.find('Staribus2Starinet')
                staribus2starinet.text = 'True'

                starinet_address = tree.find('StarinetAddress')
                starinet_address.text = self.StarinetAddressLineEdit.text()

                starinet_port = tree.find('StarinetPort')
                starinet_port.text = self.StarinetPortLineEdit.text()

        else:

            if tree.find('Staribus2Starinet') is None:

                pass

            else:

                staribus2starinet = tree.find('Staribus2Starinet')
                staribus2starinet.text = 'False'

        # root = tree.getroot()
        # b = ET.SubElement(root, 'Staribus2Starinet')
        # b.text = 'True'

        if self.instrument.instrument_staribus_port != 'None':
            staribus_port = tree.find('StaribusPort')
            staribus_port.text = self.StaribusPortLineEdit.text()

        if self.instrument.instrument_staribus_autodetect != 'None':
            staribus_autodetect = tree.find('StaribusPortAutodetect')

            if self.StaribusAutodetectCheckBox.isEnabled():
                if self.StaribusAutodetectCheckBox.isChecked():
                    staribus_autodetect.text = 'True'
                else:
                    staribus_autodetect.text = 'False'

        if self.instrument.instrument_staribus_address != 'None':
            staribus_address = tree.find('StaribusAddress')
            staribus_address.text = self.comboBox.currentText().zfill(3)

        if self.instrument.instrument_staribus_baudrate != 'None':
            staribus_baudrate = tree.find('StaribusPortBaudrate')
            staribus_baudrate.text = self.BaudrateCombobox.currentText()

        if self.instrument.instrument_staribus_timeout != 'None':
            staribus_timeout = tree.find('StaribusPortTimeout')
            staribus_timeout.text = self.TimeoutCombobox.currentText()

        if self.instrument.instrument_starinet_address != 'None':
            starinet_address = tree.find('StarinetAddress')

            if len(self.StarinetAddressLineEdit.text()) == 0:
                starinet_address.text = 'None'
            else:
                starinet_address.text = self.StarinetAddressLineEdit.text()

        if self.instrument.instrument_starinet_port != 'None':
            starinet_port = tree.find('StarinetPort')

            if len(self.StarinetPortLineEdit.text()) == 0:
                starinet_port.text = 'None'
            else:
                starinet_port.text = self.StarinetPortLineEdit.text()


        channel_metadata = tree.findall('ChannelMetadata')

        chanidx = 0

        for metadata in channel_metadata:
            ChannelLabel = metadata.find('ChannelLabel')
            ChannelLabel.text = self.channel_labels[chanidx]
            chanidx += 1

        chanidx = 0

        for metadata in channel_metadata:
            ChannelColour = metadata.find('ChannelColour')
            ChannelColour.text = self.channel_colours[chanidx]
            chanidx += 1

        logger.info('Writing configuration to : %s ' % new_file)

        tree.write(new_file)

        self.response_message = 'SUCCESS', 'Instrument attributes saved, calling reinitialisation.'

        self.close()