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
        self.relayCheckBox.stateChanged.connect(self.relay_checkbox_triggered)
        self.relayCheckBox.clicked.connect(self.relay_checkbox_triggered)
        self.S2SCheckBox.stateChanged.connect(self.s2s_checkbox_triggered)
        self.S2SCheckBox.clicked.connect(self.s2s_checkbox_triggered)

        # Setup slots for button box save
        self.chooserButton.clicked.connect(self.chooser_triggered)
        self.cancelButton.clicked.connect(self.exit_triggered)
        # self.saveButton.clicked.connect(self.save_triggered)

        # Load the contents of the UI
        self.load_ui()

    def load_ui(self):

        ## loads the ui with the current configuration from disk.

        ##########################
        ### Load 'General' Tab ###
        ##########################

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

        #######################################
        ### Load 'Observatory Metadata' Tab ###
        #######################################


        self.OyNameLineEdit.setText(self.application_conf.get('ObservatoryMetadata', 'name'))
        self.OyNameLineEdit.setToolTip('The name of the Observatory')

        self.OyNameLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observatory_name)))
        self.OyNameLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyNameLineEdit.textChanged.emit(self.OyNameLineEdit.text())

        self.OyDescriptionLineEdit.setText(self.application_conf.get('ObservatoryMetadata', 'description'))
        self.OyDescriptionLineEdit.setToolTip('The description of the Observatory')

        self.OyDescriptionLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observatory_description)))
        self.OyDescriptionLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyDescriptionLineEdit.textChanged.emit(self.OyDescriptionLineEdit.text())

        self.OyEmailLineEdit.setText(self.application_conf.get('ObservatoryMetadata', 'contact_email'))
        self.OyEmailLineEdit.setToolTip('The email address of the Observatory')

        self.OyEmailLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observatory_email)))
        self.OyEmailLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyEmailLineEdit.textChanged.emit(self.OyEmailLineEdit.text())

        self.OyTelephoneLineEdit.setText(self.application_conf.get('ObservatoryMetadata', 'contact_telephone'))
        self.OyTelephoneLineEdit.setToolTip('The telephone number of the Observatory')

        self.OyTelephoneLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observatory_telephone)))
        self.OyTelephoneLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyTelephoneLineEdit.textChanged.emit(self.OyTelephoneLineEdit.text())

        self.OyUrlLineEdit.setText(self.application_conf.get('ObservatoryMetadata', 'contact_url'))
        self.OyUrlLineEdit.setToolTip('The Observatory website URL')

        self.OyUrlLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observatory_url)))
        self.OyUrlLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyUrlLineEdit.textChanged.emit(self.OyUrlLineEdit.text())

        self.OyCountryLineEdit.setText(self.application_conf.get('ObservatoryMetadata', 'country'))
        self.OyCountryLineEdit.setToolTip('The two character Country containing the Observatory (ISO 3166)\n'
                                          'Country Codes: https://www.iso.org/obp/ui/#search/code/')

        self.OyCountryLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observatory_country)))
        self.OyCountryLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyCountryLineEdit.textChanged.emit(self.OyCountryLineEdit.text())

        self.OyTimezoneLineEdit.setText(self.application_conf.get('ObservatoryMetadata', 'timezone'))
        self.OyTimezoneLineEdit.setToolTip('The TimeZone containing the Observatory  GMT-23:59 to GMT+00:00 '
                                           'to GMT+23:59')

        self.OyTimezoneLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observatory_timezone)))
        self.OyTimezoneLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyTimezoneLineEdit.textChanged.emit(self.OyTimezoneLineEdit.text())

        self.OyDatumLineEdit.setText(self.application_conf.get('ObservatoryMetadata', 'geodetic_datum'))
        self.OyDatumLineEdit.setEnabled(False)
        self.OyDatumLineEdit.setToolTip('The GeodeticDatum used by the Observatory - Can not be changed!')

        self.OyDatumLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observatory_datum)))
        self.OyDatumLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyDatumLineEdit.textChanged.emit(self.OyDatumLineEdit.text())

        self.OyMagLatitudeLineEdit.setText(self.application_conf.get('ObservatoryMetadata', 'geomagnetic_latitude'))
        self.OyMagLatitudeLineEdit.setToolTip('The GeomagneticLatitude of the Observatory (North is positive) '
                                              '-89:59:59.9999 to +00:00:00.0000 to +89:59:59.9999')

        self.OyMagLatitudeLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observatory_geomag_latitude)))
        self.OyMagLatitudeLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyMagLatitudeLineEdit.textChanged.emit(self.OyMagLatitudeLineEdit.text())

        self.OyMagLongitudeLineEdit.setText(self.application_conf.get('ObservatoryMetadata', 'geomagnetic_longitude'))
        self.OyMagLongitudeLineEdit.setToolTip('The GeomagneticLongitude of the Observatory (West is positive)  '
                                               '-179:59:59.9999 to +000:00:00.0000 to +179:59:59.9999')

        self.OyMagLongitudeLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observatory_geomag_longitude)))
        self.OyMagLongitudeLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyMagLongitudeLineEdit.textChanged.emit(self.OyMagLongitudeLineEdit.text())

        self.OyModelLineEdit.setText(self.application_conf.get('ObservatoryMetadata', 'geomagnetic_model'))
        self.OyModelLineEdit.setEnabled(False)
        self.OyModelLineEdit.setToolTip('The GeomagneticModel used by the Observatory - Can not be changed!')

        self.OyModelLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observatory_geomag_model)))
        self.OyModelLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyModelLineEdit.textChanged.emit(self.OyModelLineEdit.text())

        self.OyLatitudeLineEdit.setText(self.application_conf.get('ObservatoryMetadata', 'latitude'))
        self.OyLatitudeLineEdit.setToolTip('The Latitude of the Framework (North is positive)  -89:59:59.9999 to '
                                           '+00:00:00.0000 to +89:59:59.9999')

        self.OyLatitudeLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observatory_latitude)))
        self.OyLatitudeLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyLatitudeLineEdit.textChanged.emit(self.OyLatitudeLineEdit.text())

        self.OyLongitudeLineEdit.setText(self.application_conf.get('ObservatoryMetadata', 'longitude'))
        self.OyLongitudeLineEdit.setToolTip('The Longitude of the Observatory (West is positive)  '
                                            '-179:59:59.9999 to +000:00:00.0000 to +179:59:59.999')

        self.OyLongitudeLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observatory_longitude)))
        self.OyLongitudeLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyLongitudeLineEdit.textChanged.emit(self.OyLongitudeLineEdit.text())

        self.OyHaslLineEdit.setText(self.application_conf.get('ObservatoryMetadata', 'hasl'))
        self.OyHaslLineEdit.setToolTip('The observatory height above sea level.')

        self.OyHaslLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observatory_hasl)))
        self.OyHaslLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyHaslLineEdit.textChanged.emit(self.OyHaslLineEdit.text())

        ####################################
        ### Load 'Observer Metadata' Tab ###
        ####################################

        self.ObNameLineEdit.setText(self.application_conf.get('ObserverMetadata', 'name'))
        self.ObNameLineEdit.setToolTip('The name of the Observer')

        self.ObNameLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observer_name)))
        self.ObNameLineEdit.textChanged.connect(self.parameter_check_state)
        self.ObNameLineEdit.textChanged.emit(self.ObNameLineEdit.text())

        self.ObDescriptionLineEdit.setText(self.application_conf.get('ObserverMetadata', 'description'))
        self.ObDescriptionLineEdit.setToolTip('The description of the Observer')

        self.ObDescriptionLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observer_description)))
        self.ObDescriptionLineEdit.textChanged.connect(self.parameter_check_state)
        self.ObDescriptionLineEdit.textChanged.emit(self.ObDescriptionLineEdit.text())

        self.ObEmailLineEdit.setText(self.application_conf.get('ObserverMetadata', 'contact_email'))
        self.ObEmailLineEdit.setToolTip('The email address of the Observer')

        self.ObEmailLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observer_email)))
        self.ObEmailLineEdit.textChanged.connect(self.parameter_check_state)
        self.ObEmailLineEdit.textChanged.emit(self.ObEmailLineEdit.text())

        self.ObTelephoneLineEdit.setText(self.application_conf.get('ObserverMetadata', 'contact_telephone'))
        self.ObTelephoneLineEdit.setToolTip('The Observer telephone number')

        self.ObTelephoneLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observer_telephone)))
        self.ObTelephoneLineEdit.textChanged.connect(self.parameter_check_state)
        self.ObTelephoneLineEdit.textChanged.emit(self.ObTelephoneLineEdit.text())

        self.ObUrlLineEdit.setText(self.application_conf.get('ObserverMetadata', 'contact_url'))
        self.ObUrlLineEdit.setToolTip('The Observer website URL')

        self.ObUrlLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observer_url)))
        self.ObUrlLineEdit.textChanged.connect(self.parameter_check_state)
        self.ObUrlLineEdit.textChanged.emit(self.ObUrlLineEdit.text())

        self.ObCountryLineEdit.setText(self.application_conf.get('ObserverMetadata', 'country'))
        self.ObCountryLineEdit.setToolTip('The two character Country containing the Observatory (ISO 3166)\n'
                                          'Country Codes: https://www.iso.org/obp/ui/#search/code/')

        self.ObCountryLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observer_country)))
        self.ObCountryLineEdit.textChanged.connect(self.parameter_check_state)
        self.ObCountryLineEdit.textChanged.emit(self.ObCountryLineEdit.text())

        self.ObNotesLineEdit.setText(self.application_conf.get('ObserverMetadata', 'notes'))
        self.ObNotesLineEdit.setToolTip('The Observer Notes')

        self.ObNotesLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observer_notes)))
        self.ObNotesLineEdit.textChanged.connect(self.parameter_check_state)
        self.ObNotesLineEdit.textChanged.emit(self.ObNotesLineEdit.text())

    #  Relay check box trigger

    def relay_checkbox_triggered(self):
        if self.relayCheckBox.checkState():
            if self.S2SCheckBox.isChecked():

                result = QtGui.QMessageBox.question(None,
                                                    "Configuration mismatch",
                                                    "\tWARNING!!\n\nYou are trying to enable the Relay while the\n"
                                                    "Staribus to Starinet converter is enabled."
                                                    "\n\nPress Cancel to leave original configuration or Ok to enable Relay.",
                                                    QtGui.QMessageBox.Cancel,QtGui.QMessageBox.Ok)

                if result == QtGui.QMessageBox.Ok:
                    self.S2SCheckBox.setChecked(False)
                    self.ipAddressLineEdit.setEnabled(True)
                    self.portLineEdit.setEnabled(True)
                elif result == QtGui.QMessageBox.Cancel:
                    self.relayCheckBox.setChecked(False)
            else:

                self.ipAddressLineEdit.setEnabled(True)
                self.portLineEdit.setEnabled(True)
        else:
            self.ipAddressLineEdit.setEnabled(False)
            self.portLineEdit.setEnabled(False)

        self.valid_configuration()

    # Staribus to Starinet check box trigger

    def s2s_checkbox_triggered(self):
        if self.S2SCheckBox.checkState():
            if self.relayCheckBox.isChecked():
                result = QtGui.QMessageBox.question(None,
                                                    "Configuration mismatch",
                                                    "\tWARNING!!\n\nYou are trying to enable the Staribus to\n"
                                                    "Starinet converter while the Relay is enabled."
                                                    "\n\nPress Cancel to leave original configuration or Ok to enable the converter.",
                                                    QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Ok)

                if result == QtGui.QMessageBox.Ok:
                    self.relayCheckBox.setChecked(False)
                    self.S2SIpAddressLineEdit.setEnabled(True)
                    self.S2SPort.setEnabled(True)
                elif result == QtGui.QMessageBox.Cancel:
                    self.S2SCheckBox.setChecked(False)

            else:
                self.S2SIpAddressLineEdit.setEnabled(True)
                self.S2SPort.setEnabled(True)

        else:
            self.S2SIpAddressLineEdit.setEnabled(False)
            self.S2SPort.setEnabled(False)

        self.valid_configuration()

    # Data save path chooser trigger

    def chooser_triggered(self):

        file = str(QtGui.QFileDialog.getExistingDirectory(QtGui.QFileDialog(), "Select Directory"))

        if len(file) == 0:
            pass
        else:
            self.savepathLineEdit.setText(file)

    # Save button state check, this enables or disables the save button depending on valid contents.

    def save_button_state(self):

        if self.valid_configuration():
            self.saveButton.setEnabled(True)
        elif self.valid_configuration() is False:
            self.saveButton.setEnabled(False)

    # Valid configuration returns true for valid and false for invalid configuration.

    def valid_configuration(self):
        pass

        # if self.S2SCheckBox.isChecked() and self.relayCheckBox.isChecked():
        #     result = QtGui.QMessageBox.question(None,
        #                                         "Configuration mismatch",
        #                                         "\tWARNING!!\n\nBoth Staribus / Starinet Relay and Staribus to\n"
        #                                         "Starinet Instrument Converter are enabled.\n\n"
        #                                         "Please enable one or t'other.",
        #                                         QtGui.QMessageBox.Ok)

            # if result == QtGui.QMessageBox.Ok:
            #     return False

    # Configuration changed, checks to see if configuration has changed.

    def configuration_changed(self):
        return False

    # Parameter check state changes the colour of the line edit boxes depending on contents.

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

    def closeEvent(self, event):

        print('Close event called.')

        # if self.accept_called_state is False:

        if self.configuration_changed() is True:
            self.response_message = 'ABORT', None
            self.reload = False
            self.hide()
        # elif self.configuration_changed() is False: # and self.configuration_check() is False:
        #     self.response_message = 'ABORT', None
        #     self.reload = False
        #     self.hide()
        elif self.configuration_changed() is False:
            result = QtGui.QMessageBox.question(None,
                                                "Confirm Exit...",
                                                'You have unsaved changes do you want to save them?',
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

            if result == QtGui.QMessageBox.Yes:
                pass
            else:
                self.response_message = 'ABORT', None
                self.close()


    # Exit trigger

    def exit_triggered(self):
        self.response_message = 'ABORT', None
        self.close()