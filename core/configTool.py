__author__ = 'mark'
import logging
import sys

from PyQt4 import QtGui, QtCore
from core.ui.configuration import Ui_ConfigurationDialog

from core.configLoader import confLoader
from core.xmlLoad import Instruments
import core.configToolRegex as configRegex

logger = logging.getLogger('core.configTool')


class configManager(QtGui.QDialog, Ui_ConfigurationDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        logger.info('Started')

        self.application_conf = confLoader()
        self.instruments = Instruments()
        
        self.loglevels = ['INFO', 'DEBUG']
        self.baudrates = ['9600', '57600', '115200']
        self.timeouts = ['20', '30', '40', '50', '60']

        # Setup signal for button box save
        self.cancelButton.clicked.connect(self.exit_triggered)
        self.saveButton.clicked.connect(self.save_triggered)

        self.load_ui()

    def load_ui(self):
        '''
        loads the ui with the current configuration from disk.
        '''

        # Load 'General' Tab

        data_save_path = self.application_conf.get('Application', 'save_path')
        instrument_name = self.application_conf.get('Application', 'instrument_name')
        loglevel = self.application_conf.get('logger_root', 'level')

        # Data save path show blank if set to None.
        if data_save_path == 'None':
            self.savepathLineEdit.setText('WARNING: Please set a path to save exported data too.')
        else:
            self.savepathLineEdit.setText(data_save_path)

        self.savepathLineEdit.setToolTip('The full path to where you wish to save your downloaded data.')

        # Set up instruments combo box.
        instruments = self.instruments.get_names()
        self.instrumentComboBox.addItems(instruments)
        self.instrumentComboBox.setCurrentIndex(instruments.index(instrument_name))

        # Set up log level combo box.
        
        self.loglevelComboBox.addItems(self.loglevels)
        self.loglevelComboBox.setCurrentIndex(self.loglevels.index(loglevel))

        #  Set Detect staribus port checkbox

        detect_staribus_port = self.application_conf.get('Application', 'detect_staribus_port')

        if detect_staribus_port == 'False':
            self.dectectInstrumentPortCheckBox.setChecked(False)
        elif detect_staribus_port == 'True':
            self.dectectInstrumentPortCheckBox.setChecked(True)
            self.serialPortLineEdit.setEnabled(False)  # Disable port entry box if auto detect is true.
        else:
            logger.warning('Unable to detect staribus port check state, setting to default \'False\'.')
            self.application_conf.set('Application', 'detect_staribus_port', 'False')
            self.dectectInstrumentPortCheckBox.setChecked(False)

        self.dectectInstrumentPortCheckBox.setToolTip('Will check each serial ports for the configured instrument'
                                                      '\nNote : The configured instrument must be attached.')

        # Set serial port name in entry box.
        port = self.application_conf.get('StaribusPort', 'port')
        self.serialPortLineEdit.setText(port)

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

        if timeout == '30':
            self.serialPortTimeoutCheckBox.setChecked(True)
            self.timeoutComboBox.setEnabled(False)

        self.serialPortTimeoutCheckBox.setToolTip('Sets the default Staribus port timeout to 30 seconds')

        self.timeoutComboBox.addItems(self.timeouts)
        self.timeoutComboBox.setCurrentIndex(self.timeouts.index(timeout))

        # Set starinetConnector (Relay) check box and line edits.
        starinetConnector_active = self.application_conf.get('StarinetConnector', 'active')

        if starinetConnector_active == 'True':
            self.relayCheckBox.setChecked(True)
        elif starinetConnector_active == 'False':
            self.ipAddressLineEdit.setEnabled(False)
            self.portLineEdit.setEnabled(False)

        starinetConnector_address = self.application_conf.get('StarinetConnector', 'address')
        # if len(starinetConnector_address) != 0:
        self.ipAddressLineEdit.setText(starinetConnector_address)
        self.ipAddressLineEdit.setToolTip('IPv4 Address only IPv6 not supported.')

        starinetConnector_port = self.application_conf.get('StarinetConnector', 'port')
        # if len(starinetConnector_port) != 0:
        self.portLineEdit.setText(starinetConnector_port)
        self.portLineEdit.setToolTip('Port can be in the range 1 - 65535, default is 1205')

        # Load Observatory Metadata Tab

        OyName = self.application_conf.get('ObservatoryMetadata', 'name')
        self.OyNameLineEdit.setText(OyName)
        self.OyNameLineEdit.setToolTip('The name of the Observatory')

        OyDescription = self.application_conf.get('ObservatoryMetadata', 'description')
        self.OyDescriptionLineEdit.setText(OyDescription)
        self.OyDescriptionLineEdit.setToolTip('The description of the Observatory')

        OyEmail = self.application_conf.get('ObservatoryMetadata', 'contact_email')
        self.OyEmailLineEdit.setText(OyEmail)
        self.OyEmailLineEdit.setToolTip('The email address of the Observatory')

        OyTelephone = self.application_conf.get('ObservatoryMetadata', 'contact_telephone')
        self.OyTelephoneLineEdit.setText(OyTelephone)
        self.OyTelephoneLineEdit.setToolTip('The telephone number of the Observatory')

        OyURL = self.application_conf.get('ObservatoryMetadata', 'contact_url')
        self.OyUrlLineEdit.setText(OyURL)
        self.OyUrlLineEdit.setToolTip('The Observatory website URL')

        OyCountry = self.application_conf.get('ObservatoryMetadata', 'country')
        self.OyCountryLineEdit.setText(OyCountry)
        self.OyCountryLineEdit.setToolTip('The two character Country containing the Observatory (ISO 3166)\n'
                                          'Country Codes: https://www.iso.org/obp/ui/#search/code/')

        OyTimezone = self.application_conf.get('ObservatoryMetadata', 'timezone')
        self.OyTimezoneLineEdit.setText(OyTimezone)
        self.OyTimezoneLineEdit.setToolTip('The TimeZone containing the Observatory  GMT-23:59 to GMT+00:00 '
                                           'to GMT+23:59 or UTC')

        OyDatum = self.application_conf.get('ObservatoryMetadata', 'geodetic_datum')
        self.OyDatumLineEdit.setText(OyDatum)
        self.OyDatumLineEdit.setEnabled(False)
        self.OyDatumLineEdit.setToolTip('The GeodeticDatum used by the Observatory - Can not be changed!')

        OyGeoLat = self.application_conf.get('ObservatoryMetadata', 'geomagnetic_latitude')
        self.OyMagLatitudeLineEdit.setText(OyGeoLat)
        self.OyMagLatitudeLineEdit.setToolTip('The GeomagneticLatitude of the Observatory (North is positive) '
                                              '-89:59:59.9999 to +00:00:00.0000 to +89:59:59.9999')

        OyGeoLong = self.application_conf.get('ObservatoryMetadata', 'geomagnetic_longitude')
        self.OyMagLongitudeLineEdit.setText(OyGeoLong)
        self.OyMagLongitudeLineEdit.setToolTip('The GeomagneticLongitude of the Observatory (West is positive)  '
                                               '-179:59:59.9999 to +000:00:00.0000 to +179:59:59.9999')

        OyGeoModel = self.application_conf.get('ObservatoryMetadata', 'geomagnetic_model')
        self.OyModelLineEdit.setText(OyGeoModel)
        self.OyModelLineEdit.setEnabled(False)
        self.OyModelLineEdit.setToolTip('The GeomagneticModel used by the Observatory - Can not be changed!')

        OyLat = self.application_conf.get('ObservatoryMetadata', 'latitude')
        self.OyLatitudeLineEdit.setText(OyLat)
        self.OyLatitudeLineEdit.setToolTip('The Latitude of the Framework (North is positive)  -89:59:59.9999 to '
                                           '+00:00:00.0000 to +89:59:59.9999')

        OyLong = self.application_conf.get('ObservatoryMetadata', 'longitude')
        self.OyLongitudeLineEdit.setText(OyLong)
        self.OyLongitudeLineEdit.setToolTip('The Longitude of the Observatory (West is positive)  '
                                            '-179:59:59.9999 to +000:00:00.0000 to +179:59:59.999')

        OyHASL = self.application_conf.get('ObservatoryMetadata', 'hasl')
        self.OyHaslLineEdit.setText(OyHASL)
        self.OyHaslLineEdit.setToolTip('The observatory height above sea level.')

        # Load Observer Metadata Tab.

        ObName = self.application_conf.get('ObserverMetadata', 'name')
        self.ObNameLineEdit.setText(ObName)
        self.ObNameLineEdit.setToolTip('The name of the Observer')

        ObDescription = self.application_conf.get('ObserverMetadata', 'description')
        self.ObDescriptionLineEdit.setText(ObDescription)
        self.ObDescriptionLineEdit.setToolTip('The description of the Observer')

        ObEmail = self.application_conf.get('ObserverMetadata', 'contact_email')
        self.ObEmailLineEdit.setText(ObEmail)
        self.ObEmailLineEdit.setToolTip('The email address of the Observer')

        ObTelephone = self.application_conf.get('ObserverMetadata', 'contact_telephone')
        self.ObTelephoneLineEdit.setText(ObTelephone)
        self.ObTelephoneLineEdit.setToolTip('The Observer telephone number')

        ObURL = self.application_conf.get('ObserverMetadata', 'contact_url')
        self.ObUrlLineEdit.setText(ObURL)
        self.ObUrlLineEdit.setToolTip('The Observer website URL')

        ObCountry = self.application_conf.get('ObserverMetadata', 'country')
        self.ObCountryLineEdit.setText(ObCountry)
        self.ObCountryLineEdit.setToolTip('The two character Country containing the Observatory (ISO 3166)\n'
                                          'Country Codes: https://www.iso.org/obp/ui/#search/code/')

        ObNotes = self.application_conf.get('ObserverMetadata', 'notes')
        self.ObNotesLineEdit.setText(ObNotes)
        self.ObNotesLineEdit.setToolTip('The Observer Notes')

    def save_triggered(self):
        print('Save triggered')

    def exit_triggered(self):
        self.close()
