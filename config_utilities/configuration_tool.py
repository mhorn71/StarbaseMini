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
import re

from PyQt4 import QtGui, QtCore

from ui import Ui_ConfigurationDialog
import config_utilities
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

        # Combo box contents
        self.log_levels = ['INFO', 'DEBUG']

        self.legend_loc = ['best', 'upper right', 'upper left', 'lower left', 'lower right', 'center left',
                           'center right', 'lower center', 'upper center', 'center']
        self.legend_font = ['xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large']

        # Setup checkbox slots.
        self.relayCheckBox.stateChanged.connect(self.relay_checkbox_triggered)
        self.relayCheckBox.clicked.connect(self.relay_checkbox_triggered)
        # self.S2SCheckBox.stateChanged.connect(self.s2s_checkbox_triggered)
        # self.S2SCheckBox.clicked.connect(self.s2s_checkbox_triggered)

        # Setup slots for button box save
        self.chooserButton.clicked.connect(self.chooser_triggered)
        self.cancelButton.clicked.connect(self.exit_triggered)
        self.saveButton.clicked.connect(self.save_triggered)

        # This sets a trip so we don't keep showing the pop up warning about data save path not being set.
        self.update_path_trip = 0

        # This set a trip so we don't run the changed config check if we save the data and exit
        self.save_trip = False

        # Load the contents of the UI
        self.load_ui()

    def update_path(self):

        result = QtGui.QMessageBox.warning(None,
                                           "Configuration mismatch",
                                           "<p align='center'>WARNING!!<br><br>You have no data save path set."
                                           "<br>Press Cancel to set later or Ok to open configuration.</p>",
                                           QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Ok)

        if result == QtGui.QMessageBox.Ok:
            self.show()
        elif result == QtGui.QMessageBox.Cancel:
            pass

    def load_ui(self):

        ## loads the ui with the current configuration from disk.

        ##########################
        ### Load 'General' Tab ###
        ##########################

        # Setup data save path line edit box.

        if self.application_conf.get('Application', 'instrument_data_path') == 'Warning: Please set path for exported data.':
            self.savepathLineEdit.setText(self.application_conf.get('Application', 'instrument_data_path'))

            if self.update_path_trip == 0:
                QtCore.QTimer.singleShot(250, self.update_path)
                self.update_path_trip += 1
        elif self.application_conf.get('Application', 'instrument_data_path') is None:

            if self.update_path_trip == 0:
                QtCore.QTimer.singleShot(250, self.update_path)
                self.update_path_trip += 1
        else:
            self.savepathLineEdit.setText(self.application_conf.get('Application', 'instrument_data_path'))

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

        # Setup starinet relay check box and line edits.

        starinetRelay_active = self.application_conf.get('StarinetRelay', 'active')

        if starinetRelay_active == 'True':
            self.relayCheckBox.setChecked(True)
        elif starinetRelay_active == 'False':
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

    # TODO need to fix this as Staribus2Starinet is now set in the Instrument Attributes.

    def relay_checkbox_triggered(self):

        if self.relayCheckBox.checkState():

            self.ipAddressLineEdit.setEnabled(True)

            self.portLineEdit.setEnabled(True)

        else:

            self.ipAddressLineEdit.setEnabled(False)

            self.portLineEdit.setEnabled(False)

    # Data save path chooser trigger

    def chooser_triggered(self):

        file = str(QtGui.QFileDialog.getExistingDirectory(QtGui.QFileDialog(), "Select Directory"))

        if len(file) == 0:

            pass

        else:

            self.savepathLineEdit.setText(file)

    # Save button state check, this enables or disables the save button depending on valid contents.

    def save_button_state(self):

        if self.configuration_check():

            self.saveButton.setEnabled(True)

        elif self.configuration_check() is False:

            self.saveButton.setEnabled(False)

    # Configuration changed, checks to see if configuration has changed.

    def configuration_changed(self):

        trip = 29

        # Check data save path.

        if self.application_conf.get('Application', 'instrument_data_path') is not None:
            if self.savepathLineEdit.text() != self.application_conf.get('Application', 'instrument_data_path'):
                trip -= 1

        # Check log level

        if self.loglevelComboBox.currentText() != self.application_conf.get('logger_root', 'level'):
            trip -= 1

        # Check upgrade checkbox

        if self.UpgradecheckBox.isChecked():
            upgrade = "True"
        else:
            upgrade = "False"

        if upgrade != self.application_conf.get('Application', 'instrument_upgrade'):
            trip -= 1

        # Check Starinet relay section

        if self.relayCheckBox.isChecked():
            starinetRelay = "True"
        else:
            starinetRelay = "False"

        if starinetRelay != self.application_conf.get('StarinetRelay', 'active'):
            trip -= 1

        if self.ipAddressLineEdit.text() != self.application_conf.get('StarinetRelay', 'address'):
            trip -= 1

        if self.portLineEdit.text() != self.application_conf.get('StarinetRelay', 'starinet_port'):
            trip -= 1

        # Check legend section

        if self.legendLocationComboBox.currentText() != self.application_conf.get('Legend', 'location'):
            trip -= 1

        if str(self.LegendColSpinBox.value()) != self.application_conf.get('Legend', 'columns'):
            trip -= 1

        if self.LegendFontComboBox.currentText() != self.application_conf.get('Legend', 'font'):
            trip -= 1

        # Check Observatory Metadata.

        if self.OyNameLineEdit.text() != self.application_conf.get('ObservatoryMetadata', 'name'):
            trip -= 1

        if self.OyDescriptionLineEdit.text() != self.application_conf.get('ObservatoryMetadata', 'description'):
            trip -= 1

        if self.OyEmailLineEdit.text() != self.application_conf.get('ObservatoryMetadata', 'contact_email'):
            trip -= 1

        if self.OyTelephoneLineEdit.text() != self.application_conf.get('ObservatoryMetadata', 'contact_telephone'):
            trip -= 1

        if self.OyUrlLineEdit.text() != self.application_conf.get('ObservatoryMetadata', 'contact_url'):
            trip -= 1

        if self.OyCountryLineEdit.text() != self.application_conf.get('ObservatoryMetadata', 'country'):
            trip -= 1

        if self.OyTimezoneLineEdit.text() != self.application_conf.get('ObservatoryMetadata', 'timezone'):
            trip -= 1

        if self.OyDatumLineEdit.text() != self.application_conf.get('ObservatoryMetadata', 'geodetic_datum'):
            trip -= 1

        if self.OyMagLatitudeLineEdit.text() != self.application_conf.get('ObservatoryMetadata', 'geomagnetic_latitude'):
            trip -= 1

        if self.OyMagLongitudeLineEdit.text() != self.application_conf.get('ObservatoryMetadata', 'geomagnetic_longitude'):
            trip -= 1

        if self.OyModelLineEdit.text() != self.application_conf.get('ObservatoryMetadata', 'geomagnetic_model'):
            trip -= 1

        if self.OyLatitudeLineEdit.text() != self.application_conf.get('ObservatoryMetadata', 'latitude'):
            trip -= 1

        if self.OyLongitudeLineEdit.text() != self.application_conf.get('ObservatoryMetadata', 'longitude'):
            trip -= 1

        if self.OyHaslLineEdit.text() != self.application_conf.get('ObservatoryMetadata', 'hasl'):
            trip -= 1

        # Check Observer Metadata.

        if self.ObNameLineEdit.text() != self.application_conf.get('ObserverMetadata', 'name'):
            trip -= 1

        if self.ObDescriptionLineEdit.text() != self.application_conf.get('ObserverMetadata', 'description'):
            trip -= 1

        if self.ObEmailLineEdit.text() != self.application_conf.get('ObserverMetadata', 'contact_email'):
            trip -= 1

        if self.ObTelephoneLineEdit.text() != self.application_conf.get('ObserverMetadata', 'contact_telephone'):
            trip -= 1

        if self.ObUrlLineEdit.text() != self.application_conf.get('ObserverMetadata', 'contact_url'):
            trip -= 1

        if self.ObCountryLineEdit.text() != self.application_conf.get('ObserverMetadata', 'country'):
            trip -= 1

        if self.ObNotesLineEdit.text() != self.application_conf.get('ObserverMetadata', 'notes'):
            trip -= 1

        if trip == 29:
            return False
        else:
            return True

    # Configuration validation check.

    def configuration_check(self):

        trip = 30

        # Check Starinet relay section

        if not re.match(constants.starinet_ip, self.ipAddressLineEdit.text()):
            trip -= 1


        if not re.match(constants.starinet_port, self.portLineEdit.text()):
            trip -= 1

        # Check Observatory Metadata.

        if not re.match(constants.observatory_name, self.OyNameLineEdit.text()) or len(self.OyNameLineEdit.text()) ==0:
            trip -= 1

        if not re.match(constants.observatory_description, self.OyDescriptionLineEdit.text()) or len(self.OyDescriptionLineEdit.text()) ==0:
            trip -= 1

        if not re.match(constants.observatory_email, self.OyEmailLineEdit.text()) or len(self.OyEmailLineEdit.text()) ==0:
            trip -= 1

        if not re.match(constants.observatory_telephone, self.OyTelephoneLineEdit.text()) or len(self.OyTelephoneLineEdit.text()) ==0:
            trip -= 1

        if not re.match(constants.observatory_url, self.OyUrlLineEdit.text()) or len(self.OyUrlLineEdit.text()) ==0:
            trip -= 1

        if not re.match(constants.observatory_country, self.OyCountryLineEdit.text()) or len(self.OyCountryLineEdit.text()) ==0:
            trip -= 1

        if not re.match(constants.observatory_timezone, self.OyTimezoneLineEdit.text()):
            trip -= 1

        if not re.match(constants.observatory_datum, self.OyDatumLineEdit.text()) or len(self.OyNameLineEdit.text()) ==0:
            trip -= 1

        if not re.match(constants.observatory_geomag_latitude, self.OyMagLatitudeLineEdit.text()):
            trip -= 1

        if not re.match(constants.observatory_geomag_longitude, self.OyMagLongitudeLineEdit.text()):
            trip -= 1

        if not re.match(constants.observatory_geomag_model, self.OyModelLineEdit.text()):
            trip -= 1

        if not re.match(constants.observatory_latitude, self.OyLatitudeLineEdit.text()):
            trip -= 1

        if not re.match(constants.observatory_longitude, self.OyLongitudeLineEdit.text()):
            trip -= 1

        if not re.match(constants.observatory_hasl, self.OyHaslLineEdit.text()):
            trip -= 1

        # Check Observer Metadata.

        if not re.match(constants.observer_name, self.ObNameLineEdit.text()) or len(self.ObNameLineEdit.text()) ==0:
            trip -= 1

        if not re.match(constants.observer_description, self.ObDescriptionLineEdit.text()) or len(self.ObDescriptionLineEdit.text()) ==0:
            trip -= 1

        if not re.match(constants.observer_email, self.ObEmailLineEdit.text()) or len(self.ObEmailLineEdit.text()) ==0:
            trip -= 1

        if not re.match(constants.observer_telephone, self.ObTelephoneLineEdit.text()) or len(self.ObTelephoneLineEdit.text()) ==0:
            trip -= 1

        if not re.match(constants.observer_url, self.ObUrlLineEdit.text()) or len(self.ObUrlLineEdit.text()) ==0:
            trip -= 1

        if not re.match(constants.observer_country, self.ObCountryLineEdit.text()):
            trip -= 1

        if not re.match(constants.observer_notes, self.ObNotesLineEdit.text()) or len(self.ObNotesLineEdit.text()) ==0:
            trip -= 1

        if trip == 30:
            return True
        else:
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
            color = '#f6989d'  # red
            sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
            self.save_button_state()
        elif state == QtGui.QValidator.Acceptable:
            color = '#c4df9b'  # green
            sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
            self.save_button_state()
        elif state == QtGui.QValidator.Intermediate and len(sender.text()) == 0:
            color = '#f6989d'  # red
            sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
            self.save_button_state()
        elif state == QtGui.QValidator.Intermediate:
            color = '#fff79a'  # yellow
            sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
            self.save_button_state()
        else:
            sender.setStyleSheet('QLineEdit { background-color: #f6989d')
            self.save_button_state()

    def closeEvent(self, event):

        if self.save_trip is True:
            self.hide()
            self.save_trip = False
        else:

            if self.configuration_changed() is False:
                self.response_message = 'ABORT', None
                self.reload = False
                self.hide()
                self.load_ui()
            elif self.configuration_changed() and self.configuration_check():
                result = QtGui.QMessageBox.warning(None,
                                                   None,
                                                   '<br><br>Save changes?',
                                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

                if result == QtGui.QMessageBox.Yes:
                    self.save_triggered()
                else:
                    self.response_message = 'ABORT', None
                    self.close()
                    self.load_ui()
            else:
                self.response_message = 'ABORT', None
                self.reload = False
                self.hide()
                self.load_ui()

    # Exit

    def exit_triggered(self):
        if self.configuration_changed():
            self.close()
        else:
            self.response_message = 'ABORT', None
            self.load_ui()
            self.close()

    def save_triggered(self):

        self.save_trip = True

        # Application
        self.application_conf.set('Application', 'instrument_data_path', self.savepathLineEdit.text())

        # Logging Level
        self.application_conf.set('logger_root', 'level', self.loglevelComboBox.itemText(
            self.loglevelComboBox.currentIndex()))

        # UpgradeCheckbox
        if self.UpgradecheckBox.checkState():
            self.application_conf.set('Application', 'instrument_upgrade', 'True')
        else:
            self.application_conf.set('Application', 'instrument_upgrade', 'False')

        # StarinetConnector
        if self.relayCheckBox.checkState():
            self.application_conf.set('StarinetRelay', 'active', 'True')
        else:
            self.application_conf.set('StarinetRelay', 'active', 'False')

        self.application_conf.set('StarinetRelay', 'address', self.ipAddressLineEdit.text())
        self.application_conf.set('StarinetRelay', 'starinet_port', self.portLineEdit.text())

        # Chart Legend
        self.application_conf.set('Legend', 'location',
                                  self.legendLocationComboBox.itemText(self.legendLocationComboBox.currentIndex()))

        self.application_conf.set('Legend', 'columns', str(self.LegendColSpinBox.value()))

        self.application_conf.set('Legend', 'font',
                                  self.LegendFontComboBox.itemText(self.LegendFontComboBox.currentIndex()))

        # ObservatoryMetadata
        self.application_conf.set('ObservatoryMetadata', 'name', self.OyNameLineEdit.text())
        self.application_conf.set('ObservatoryMetadata', 'description', self.OyDescriptionLineEdit.text())
        self.application_conf.set('ObservatoryMetadata', 'contact_email', self.OyEmailLineEdit.text())
        self.application_conf.set('ObservatoryMetadata', 'contact_telephone', self.OyTelephoneLineEdit.text())
        self.application_conf.set('ObservatoryMetadata', 'contact_url', self.OyUrlLineEdit.text())
        self.application_conf.set('ObservatoryMetadata', 'country', self.OyCountryLineEdit.text())
        self.application_conf.set('ObservatoryMetadata', 'timezone', self.OyTimezoneLineEdit.text())
        self.application_conf.set('ObservatoryMetadata', 'geomagnetic_latitude', self.OyMagLatitudeLineEdit.text())
        self.application_conf.set('ObservatoryMetadata', 'geomagnetic_longitude', self.OyMagLongitudeLineEdit.text())
        self.application_conf.set('ObservatoryMetadata', 'latitude', self.OyLatitudeLineEdit.text())
        self.application_conf.set('ObservatoryMetadata', 'longitude', self.OyLongitudeLineEdit.text())
        self.application_conf.set('ObservatoryMetadata', 'hasl', self.OyHaslLineEdit.text())

        # ObserverMetadata
        self.application_conf.set('ObserverMetadata', 'name', self.ObNameLineEdit.text())
        self.application_conf.set('ObserverMetadata', 'description', self.ObDescriptionLineEdit.text())
        self.application_conf.set('ObserverMetadata', 'contact_email', self.ObEmailLineEdit.text())
        self.application_conf.set('ObserverMetadata', 'contact_telephone', self.ObTelephoneLineEdit.text())
        self.application_conf.set('ObserverMetadata', 'contact_url', self.ObUrlLineEdit.text())
        self.application_conf.set('ObserverMetadata', 'country', self.ObCountryLineEdit.text())
        self.application_conf.set('ObserverMetadata', 'notes', self.ObNotesLineEdit.text())

        self.response_message = 'SUCCESS', 'Configuration saved.'

        self.load_ui()
        self.close()