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

import logging
import sys
import os

from PyQt4 import QtGui, QtCore

from ui import Ui_ConfigurationDialog
import config_utilities
import xml_utilities
import constants

logger = logging.getLogger('core.configTool')


class ConfigManager(QtGui.QDialog, Ui_ConfigurationDialog):
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

        # Initialise application configuration class
        self.application_conf = config_utilities.ConfigLoader()

        # Set the default reponse message to abort
        self.response_message = 'ABORT', None

        # Initialise the users instruments.xml if it's present in the .starbasemini/instruments folder.

        self.instruments_local = None

        instruments_xml_user = os.path.expanduser('~') + os.path.sep + '.starbasemini' + os.path.sep + 'instruments' + \
                            os.path.sep + 'instruments.xml'

        if os.path.isfile(instruments_xml_user):
            self.instruments_local = xml_utilities.Instruments(instruments_xml_user)

        instruments_system = 'instruments' + os.path.sep + 'instruments.xml'

        # Initialise the default instruments.xml file from the installaton path, instruments folder.

        self.instruments = xml_utilities.Instruments('instruments' + os.path.sep + 'instruments.xml')

        # Combo box contents
        self.log_levels = ['INFO', 'DEBUG']

        self.legend_loc = ['best', 'upper right', 'upper left', 'lower left', 'lower right', 'center left',
                           'center right', 'lower center', 'upper center', 'center']
        self.legend_font = ['xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large']

        # Setup checkbox slots.
        # self.relayCheckBox.stateChanged.connect(self.relay_checkbox_triggered)
        # self.S2SCheckBox.stateChanged.connect(self.s2s_checkbox_triggered)

        # Setup slots for button box save
        # self.chooserButton.clicked.connect(self.chooser_triggered)
        # self.cancelButton.clicked.connect(self.exit_triggered)
        # self.saveButton.clicked.connect(self.save_triggered)

        # Load the contents of the UI
        self.load_ui()

    def load_ui(self):

        #loads the ui with the current configuration from disk.

        # Load 'General' Tab Box

        # Setup data save path line edit box.

        data_save_path = self.application_conf.get('Application', 'instrument_data_path')

        # Setup data save path, show warning if None.
        if data_save_path is None:
            self.savepathLineEdit.setText('Warning: Please set path for exported data.')
        else:
            self.savepathLineEdit.setText(data_save_path)

        self.savepathLineEdit.setToolTip('The full path where you wish to save your downloaded data.')

        if sys.platform.startswith('win32'):
            savepath_regex = constants.windows_path
        else:
            savepath_regex = constants.unix_path

        self.savepathLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(savepath_regex)))
        self.savepathLineEdit.textChanged.connect(self.parameter_check_state)
        self.savepathLineEdit.textChanged.emit(self.savepathLineEdit.text())

        # Setup log level

        self.loglevelComboBox.addItems(self.log_levels)
        self.loglevelComboBox.setCurrentIndex(self.log_levels.index(self.application_conf.get('logger_root', 'level')))

        # Setup upgrade checkbox

        upgrade_check = self.application_conf.get('Application', 'instrument_upgrade')

        if upgrade_check == 'True':
            self.UpgradecheckBox.setChecked(True)
        elif upgrade_check == 'False':
            self.UpgradecheckBox.setChecked(False)

        # Setup starinetConnector (Relay) check box and line edits.

        starinetConnector_active = self.application_conf.get('StarinetRelay', 'active')

        if starinetConnector_active == 'True':
            self.relayCheckBox.setChecked(True)
        elif starinetConnector_active == 'False':
            self.ipAddressLineEdit.setEnabled(False)
            self.portLineEdit.setEnabled(False)

        self.ipAddressLineEdit.setText(self.application_conf.get('StarinetRelay', 'address'))
        self.ipAddressLineEdit.setToolTip('IPv4 Address only IPv6 not supported.\n'
                                          'Default 0.0.0.0 will bind to all IPv4 interfaces.')

        self.ipAddressLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.starinet_ip)))
        self.ipAddressLineEdit.textChanged.connect(self.parameter_check_state)
        self.ipAddressLineEdit.textChanged.emit(self.ipAddressLineEdit.text())

        self.portLineEdit.setText(self.application_conf.get('StarinetRelay', 'starinet_port'))
        self.portLineEdit.setToolTip('Port can be in the range 1 - 65535, default is 1205')

        self.portLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.starinet_port)))
        self.portLineEdit.textChanged.connect(self.parameter_check_state)
        self.portLineEdit.textChanged.emit(self.portLineEdit.text())

        # Setup staribus to starinet check box and line edits.
        staribus2starinet_active = self.application_conf.get('Staribus2Starinet', 'active')

        if staribus2starinet_active == 'True':
            self.S2SCheckBox.setChecked(True)
        elif staribus2starinet_active == 'False':
            self.S2SIpAddressLineEdit.setEnabled(False)
            self.S2SPort.setEnabled(False)

        self.S2SIpAddressLineEdit.setText(self.application_conf.get('Staribus2Starinet', 'address'))
        self.S2SIpAddressLineEdit.setToolTip(
            'The IPv4 address of the relay or instrument.\nIPv4 Address only IPv6 not '
            'supported.')

        self.S2SIpAddressLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.starinet_ip)))
        self.S2SIpAddressLineEdit.textChanged.connect(self.parameter_check_state)
        self.S2SIpAddressLineEdit.textChanged.emit(self.S2SIpAddressLineEdit.text())


        self.S2SPort.setText(self.application_conf.get('Staribus2Starinet', 'starinet_port'))
        self.S2SPort.setToolTip('Port can be in the range 1 - 65535, default is 1205')

        self.S2SPort.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.starinet_port)))
        self.S2SPort.textChanged.connect(self.parameter_check_state)
        self.S2SPort.textChanged.emit(self.S2SPort.text())


        # Setup chart legend, font and column combo boxes

        self.legendLocationComboBox.addItems(self.legend_loc)
        self.legendLocationComboBox.setCurrentIndex(self.legend_loc.index(
            self.application_conf.get('Legend', 'location')))

        self.LegendColSpinBox.setValue(int(self.application_conf.get('Legend', 'columns')))

        self.LegendFontComboBox.addItems(self.legend_font)
        self.LegendFontComboBox.setCurrentIndex(self.legend_font.index(self.application_conf.get('Legend', 'font')))





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
