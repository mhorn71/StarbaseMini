__author__ = 'mark'
import logging
from PyQt4 import QtGui, QtCore
from core.ui.configuration import Ui_ConfigurationDialog

from core.configLoader import confLoader
from core.xmlLoad import Instruments

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
        self.timeouts = ['10', '20', '30', '40', '50', '60']

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

        # Set serial port name in entry box.
        port = self.application_conf.get('StaribusPort', 'port')
        if len(port) != 0:
            self.serialPortLineEdit.setText(port)

        # Set baudrate check box and combo box.
        baudrate = self.application_conf.get('StaribusPort', 'baudrate')

        if baudrate == '57600':
            self.baudrateDefaultCheckBox.setChecked(True)
            self.baudrateComboBox.setEnabled(False)  # Disable combo box if default set.

        self.baudrateComboBox.addItems(self.baudrates)
        self.baudrateComboBox.setCurrentIndex(self.baudrates.index(baudrate))

        # Set timeout check box and combo box.
        timeout = self.application_conf.get('StaribusPort', 'timeout')

        if timeout == '30':
            self.serialPortTimeoutCheckBox.setChecked(True)
            self.timeoutComboBox.setEnabled(False)

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

        starinetConnector_port = self.application_conf.get('StarinetConnector', 'port')
        # if len(starinetConnector_port) != 0:
        self.portLineEdit.setText(starinetConnector_port)

        # Load Observatory Tab

        OyName = self.application_conf.get('ObservatoryMetadata', 'name')
        self.OyNameLineEdit.setText(OyName)

        OyDescription = self.application_conf.get('ObservatoryMetadata', 'description')
        self.OyDescriptionLineEdit.setText(OyDescription)

        OyEmail = self.application_conf.get('ObservatoryMetadata', 'contact_email')
        self.QyEmailLineEdit.setText(OyEmail)

        OyTelephone = self.application_conf.get('ObservatoryMetadata', 'contact_telephone')
        self.OyTelephoneLineEdit.setText(OyTelephone)

        OyURL = self.application_conf.get('ObservatoryMetadata', 'contact_url')
        self.OyUrlLineEdit.setText(OyURL)

        OyCountry = self.application_conf.get('ObservatoryMetadata', 'country')
        self.OyCountryLineEdit.setText(OyCountry)

        OyTimezone = self.application_conf.get('ObservatoryMetadata', 'timezone')
        self.OyTimezoneLineEdit.setText(OyTimezone)

        OyDatum = self.application_conf.get('ObservatoryMetadata', 'geodetic_datum')
        self.OyDatumLineEdit.setText(OyDatum)

        OyGeoLat = self.application_conf.get('ObservatoryMetadata', 'geomagnetic_latitude')
        self.OyMagLatitudeLineEdit.setText(OyGeoLat)

        OyGeoLong = self.application_conf.get('ObservatoryMetadata', 'geomagnetic_longitude')
        self.OyMagLongitudeLineEdit.setText(OyGeoLong)

        OyGeoModel = self.application_conf.get('ObservatoryMetadata', 'geomagnetic_model')
        self.OyModelLineEdit.setText(OyGeoModel)

        OyLat = self.application_conf.get('ObservatoryMetadata', 'latitude')
        self.OyLatitudeLineEdit.setText(OyLat)

        OyLong = self.application_conf.get('ObservatoryMetadata', 'longitude')
        self.OyLongitudeLineEdit.setText(OyLong)

        OyHASL = self.application_conf.get('ObservatoryMetadata', 'hasl')
        self.OyHaslLineEdit.setText(OyHASL)

    def exit_triggered(self):
        self.close()

    def save_triggered(self):
        print('Save triggered')
