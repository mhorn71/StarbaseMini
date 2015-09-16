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

        logger.info('Started')

        self.application_conf = config_utilities.ConfigLoader()

        self.instruments_local = None
        
        self.response_message = 'ABORT', None

        instruments_local = os.path.expanduser('~') + os.path.sep + '.starbasemini' + os.path.sep + 'instruments' + \
                            os.path.sep + 'instruments.xml'

        if os.path.isfile(instruments_local):
            self.instruments_local = xml_utilities.Instruments(instruments_local)

        instruments_system = 'instruments' + os.path.sep + 'instruments.xml'

        self.instruments = xml_utilities.Instruments(instruments_system)
        
        self.loglevels = ['INFO', 'DEBUG']
        self.baudrates = ['9600', '19200', '38400', '57600', '115200']
        self.timeouts = ['20', '30', '40', '50', '60']
        self.legend_loc = ['best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left',
                           'center right', 'lower center', 'upper center', 'center']
        self.legend_font = ['xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large']

        # Setup checkbox slots.
        self.detectInstrumentPortCheckBox.stateChanged.connect(self.instrument_port_checkbox_triggered)
        self.baudrateDefaultCheckBox.stateChanged.connect(self.baudrate_checkbox_triggered)
        self.serialPortTimeoutCheckBox.stateChanged.connect(self.timeout_checkbox_triggered)
        self.relayCheckBox.stateChanged.connect(self.relay_checkbox_triggered)
        self.S2SCheckBox.stateChanged.connect(self.s2s_checkbox_triggered)

        # Setup slots for button box save
        self.chooserButton.clicked.connect(self.chooser_triggered)
        self.cancelButton.clicked.connect(self.exit_triggered)
        self.saveButton.clicked.connect(self.save_triggered)

        self.load_ui()

    def load_ui(self):
        '''
        loads the ui with the current configuration from disk.
        '''

        # Load 'General' Tab

        data_save_path = self.application_conf.get('Application', 'instrument_data_path')
        instrument_name = self.application_conf.get('Application', 'instrument_identifier')
        loglevel = self.application_conf.get('logger_root', 'level')

        # Data save path show blank if set to None.
        if data_save_path is None:
            self.savepathLineEdit.setText('Warning: Please set path for exported data.')
        else:
            self.savepathLineEdit.setText(data_save_path)

        self.savepathLineEdit.setToolTip('The full path to where you wish to save your downloaded data.')

        if sys.platform.startswith('win32'):
            savepath_regex = constants.windows_path
        else:
            savepath_regex = constants.unix_path

        savepathLineEditRegexp = QtCore.QRegExp(savepath_regex)
        savepathLineEditValidator = QtGui.QRegExpValidator(savepathLineEditRegexp)
        self.savepathLineEdit.setValidator(savepathLineEditValidator)
        self.savepathLineEdit.textChanged.connect(self.parameter_check_state)
        self.savepathLineEdit.textChanged.emit(self.savepathLineEdit.text())

        # Set up instruments combo box.
        instruments = self.instruments.get_names()

        if self.instruments_local is not None:
            for i in self.instruments_local.get_names():
                instruments.append(i)

        self.instrumentComboBox.addItems(instruments)
        self.instrumentComboBox.setCurrentIndex(instruments.index(instrument_name))

        # Set up log level combo box.
        
        self.loglevelComboBox.addItems(self.loglevels)
        self.loglevelComboBox.setCurrentIndex(self.loglevels.index(loglevel))

        #  Set Detect staribus port checkbox

        detect_staribus_port = self.application_conf.get('Application', 'instrument_autodetect')

        if detect_staribus_port == 'False':
            self.detectInstrumentPortCheckBox.setChecked(False)
        elif detect_staribus_port == 'True':
            self.detectInstrumentPortCheckBox.setChecked(True)
            self.serialPortLineEdit.setEnabled(False)  # Disable port entry box if auto detect is true.
        else:
            logger.warning('Unable to detect staribus port check state, setting to default \'False\'.')
            self.application_conf.set('Application', 'instrument_autodetect', 'False')
            self.detectInstrumentPortCheckBox.setChecked(False)

        self.detectInstrumentPortCheckBox.setToolTip('Will check each serial ports for the configured instrument'
                                                     '\nNote : The configured instrument must be attached.')

        # Set serial port name in entry box.
        port = self.application_conf.get('StaribusPort', 'staribus_port')

        if port is None:
            if self.application_conf.get('Application', 'instrument_autodetect'):
                port = 'No serial ports detected!!'
            else:
                port = 'No serial port set!!'

        self.serialPortLineEdit.setText(port)
        serialPortLineEditRegexp = QtCore.QRegExp(constants.staribus_port)
        serialPortLineEditValidator = QtGui.QRegExpValidator(serialPortLineEditRegexp)
        self.serialPortLineEdit.setValidator(serialPortLineEditValidator)
        self.serialPortLineEdit.textChanged.connect(self.parameter_check_state)
        self.serialPortLineEdit.textChanged.emit(self.serialPortLineEdit.text())

        if sys.platform.startswith('win32'):
            self.serialPortLineEdit.setToolTip('The com port to which the instrument is attached, such as COM1')
        else:
            self.serialPortLineEdit.setToolTip('The full path and serial port the instrument is attached, '
                                               'such as /dev/ttyS0')

        # Set baudrate check box and combo box.
        baudrate = self.application_conf.get('StaribusPort', 'baudrate')

        if baudrate == '57600':
            self.baudrateDefaultCheckBox.setChecked(True)
            self.baudrateComboBox.setEnabled(False)  # Disable combo box if default set.

        self.baudrateDefaultCheckBox.setToolTip('Sets the default baudrate to 57600')

        self.baudrateComboBox.addItems(self.baudrates)
        self.baudrateComboBox.setCurrentIndex(self.baudrates.index(baudrate))

        # Set timeout check box and combo box.
        timeout = self.application_conf.get('StaribusPort', 'timeout')

        if timeout == '20':
            self.serialPortTimeoutCheckBox.setChecked(True)
            self.timeoutComboBox.setEnabled(False)

        self.serialPortTimeoutCheckBox.setToolTip('Sets the default Staribus port timeout to 20 seconds')

        self.timeoutComboBox.addItems(self.timeouts)
        self.timeoutComboBox.setCurrentIndex(self.timeouts.index(timeout))

        # Set starinetConnector (Relay) check box and line edits.
        starinetConnector_active = self.application_conf.get('StarinetRelay', 'active')

        if starinetConnector_active == 'True':
            self.relayCheckBox.setChecked(True)
        elif starinetConnector_active == 'False':
            self.ipAddressLineEdit.setEnabled(False)
            self.portLineEdit.setEnabled(False)

        starinetConnector_address = self.application_conf.get('StarinetRelay', 'address')
        self.ipAddressLineEdit.setText(starinetConnector_address)
        self.ipAddressLineEdit.setToolTip('IPv4 Address only IPv6 not supported.\n'
                                          'Default 0.0.0.0 will bind to all IPv4 interfaces.')
        ipAddressLineEditRegexp = QtCore.QRegExp(constants.starinet_ip)
        ipAddressLineEditValidator = QtGui.QRegExpValidator(ipAddressLineEditRegexp)
        self.ipAddressLineEdit.setValidator(ipAddressLineEditValidator)
        self.ipAddressLineEdit.textChanged.connect(self.parameter_check_state)
        self.ipAddressLineEdit.textChanged.emit(self.ipAddressLineEdit.text())

        starinetConnector_port = self.application_conf.get('StarinetRelay', 'starinet_port')
        self.portLineEdit.setText(starinetConnector_port)
        self.portLineEdit.setToolTip('Port can be in the range 1 - 65535, default is 1205')
        portLineEditRegexp = QtCore.QRegExp(constants.starinet_port)
        portLineEditValidator = QtGui.QRegExpValidator(portLineEditRegexp)
        self.portLineEdit.setValidator(portLineEditValidator)
        self.portLineEdit.textChanged.connect(self.parameter_check_state)
        self.portLineEdit.textChanged.emit(self.portLineEdit.text())

        # Set starinetConnector (Relay) check box and line edits.
        staribus2starinet_active = self.application_conf.get('Staribus2Starinet', 'active')

        if staribus2starinet_active == 'True':
            self.S2SCheckBox.setChecked(True)
        elif staribus2starinet_active == 'False':
            self.S2SIpAddressLineEdit.setEnabled(False)
            self.S2SPort.setEnabled(False)

        # Chart legend
        self.legendLocationComboBox.addItems(self.legend_loc)
        self.legendLocationComboBox.setCurrentIndex(self.legend_loc.index(
                                                    self.application_conf.get('Legend', 'location')))

        self.LegendFontComboBox.addItems(self.legend_font)
        self.LegendFontComboBox.setCurrentIndex(self.legend_font.index(self.application_conf.get('Legend', 'font')))

        self.LegendColSpinBox.setValue(int(self.application_conf.get('Legend', 'columns')))

        staribus2starinet_address = self.application_conf.get('Staribus2Starinet', 'address')
        self.S2SIpAddressLineEdit.setText(staribus2starinet_address)
        self.S2SIpAddressLineEdit.setToolTip('The IPv4 address of the relay or instrument.\nIPv4 Address only IPv6 not '
                                             'supported.')
        S2SIpAddressLineEditRegexp = QtCore.QRegExp(constants.starinet_ip)
        S2SIpAddressLineEditValidator = QtGui.QRegExpValidator(S2SIpAddressLineEditRegexp)
        self.S2SIpAddressLineEdit.setValidator(S2SIpAddressLineEditValidator)
        self.S2SIpAddressLineEdit.textChanged.connect(self.parameter_check_state)
        self.S2SIpAddressLineEdit.textChanged.emit(self.S2SIpAddressLineEdit.text())

        staribus2starinet_port = self.application_conf.get('Staribus2Starinet', 'starinet_port')
        self.S2SPort.setText(staribus2starinet_port)
        self.S2SPort.setToolTip('Port can be in the range 1 - 65535, default is 1205')
        S2SPortRegexp = QtCore.QRegExp(constants.starinet_port)
        S2SPortValidator = QtGui.QRegExpValidator(S2SPortRegexp)
        self.S2SPort.setValidator(S2SPortValidator)
        self.S2SPort.textChanged.connect(self.parameter_check_state)
        self.S2SPort.textChanged.emit(self.S2SPort.text())

        # Load Observatory Metadata Tab

        OyName = self.application_conf.get('ObservatoryMetadata', 'name')
        self.OyNameLineEdit.setText(OyName)
        self.OyNameLineEdit.setToolTip('The name of the Observatory')
        OyNameLineEditRegexp = QtCore.QRegExp(constants.observatory_name)
        OyNameLineEditValidator = QtGui.QRegExpValidator(OyNameLineEditRegexp)
        self.OyNameLineEdit.setValidator(OyNameLineEditValidator)
        self.OyNameLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyNameLineEdit.textChanged.emit(self.OyNameLineEdit.text())

        OyDescription = self.application_conf.get('ObservatoryMetadata', 'description')
        self.OyDescriptionLineEdit.setText(OyDescription)
        self.OyDescriptionLineEdit.setToolTip('The description of the Observatory')
        OyDescriptionLineEditRegexp = QtCore.QRegExp(constants.observatory_description)
        OyDescriptionLineEditValidator = QtGui.QRegExpValidator(OyDescriptionLineEditRegexp)
        self.OyDescriptionLineEdit.setValidator(OyDescriptionLineEditValidator)
        self.OyDescriptionLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyDescriptionLineEdit.textChanged.emit(self.OyDescriptionLineEdit.text())

        OyEmail = self.application_conf.get('ObservatoryMetadata', 'contact_email')
        self.OyEmailLineEdit.setText(OyEmail)
        self.OyEmailLineEdit.setToolTip('The email address of the Observatory')
        OyEmailLineEditRegexp = QtCore.QRegExp(constants.observatory_email)
        OyEmailLineEditValidator = QtGui.QRegExpValidator(OyEmailLineEditRegexp)
        self.OyEmailLineEdit.setValidator(OyEmailLineEditValidator)
        self.OyEmailLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyEmailLineEdit.textChanged.emit(self.OyEmailLineEdit.text())

        OyTelephone = self.application_conf.get('ObservatoryMetadata', 'contact_telephone')
        self.OyTelephoneLineEdit.setText(OyTelephone)
        self.OyTelephoneLineEdit.setToolTip('The telephone number of the Observatory')
        OyTelephoneLineEditRegexp = QtCore.QRegExp(constants.observatory_telephone)
        OyTelephoneLineEditValidator = QtGui.QRegExpValidator(OyTelephoneLineEditRegexp)
        self.OyTelephoneLineEdit.setValidator(OyTelephoneLineEditValidator)
        self.OyTelephoneLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyTelephoneLineEdit.textChanged.emit(self.OyTelephoneLineEdit.text())

        OyURL = self.application_conf.get('ObservatoryMetadata', 'contact_url')
        self.OyUrlLineEdit.setText(OyURL)
        self.OyUrlLineEdit.setToolTip('The Observatory website URL')
        OyUrlLineEditRegexp = QtCore.QRegExp(constants.observatory_url)
        OyUrlLineEditValidator = QtGui.QRegExpValidator(OyUrlLineEditRegexp)
        self.OyUrlLineEdit.setValidator(OyUrlLineEditValidator)
        self.OyUrlLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyUrlLineEdit.textChanged.emit(self.OyUrlLineEdit.text())

        OyCountry = self.application_conf.get('ObservatoryMetadata', 'country')
        self.OyCountryLineEdit.setText(OyCountry)
        self.OyCountryLineEdit.setToolTip('The two character Country containing the Observatory (ISO 3166)\n'
                                          'Country Codes: https://www.iso.org/obp/ui/#search/code/')
        OyCountryLineEditRegexp = QtCore.QRegExp(constants.observatory_country)
        OyCountryLineEditValidator = QtGui.QRegExpValidator(OyCountryLineEditRegexp)
        self.OyCountryLineEdit.setValidator(OyCountryLineEditValidator)
        self.OyCountryLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyCountryLineEdit.textChanged.emit(self.OyCountryLineEdit.text())

        OyTimezone = self.application_conf.get('ObservatoryMetadata', 'timezone')
        self.OyTimezoneLineEdit.setText(OyTimezone)
        self.OyTimezoneLineEdit.setToolTip('The TimeZone containing the Observatory  GMT-23:59 to GMT+00:00 '
                                           'to GMT+23:59 or UTC')
        OyTimezoneLineEditRegexp = QtCore.QRegExp(constants.observatory_timezone)
        OyTimezoneLineEditValidator = QtGui.QRegExpValidator(OyTimezoneLineEditRegexp)
        self.OyTimezoneLineEdit.setValidator(OyTimezoneLineEditValidator)
        self.OyTimezoneLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyTimezoneLineEdit.textChanged.emit(self.OyTimezoneLineEdit.text())

        OyDatum = self.application_conf.get('ObservatoryMetadata', 'geodetic_datum')
        self.OyDatumLineEdit.setText(OyDatum)
        self.OyDatumLineEdit.setEnabled(False)
        self.OyDatumLineEdit.setToolTip('The GeodeticDatum used by the Observatory - Can not be changed!')
        OyDatumLineEditRegexp = QtCore.QRegExp(constants.observatory_datum)
        OyDatumLineEditValidator = QtGui.QRegExpValidator(OyDatumLineEditRegexp)
        self.OyDatumLineEdit.setValidator(OyDatumLineEditValidator)
        self.OyDatumLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyDatumLineEdit.textChanged.emit(self.OyDatumLineEdit.text())

        OyGeoLat = self.application_conf.get('ObservatoryMetadata', 'geomagnetic_latitude')
        self.OyMagLatitudeLineEdit.setText(OyGeoLat)
        self.OyMagLatitudeLineEdit.setToolTip('The GeomagneticLatitude of the Observatory (North is positive) '
                                              '-89:59:59.9999 to +00:00:00.0000 to +89:59:59.9999')
        OyMagLatitudeLineEditRegexp = QtCore.QRegExp(constants.observatory_geomag_latitude)
        OyMagLatitudeLineEditValidator = QtGui.QRegExpValidator(OyMagLatitudeLineEditRegexp)
        self.OyMagLatitudeLineEdit.setValidator(OyMagLatitudeLineEditValidator)
        self.OyMagLatitudeLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyMagLatitudeLineEdit.textChanged.emit(self.OyMagLatitudeLineEdit.text())

        OyGeoLong = self.application_conf.get('ObservatoryMetadata', 'geomagnetic_longitude')
        self.OyMagLongitudeLineEdit.setText(OyGeoLong)
        self.OyMagLongitudeLineEdit.setToolTip('The GeomagneticLongitude of the Observatory (West is positive)  '
                                               '-179:59:59.9999 to +000:00:00.0000 to +179:59:59.9999')
        OyMagLongitudeLineEditRegexp = QtCore.QRegExp(constants.observatory_geomag_longitude)
        OyMagLongitudeLineEditValidator = QtGui.QRegExpValidator(OyMagLongitudeLineEditRegexp)
        self.OyMagLongitudeLineEdit.setValidator(OyMagLongitudeLineEditValidator)
        self.OyMagLongitudeLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyMagLongitudeLineEdit.textChanged.emit(self.OyMagLongitudeLineEdit.text())

        OyGeoModel = self.application_conf.get('ObservatoryMetadata', 'geomagnetic_model')
        self.OyModelLineEdit.setText(OyGeoModel)
        self.OyModelLineEdit.setEnabled(False)
        self.OyModelLineEdit.setToolTip('The GeomagneticModel used by the Observatory - Can not be changed!')
        OyModelLineEditRegexp = QtCore.QRegExp(constants.observatory_geomag_model)
        OyModelLineEditValidator = QtGui.QRegExpValidator(OyModelLineEditRegexp)
        self.OyModelLineEdit.setValidator(OyModelLineEditValidator)
        self.OyModelLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyModelLineEdit.textChanged.emit(self.OyModelLineEdit.text())

        OyLat = self.application_conf.get('ObservatoryMetadata', 'latitude')
        self.OyLatitudeLineEdit.setText(OyLat)
        self.OyLatitudeLineEdit.setToolTip('The Latitude of the Framework (North is positive)  -89:59:59.9999 to '
                                           '+00:00:00.0000 to +89:59:59.9999')
        OyLatitudeLineEditRegexp = QtCore.QRegExp(constants.observatory_latitude)
        OyLatitudeLineEditValidator = QtGui.QRegExpValidator(OyLatitudeLineEditRegexp)
        self.OyLatitudeLineEdit.setValidator(OyLatitudeLineEditValidator)
        self.OyLatitudeLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyLatitudeLineEdit.textChanged.emit(self.OyLatitudeLineEdit.text())

        OyLong = self.application_conf.get('ObservatoryMetadata', 'longitude')
        self.OyLongitudeLineEdit.setText(OyLong)
        self.OyLongitudeLineEdit.setToolTip('The Longitude of the Observatory (West is positive)  '
                                            '-179:59:59.9999 to +000:00:00.0000 to +179:59:59.999')
        OyLongitudeLineEditRegexp = QtCore.QRegExp(constants.observatory_longitude)
        OyLongitudeLineEditValidator = QtGui.QRegExpValidator(OyLongitudeLineEditRegexp)
        self.OyLongitudeLineEdit.setValidator(OyLongitudeLineEditValidator)
        self.OyLongitudeLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyLongitudeLineEdit.textChanged.emit(self.OyLongitudeLineEdit.text())

        OyHASL = self.application_conf.get('ObservatoryMetadata', 'hasl')
        self.OyHaslLineEdit.setText(OyHASL)
        self.OyHaslLineEdit.setToolTip('The observatory height above sea level.')
        OyHaslLineEditRegexp = QtCore.QRegExp(constants.observatory_hasl)
        OyHaslLineEditValidator = QtGui.QRegExpValidator(OyHaslLineEditRegexp)
        self.OyHaslLineEdit.setValidator(OyHaslLineEditValidator)
        self.OyHaslLineEdit.textChanged.connect(self.parameter_check_state)
        self.OyHaslLineEdit.textChanged.emit(self.OyHaslLineEdit.text())

        # Load Observer Metadata Tab.

        ObName = self.application_conf.get('ObserverMetadata', 'name')
        self.ObNameLineEdit.setText(ObName)
        self.ObNameLineEdit.setToolTip('The name of the Observer')
        ObNameLineEditRegexp = QtCore.QRegExp(constants.observer_name)
        ObNameLineEditValidator = QtGui.QRegExpValidator(ObNameLineEditRegexp)
        self.ObNameLineEdit.setValidator(ObNameLineEditValidator)
        self.ObNameLineEdit.textChanged.connect(self.parameter_check_state)
        self.ObNameLineEdit.textChanged.emit(self.ObNameLineEdit.text())

        ObDescription = self.application_conf.get('ObserverMetadata', 'description')
        self.ObDescriptionLineEdit.setText(ObDescription)
        self.ObDescriptionLineEdit.setToolTip('The description of the Observer')
        ObDescriptionLineEditRegexp = QtCore.QRegExp(constants.observer_description)
        ObDescriptionLineEditValidator = QtGui.QRegExpValidator(ObDescriptionLineEditRegexp)
        self.ObDescriptionLineEdit.setValidator(ObDescriptionLineEditValidator)
        self.ObDescriptionLineEdit.textChanged.connect(self.parameter_check_state)
        self.ObDescriptionLineEdit.textChanged.emit(self.ObDescriptionLineEdit.text())

        ObEmail = self.application_conf.get('ObserverMetadata', 'contact_email')
        self.ObEmailLineEdit.setText(ObEmail)
        self.ObEmailLineEdit.setToolTip('The email address of the Observer')
        ObEmailLineEditRegexp = QtCore.QRegExp(constants.observer_email)
        ObEmailLineEditValidator = QtGui.QRegExpValidator(ObEmailLineEditRegexp)
        self.ObEmailLineEdit.setValidator(ObEmailLineEditValidator)
        self.ObEmailLineEdit.textChanged.connect(self.parameter_check_state)
        self.ObEmailLineEdit.textChanged.emit(self.ObEmailLineEdit.text())

        ObTelephone = self.application_conf.get('ObserverMetadata', 'contact_telephone')
        self.ObTelephoneLineEdit.setText(ObTelephone)
        self.ObTelephoneLineEdit.setToolTip('The Observer telephone number')
        ObTelephoneLineEditRegexp = QtCore.QRegExp(constants.observer_telephone)
        ObTelephoneLineEditValidator = QtGui.QRegExpValidator(ObTelephoneLineEditRegexp)
        self.ObTelephoneLineEdit.setValidator(ObTelephoneLineEditValidator)
        self.ObTelephoneLineEdit.textChanged.connect(self.parameter_check_state)
        self.ObTelephoneLineEdit.textChanged.emit(self.ObTelephoneLineEdit.text())

        ObURL = self.application_conf.get('ObserverMetadata', 'contact_url')
        self.ObUrlLineEdit.setText(ObURL)
        self.ObUrlLineEdit.setToolTip('The Observer website URL')
        ObUrlLineEditRegexp = QtCore.QRegExp(constants.observer_url)
        ObUrlLineEditValidator = QtGui.QRegExpValidator(ObUrlLineEditRegexp)
        self.ObUrlLineEdit.setValidator(ObUrlLineEditValidator)
        self.ObUrlLineEdit.textChanged.connect(self.parameter_check_state)
        self.ObUrlLineEdit.textChanged.emit(self.ObUrlLineEdit.text())

        ObCountry = self.application_conf.get('ObserverMetadata', 'country')
        self.ObCountryLineEdit.setText(ObCountry)
        self.ObCountryLineEdit.setToolTip('The two character Country containing the Observatory (ISO 3166)\n'
                                          'Country Codes: https://www.iso.org/obp/ui/#search/code/')
        ObCountryLineEditRegexp = QtCore.QRegExp(constants.observer_country)
        ObCountryLineEditValidator = QtGui.QRegExpValidator(ObCountryLineEditRegexp)
        self.ObCountryLineEdit.setValidator(ObCountryLineEditValidator)
        self.ObCountryLineEdit.textChanged.connect(self.parameter_check_state)
        self.ObCountryLineEdit.textChanged.emit(self.ObCountryLineEdit.text())

        ObNotes = self.application_conf.get('ObserverMetadata', 'notes')
        self.ObNotesLineEdit.setText(ObNotes)
        self.ObNotesLineEdit.setToolTip('The Observer Notes')
        ObNotesLineEditRegexp = QtCore.QRegExp(constants.observer_notes)
        ObNotesLineEditValidator = QtGui.QRegExpValidator(ObNotesLineEditRegexp)
        self.ObNotesLineEdit.setValidator(ObNotesLineEditValidator)
        self.ObNotesLineEdit.textChanged.connect(self.parameter_check_state)
        self.ObNotesLineEdit.textChanged.emit(self.ObNotesLineEdit.text())

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

    def instrument_port_checkbox_triggered(self):
        if self.detectInstrumentPortCheckBox.checkState():
            self.serialPortLineEdit.setEnabled(False)
        else:
            self.serialPortLineEdit.setEnabled(True)

    def baudrate_checkbox_triggered(self):
        if self.baudrateDefaultCheckBox.checkState():
            self.baudrateComboBox.setEnabled(False)
            self.baudrateComboBox.setCurrentIndex(self.baudrates.index('57600'))
        else:
            self.baudrateComboBox.setEnabled(True)

    def timeout_checkbox_triggered(self):
        if self.serialPortTimeoutCheckBox.checkState():
            self.timeoutComboBox.setEnabled(False)
            self.timeoutComboBox.setCurrentIndex(self.timeouts.index('20'))
        else:
            self.timeoutComboBox.setEnabled(True)

    def relay_checkbox_triggered(self):
        if self.relayCheckBox.checkState():
            self.ipAddressLineEdit.setEnabled(True)
            self.portLineEdit.setEnabled(True)
        else:
            self.ipAddressLineEdit.setEnabled(False)
            self.portLineEdit.setEnabled(False)

    def s2s_checkbox_triggered(self):
        if self.S2SCheckBox.checkState():
            self.S2SIpAddressLineEdit.setEnabled(True)
            self.S2SPort.setEnabled(True)
        else:
            self.S2SIpAddressLineEdit.setEnabled(False)
            self.S2SPort.setEnabled(False)

    def save_triggered(self):

        # Application
        self.application_conf.set('Application', 'instrument_data_path', self.savepathLineEdit.text())

        self.application_conf.set('Application', 'instrument_identifier',
                                  self.instrumentComboBox.itemText(self.instrumentComboBox.currentIndex()))

        if self.detectInstrumentPortCheckBox.checkState():
            self.application_conf.set('Application', 'instrument_autodetect', 'True')
        else:
            self.application_conf.set('Application', 'instrument_autodetect', 'False')

        # Logging Level
        self.application_conf.set('logger_root', 'level', self.loglevelComboBox.itemText(
            self.loglevelComboBox.currentIndex()))

        # StaribusPort
        if self.serialPortLineEdit.text().startswith('No serial'):
            self.application_conf.set('StaribusPort', 'staribus_port', '')
        else:
            self.application_conf.set('StaribusPort', 'staribus_port', self.serialPortLineEdit.text())

        self.application_conf.set('StaribusPort', 'baudrate',
                                  self.baudrateComboBox.itemText(self.baudrateComboBox.currentIndex()))

        self.application_conf.set('StaribusPort', 'timeout',
                                  self.timeoutComboBox.itemText(self.timeoutComboBox.currentIndex()))

        # Staribus2Starinet
        if self.S2SCheckBox.checkState():
            self.application_conf.set('Staribus2Starinet', 'active', 'True')
        else:
            self.application_conf.set('Staribus2Starinet', 'active', 'False')

        self.application_conf.set('Staribus2Starinet', 'address', self.S2SIpAddressLineEdit.text())
        self.application_conf.set('Staribus2Starinet', 'starinet_port', self.S2SPort.text())

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
        
        self.response_message = 'SUCCESS', 'Configuration saved, please restart application.'

        self.close()

    def chooser_triggered(self):

        file = str(QtGui.QFileDialog.getExistingDirectory(QtGui.QFileDialog(), "Select Directory"))

        if len(file) == 0:
            pass
        else:
            self.savepathLineEdit.setText(file)

    def exit_triggered(self):
        self.response_message = 'ABORT', None
        self.close()
