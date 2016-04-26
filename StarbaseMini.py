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
import os
import logging.config
import logging
import datetime
import threading
import time

from PyQt4 import QtGui, QtCore

try:
    from PyQt4.QtCore import QString
except ImportError:
    QString = str

from ui import Ui_MainWindow
import utilities
import xml_utilities
import config_utilities
import starinet_connector
import interpreter
import constants
import datatranslators
import metadata
import charting
import instrument_attrib

version = '2.0.2'


class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):

        # Fatal error trip
        self.fatal_error = False
        self.config_error = False
        self.load_finish = False

        # Parameter / check state, regex parameter.
        self.parameter_regex = '^.*$'

        # DataBlock Boolean.
        self.DataBlockBool = False

        # Data from need so we know where the data is from
        self.data_from = None

        # Base attributes.
        self.saved_data_state = False

        # Disable UI boolean.
        self.disable_all_boolean = False

        # Instrument Attributes
        self.instrument = None
        self.instrument_file = None
        self.datatranslator = None
        self.metadata_creator = None
        self.metadata_deconstructor = None
        self.instrument_data_path = None
        self.starinet_relay_boolean = None
        self.starinet_address = None
        self.starinet_port = None
        self.instrument_autodetect_status_boolean = False
        self.command_interpreter = None
        self.configurationManager = None
        self.chart = None
        self.data_source = None
        self.starinet_relay_initialised = False

        # Initialise UI
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Menu items
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionConfiguration.triggered.connect(self.configuration_triggered)
        self.ui.actionInstrument_Attrib.triggered.connect(self.instrument_attrib_triggered)
        self.ui.actionAbout.triggered.connect(self.help_about_triggered)

        # Setup charting
        self.mplwindow = self.ui.mplwindow
        self.mplvl = self.ui.mplvl

        # Setup QTableWidget
        headers = ['DateTime', 'Identifier', 'Status', 'Units', 'ResponseValue']
        self.ui.statusMessage.setHorizontalHeaderLabels(headers)
        self.ui.statusMessage.setColumnWidth(0, 115)  # Datetime Column
        self.ui.statusMessage.setColumnWidth(1, 110)  # Ident Column
        self.ui.statusMessage.setColumnWidth(2, 182)  # Status Column
        self.ui.statusMessage.setColumnWidth(3, 56)  # Units Column
        self.ui.statusMessage.verticalHeader().setDefaultSectionSize(20)  # Sets the height of the rows.
        self.ui.statusMessage.horizontalHeader().setStretchLastSection(True)  # Expands section to widget width.
        self.statusMessageIndex = 0

        # Trip counters, these are so we ignore dict KeyError's when first populating which seems to differ
        # from one platform to another and I have no idea why.  Answers on a postcard please. ;-))
        self.ui_module_trip = 0
        self.ui_command_trip = 0
        self.chart_warning = 0
        self.command_parameter_trip = 0
        self.parameter_check_state_trip = 0

        # Setup initial channel button and checkbox states.
        self.ui.chartDecimateCheckBox.setEnabled(False)
        self.ui.chartAutoRangeCheckBox.setEnabled(False)
        self.ui.showLegend.setEnabled(False)
        self.ui.channel0Button.setVisible(False)
        self.ui.channel0colour.setVisible(False)
        self.ui.channel0colour.setEnabled(False)
        self.ui.channel1Button.setVisible(False)
        self.ui.channel1colour.setVisible(False)
        self.ui.channel1colour.setEnabled(False)
        self.ui.channel2Button.setVisible(False)
        self.ui.channel2colour.setVisible(False)
        self.ui.channel2colour.setEnabled(False)
        self.ui.channel3Button.setVisible(False)
        self.ui.channel3colour.setVisible(False)
        self.ui.channel3colour.setEnabled(False)
        self.ui.channel4Button.setVisible(False)
        self.ui.channel4colour.setVisible(False)
        self.ui.channel4colour.setEnabled(False)
        self.ui.channel5Button.setVisible(False)
        self.ui.channel5colour.setVisible(False)
        self.ui.channel5colour.setEnabled(False)
        self.ui.channel6Button.setVisible(False)
        self.ui.channel6colour.setVisible(False)
        self.ui.channel6colour.setEnabled(False)
        self.ui.channel7Button.setVisible(False)
        self.ui.channel7colour.setVisible(False)
        self.ui.channel7colour.setEnabled(False)
        self.ui.channel8Button.setVisible(False)
        self.ui.channel8colour.setVisible(False)
        self.ui.channel8colour.setEnabled(False)

        # Disable Parameter Entry, Choices Combobox and Execute Button
        self.ui.executeButton.setEnabled(False)
        self.ui.commandParameter.setEnabled(False)
        self.ui.choicesComboBox.setEnabled(False)

        # Button connectors
        self.ui.executeButton.clicked.connect(self.execute_triggered)
        self.ui.channel0Button.clicked.connect(self.channel0_triggered)
        self.ui.channel1Button.clicked.connect(self.channel1_triggered)
        self.ui.channel2Button.clicked.connect(self.channel2_triggered)
        self.ui.channel3Button.clicked.connect(self.channel3_triggered)
        self.ui.channel4Button.clicked.connect(self.channel4_triggered)
        self.ui.channel5Button.clicked.connect(self.channel5_triggered)
        self.ui.channel6Button.clicked.connect(self.channel6_triggered)
        self.ui.channel7Button.clicked.connect(self.channel7_triggered)
        self.ui.channel8Button.clicked.connect(self.channel8_triggered)

        # Module, Command and Choices ComboBox Triggers.
        self.ui.moduleCombobox.currentIndexChanged.connect(self.populate_ui_command)
        self.ui.commandCombobox.currentIndexChanged.connect(self.command_parameter_populate)

        # Parameter entry emit and connect signals
        self.ui.commandParameter.textChanged.connect(self.parameter_check_state)
        self.ui.commandParameter.textChanged.emit(self.ui.commandParameter.text())

        # Chart Decimate and AutoRange signals.
        self.ui.chartAutoRangeCheckBox.stateChanged.connect(self.chart_auto_range_triggered)
        self.ui.chartDecimateCheckBox.stateChanged.connect(self.chart_decimate_triggered)
        self.ui.showLegend.stateChanged.connect(self.chart_show_legend_triggered)

        # Initialise Command Interpreter Class
        self.command_interpreter = interpreter.CommandInterpreter()

        # Attempt at allowing configuration changes
        self.first_initialisation = True

        # Style sheets
        self.style_boolean = False

        if sys.platform.startswith('darwin'):
            self.stylesheet = 'css/macStyle.css'
            self.style_boolean = True
        elif sys.platform.startswith('win32'):
            self.stylesheet = 'css/winStyle.css'
            self.style_boolean = True
        elif sys.platform.startswith('linux'):
            self.stylesheet = 'css/nixStyle.css'
            self.style_boolean = True

        if self.style_boolean:
            with open(self.stylesheet, 'r') as style:
                self.setStyleSheet(style.read())

        self.setWindowIcon(QtGui.QIcon('images/starbase.png'))

        # Run instrument configuration initialisation.
        self.initialise_configuration()

    # Initialise configuration.
    def initialise_configuration(self):

        if self.starinet_relay_initialised is True:
            self.disable_all()
            self.status_message('system', 'INFO', 'Starinet relay is initialised please restart the application.', None)
        else:

            self.ui.moduleCombobox.clear()
            self.ui.commandCombobox.clear()

            try:
                self.config = config_utilities.ConfigLoader()
            except (FileNotFoundError, OSError, ValueError) as msg:
                msg = ('Configuration Tool : %s' % str(msg))
                self.status_message('system', 'CRITICAL_ERROR', str(msg), None)
                self.disable_all()
                self.fatal_error = True
                self.config_error = True
            else:
                # # Generate user configuration if it's missing.
                logging.config.fileConfig(self.config.conf_file, disable_existing_loggers=False)
                self.logger = logging.getLogger('main')

                if self.first_initialisation is True:
                    self.logger.info('**************************** APPLICATION STARTUP ****************************')

                # Enable all UI components.
                self.enable_all()

                # Load application parameters.
                try:
                    self.instrument_identifier = self.config.get('Application', 'instrument_identifier')
                    self.logger.info('############################## Initialising ' + self.instrument_identifier +
                                     ' ##############################')
                    self.instrument_data_path = self.config.get('Application', 'instrument_data_path')
                    self.starinet_relay_boolean = self.config.get('StarinetRelay', 'active')
                    self.starinet_address = self.config.get('StarinetRelay', 'address')
                    self.starinet_port = self.config.get('StarinetRelay', 'starinet_port')
                    self.staribus2starinet_relay_boolean = self.config.get('Staribus2Starinet', 'active')
                    self.staribus2starinet_address = self.config.get('Staribus2Starinet', 'address')
                    self.staribus2starinet_port = self.config.get('Staribus2Starinet', 'starinet_port')
                except (ValueError, KeyError, ValueError) as msg:
                    self.logger.critical('Configuration ValueError : %s' % str(msg))
                    msg = ('Configuration ValueError : %s exiting.' % str(msg))
                    self.fatal_error = True
                    self.status_message('system', 'CRITICAL_ERROR', str(msg), None)
                else:
                    self.logger.info('Instrument Identifier : %s' % self.instrument_identifier)
                    self.logger.info('Initial parameter for instrument_data_path : %s' % self.instrument_data_path)
                    self.logger.info('Initial parameter for starinet_relay_boolean : %s' % self.starinet_relay_boolean)
                    self.logger.info('Initial parameter for starinet_relay_address : %s' % self.starinet_address)
                    self.logger.info('Initial parameter for starinet_relay_port : %s' % self.starinet_port)
                    self.logger.info('Initial parameter for staribus2starinet_relay_boolean : %s' %
                                     self.staribus2starinet_relay_boolean)
                    self.logger.info('Initial parameter for staribus2starinet_relay_address : %s' %
                                     self.staribus2starinet_address)
                    self.logger.info('Initial parameter for staribus2starinet_relay_port : %s' %
                                     self.staribus2starinet_port)

                    # Initialise configurationManager & charting.
                    if self.config_error is False:
                        self.configurationManager = config_utilities.ConfigManager()

                if self.fatal_error is False:
                    self.instrument_loader()


                if self.fatal_error is False:
                    self.datatranslator_loader()

                # Initialise charting.
                if self.config_error is False:
                    self.chart_loader()

                if self.fatal_error is False and self.config_error is False:
                    # Initialise command interpreter
                    self.instrument_interpreter_loader()
                    # Fire populate_ui_module for the first time.
                    self.populate_ui_module()

                    self.load_finish = True

            self.instrument_attributes = instrument_attrib.InstrumentAttrib()

            if self.first_initialisation is True:

                upgrade = utilities.Upgrader()

                message = upgrade.detect_upgrade(version)

                # This is just a trial to workout how to add menu items that are checkable
                # http://stackoverflow.com/questions/20019489/pyside-adding-a-toggle-option-action-to-the-menu-bar
                # See also
                # http://stackoverflow.com/questions/1100775/create-pyqt-menu-from-a-list-of-strings

                action = QtGui.QActionGroup(self.ui.menuInstrument, exclusive=True)

                for item in self.configurationManager.instruments.get_names():
                    ag = QtGui.QAction(item, action, checkable=True)

                    if self.config.get('Application', 'instrument_identifier') == item:
                        ag.setChecked(True)
                        self.instrument_item = item

                    self.ui.menuInstrument.addAction(ag)
                    self.connect(ag, QtCore.SIGNAL('triggered()'), lambda item=item: self.instrument_selection(item))

                if message is not None:
                    self.status_message('system', message[0], message[1], None)

                self.first_initialisation = False

    def instrument_selection(self, item):

        if self.data_source == 'instrument':
            if self.saved_data_state is not False:

                message = 'WARNING:  You have unsaved data.\n\nIf you change the instrument, ' + \
                          'you will be able to save the unsaved data!\n\nDo you want to change instruments?'
                header = 'HELLO'

                result = QtGui.QMessageBox.question(None,
                                                    header,
                                                    message,
                                                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

                if result == QtGui.QMessageBox.Yes:
                    self.datatranslator.clear()
                    self.saved_data_state = False
                    self.config.set('Application', 'instrument_identifier', item)
                    self.initialise_configuration()
                    self.instrument_item = item
                    self.ui.chartDecimateCheckBox.setEnabled(False)
                    self.ui.chartAutoRangeCheckBox.setEnabled(False)
                    self.ui.showLegend.setEnabled(False)
                else:
                    for action in self.ui.menuInstrument.actions():
                        if action.text() == self.instrument_item:
                            action.setChecked(True)


        else:
            self.config.set('Application', 'instrument_identifier', item)
            self.initialise_configuration()
            self.instrument_item = item


    # ----------------------------------------
    # Instrument loader method.
    # ----------------------------------------

    def instrument_loader(self):

        instrument_found = False

        sep = os.path.sep

        instruments_local_home = os.path.expanduser('~') + sep + '.starbasemini' + sep + 'instruments' + sep

        instruments_local = instruments_local_home + 'instruments.xml'

        instruments_system_home = 'instruments' + os.path.sep

        instruments_system = instruments_system_home + 'instruments.xml'

        # First see if we have a local instrument.
        try:
            my_instruments = xml_utilities.Instruments(instruments_local)
        except (FileNotFoundError, ValueError, LookupError, AttributeError):
            self.logger.info('No instruments found in user home location')
        else:
            try:
                filename = my_instruments.get_filename(self.instrument_identifier)
                filename = instruments_local_home + filename
                self.instrument = xml_utilities.Instrument(filename)
                self.instrument_file = filename
            except (FileNotFoundError, ValueError, LookupError, AttributeError, UnboundLocalError) as msg:
                self.logger.info('Instrument not found in user home location')
            else:
                instrument_found = True

        if instrument_found is not True:
            # Load set instrument XML, selectedInstrument returns the relative path and XML file name.
            try:
                my_instruments = xml_utilities.Instruments(instruments_system)
            except (FileNotFoundError, ValueError, LookupError, AttributeError) as msg:
                self.fatal_error = True
                self.logger.critical('Unable to load instruments.xml %s' % str(msg))
                self.status_message('system', 'CRITICAL_ERROR', str(msg), None)
            else:
                try:
                    filename = my_instruments.get_filename(self.instrument_identifier)
                    filename_local = instruments_local_home + filename
                    filename_system = instruments_system_home + filename

                    if os.path.isfile(filename_local):
                        self.instrument = xml_utilities.Instrument(filename_local)
                        file = filename_local
                        self.instrument_file = filename_local
                    else:
                        self.instrument = xml_utilities.Instrument(filename_system)
                        file = filename_system
                        self.instrument_file = filename_system
                except (FileNotFoundError, ValueError, LookupError, AttributeError) as msg:
                    self.logger.critical('Unable to load instrument xml %s' % str(msg))
                    self.fatal_error = True
                    self.status_message('system', 'CRITICAL_ERROR', str(msg), None)
                else:
                    self.logger.debug('Instrument XML found at : %s' % file)
                    self.logger.info('Instrument XML loaded for : %s', self.instrument_identifier)

        if self.instrument is not None:
            if self.instrument.instrument_staribus_autodetect == 'True' and self.staribus2starinet_relay_boolean == 'False':
                self.instrument_autodetector()

        # Setup StarinetConnector if enabled.
        if self.starinet_relay_boolean == 'True':
            self.starinet_relay_initialised = True
            self.starinet_connector_loader()
            self.ui.menuInstrument.setEnabled(False)
        else:
            self.ui.menuInstrument.setEnabled(True)


    # ----------------------------------------
    # Datatranslator loader method.
    # ----------------------------------------

    def datatranslator_loader(self):
        # Initialise datatranslator, added new datatranslators here.
        if self.instrument.instrument_datatranslator == 'StaribusBlock':
            self.datatranslator = datatranslators.StaribusParser(self.instrument.instrument_number_of_channels)
            # Initialise metadata
            self.metadata_deconstructor = metadata.StaribusMetaDataDeconstructor()
            self.metadata_creator = metadata.StaribusMetaDataCreator(self)
        else:
            self.logger.critical('Unable to locate Instrument DataTranslator')
            self.status_message('system', 'CRITICAL_ERROR', 'Unable to locate Instrument DataTranslator', None)
            self.fatal_error = True

    # ----------------------------------------
    # Instrument interpreter loader method.
    # ----------------------------------------

    def instrument_interpreter_loader(self):
        # Initialise Command Interpreter
        try:
            if self.starinet_relay_boolean == 'False':
                if self.instrument.instrument_starinet_address != 'None':
                    self.logger.debug('Main Starinet Routine being run')
                    self.logger.info('Initialising Command Interpreter for Starinet')
                    self.command_interpreter.start(self)
                    message = ('Initialised Starinet Instrument : %s ' % self.instrument_identifier)
                    self.status_message('system', 'INFO', message, None)
                elif self.instrument.instrument_staribus_address != 'None':
                    if self.staribus2starinet_relay_boolean == 'True':
                        self.logger.debug('Main Staribus 2 Starinet Routine being run')
                        self.logger.info('Initialising Command Interpreter for Staribus2Starinet')
                        message = ('Initialised Staribus2Starinet Instrument : %s ' % self.instrument_identifier)
                        self.status_message('system', 'INFO', message, None)
                        self.command_interpreter.start(self)
                    else:
                        self.logger.debug('Main Staribus Routine being run')
                        self.command_interpreter.close()

                        if utilities.check_serial_port(self.instrument.instrument_staribus_port):
                            self.logger.debug('Main Staribus check_serial Routine success')
                            self.logger.info('Initialising Command Interpreter for Staribus')
                            self.command_interpreter.start(self)
                            message = ('Initialised Staribus Instrument : %s ' % self.instrument_identifier)
                            self.status_message('system', 'INFO', message, None)
                        else:
                            self.logger.debug('Main Staribus check_serial Routine failure')
                            self.disable_all()
                            message = ('Initialised Staribus Instrument : %s ' % self.instrument_identifier)
                            self.status_message('system', 'INFO', message, None)
                            self.status_message('system', 'WARNING',
                                                'Unable to open serial port - UI controls disabled.', None)
                else:
                    self.logger.critical('Unable able to determine stream type.')
                    self.status_message('system', 'ERROR',
                                        'Unable able to determine stream type - UI controls disabled.', None)
                    self.disable_all()
        except (TypeError, IOError) as msg:
            self.logger.critical(str(msg))
            message = str(msg) + ' - UI controls disabled.'
            self.status_message('system', 'CRITICAL_ERROR', message, None)
            self.disable_all()

    # ----------------------------------------
    # Instrument autodetect method.
    # ----------------------------------------

    def instrument_autodetector(self):
        self.logger.info('Instrument autodetect is True.')
        if self.instrument.instrument_starinet_address != 'None':
            self.logger.info('Instrument autodetect true however instrument appears to be Starinet.')
            self.instrument_autodetect_status_boolean = False
        else:
            ports = utilities.serial_port_scanner()
            if ports is None:
                self.logger.warning('No serial ports found to scan for instrument.')
                self.instrument_autodetect_status_boolean = False
            else:
                instrument_port = utilities.check_serial_port_staribus_instrument(
                    self.instrument.instrument_staribus_address, ports, self.instrument.instrument_staribus_baudrate)
                if instrument_port is None:
                    self.logger.warning('Staribus instrument not found for address %s' %
                                        self.instrument.instrument_staribus_address)
                    self.instrument_autodetect_status_boolean = False
                elif len(instrument_port) > 1:
                    self.logger.warning('Multiple Staribus instruments found defaulting to first.')
                    self.status_message('system', 'WARNING',
                                        'Multiple Staribus instruments found defaulting to first.', None)
                    self.logger.info('Setting serial port to %s' % instrument_port[0])
                    self.instrument.instrument_staribus_port = instrument_port[0]
                    self.instrument_autodetect_status_boolean = True
                else:
                    self.status_message('system', 'INFO',  ('%s instrument found.' %
                                                            self.instrument.instrument_identifier), None)
                    self.logger.info('Setting serial port to %s' % instrument_port[0])
                    self.instrument.instrument_staribus_port = instrument_port[0]
                    self.instrument_autodetect_status_boolean = True

    # ----------------------------------------
    # Starinet connector loader method.
    # ----------------------------------------

    def starinet_connector_loader(self):
        if self.command_interpreter is not None:
            self.command_interpreter.close()

        if self.instrument.instrument_staribus_autodetect == 'True':
            self.instrument_autodetector()

            if self.instrument_autodetect_status_boolean:
                self.disable_all()
                starinet_connector.StarinetConnectorStart(self.starinet_address, self.starinet_port, self.instrument.instrument_staribus_port,
                                                          self.instrument.instrument_staribus_baudrate, self.instrument.instrument_staribus_timeout)
                self.logger.info('Starinet relay initialised.')
                msg = 'Starinet relay initialised.'
                self.status_message('system', 'INFO', msg, None)
            else:
                self.disable_all()
                self.logger.critical('Starinet relay cannot initialise no instrument found.')
                msg = 'Starinet relay cannot initialise no instrument found.'
                self.status_message('system', 'ERROR', msg, None)
        else:
            if self.instrument.instrument_staribus_port is None:
                self.disable_all()
                self.logger.critical('Starinet relay cannot initialise as serial port isn\'t set.')
                msg = 'Starinet relay cannot initialise as serial port isn\'t set.'
                self.status_message('system', 'ERROR', msg, None)
            else:
                self.disable_all()
                starinet_connector.StarinetConnectorStart(self.starinet_address, self.starinet_port, self.instrument.instrument_staribus_port,
                                                          self.instrument.instrument_staribus_baudrate, self.instrument.instrument_staribus_timeout)
                self.logger.info('Starinet relay initialised.')
                msg = 'Starinet relay initialised.'
                self.status_message('system', 'INFO', msg, None)

    # ----------------------------------------
    # Chart loader method.
    # ----------------------------------------

    def chart_loader(self):
        if self.first_initialisation is True:
            try:
                self.chart = charting.Chart(self.ui, self.config)
                self.chart.chart_instrument_setup(self.datatranslator, self.instrument, self.metadata_deconstructor)
            except Exception as msg:
                # msg = ('Charting failed to initialise - %s' % str(msg))
                self.logger.critical(str(msg))
                self.status_message('system', 'CRITICAL_ERROR', str(msg), None)
        else:
            try:
                self.chart.chart_instrument_setup(self.datatranslator, self.instrument, self.metadata_deconstructor)
            except Exception as msg:
                # msg = ('Charting failed to initialise - %s' % str(msg))
                self.logger.critical(str(msg))
                self.status_message('system', 'CRITICAL_ERROR', str(msg), None)

    # ----------------------------------------
    # Disable ui controls method.
    # ----------------------------------------

    def disable_all(self):
        self.disable_all_boolean = True
        self.logger.info('Instrument control panel disabled.')
        # self.status_message('system', 'INFO', 'Instrument control panel disabled', None)
        self.ui.moduleCombobox.setEnabled(False)
        self.logger.debug('Module Combo box set False')
        self.ui.commandCombobox.setEnabled(False)
        self.logger.debug('Command Combo box set False')
        self.ui.commandParameter.setEnabled(False)
        self.logger.debug('Parameter Combo box set False')
        self.ui.choicesComboBox.setEnabled(False)
        self.logger.debug('Choices Combo box set False')
        self.ui.executeButton.setEnabled(False)
        self.logger.debug('Execute Button set False')

    def enable_all(self):
        self.disable_all_boolean = False
        self.logger.info('Instrument control panel enabled.')
        # self.status_message('system', 'INFO', 'Instrument control panel disabled', None)
        self.ui.moduleCombobox.setEnabled(True)
        self.logger.debug('Module Combo box set True')
        self.ui.commandCombobox.setEnabled(True)
        self.logger.debug('Command Combo box set True')
        self.ui.commandParameter.setEnabled(True)
        self.logger.debug('Parameter Combo box set True')
        self.ui.choicesComboBox.setEnabled(True)
        self.logger.debug('Choices Combo box set True')
        self.ui.executeButton.setEnabled(True)
        self.logger.debug('Execute Button set True')

    # ----------------------------------------
    # Status Message method.
    # ----------------------------------------

    def status_message(self, ident, status, response_value, units):

        self.logger.info('################### ' + str(ident) + ' ' + str(status) + ' ' + str(response_value) +
                         ' ###################')

        dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.ui.statusMessage.insertRow(self.statusMessageIndex)

        self.ui.statusMessage.setItem(self.statusMessageIndex, 0, QtGui.QTableWidgetItem(dateTime))

        if ident is not None:
            self.ui.statusMessage.setItem(self.statusMessageIndex, 1, QtGui.QTableWidgetItem(ident))

        if status is not None:
            self.ui.statusMessage.setItem(self.statusMessageIndex, 2, QtGui.QTableWidgetItem(status))

        if units is not None:
            self.ui.statusMessage.setItem(self.statusMessageIndex, 3, QtGui.QTableWidgetItem(units))

        if response_value is not None:
            response_value = response_value.replace(constants.RS, '  ')
            self.ui.statusMessage.setItem(self.statusMessageIndex, 4, QtGui.QTableWidgetItem(response_value))

        #  Make sure the last item set is visible.
        self.ui.statusMessage.scrollToBottom()

        self.statusMessageIndex += 1

    # ----------------------------------------
    # For here on is the UI populate methods.
    # ----------------------------------------

    def populate_ui_module(self):
        self.ui_module_trip = 0
        try:
            # populate module combobox.
            self.logger.debug('Populating module combobox')

            index = 0

            for plugin in self.instrument.module_list:
                self.logger.debug('Populate module combobox with : %s' % str(plugin))
                self.ui.moduleCombobox.addItem(plugin[0], plugin[2])
                self.ui.moduleCombobox.setItemData(index, plugin[1], QtCore.Qt.ToolTipRole)

                index += 1
        except KeyError as msg:
            if self.ui_module_trip == 0:
                self.logger.warning('First Run ignore KeyError : populate_ui_module : %s' % str(msg))
            else:
                self.logger.critical('Populate UI Module KeyError. %s' % str(msg))
                self.status_message('system', 'ERROR', ('Populate UI Module KeyError. %s' % str(msg)), None)
        else:
            self.ui_module_trip += 1

    def populate_ui_command(self):
        self.ui_command_trip = 0
        try:
            self.logger.debug('Populating command combobox.')
            plugin_index = self.ui.moduleCombobox.currentIndex()

            self.ui.commandCombobox.clear()

            index = 0

            for cmd in self.instrument.command_list[plugin_index]:
                self.logger.debug('Populate command combobox with : %s' % str(cmd))
                self.ui.commandCombobox.addItem(cmd[0], cmd[2])
                self.ui.commandCombobox.setItemData(index, cmd[1], QtCore.Qt.ToolTipRole)

                index += 1
        except KeyError as msg:
            if self.ui_command_trip == 0:
                self.logger.warning('First Run ignore KeyError : populate_ui_command : %s' % str(msg))
            else:
                self.logger.critical('Populate UI Command KeyError : %s' % str(msg))
                self.status_message('system', 'ERROR', ('Populate UI Command KeyError : %s' % str(msg)), None)
        else:
            self.ui_command_trip += 1

    # Get the command parameters for the current set command.
    def command_parameter_populate(self):
        self.command_parameter_trip = 0
        self.ui.commandParameter.clear()

        try:
            for command in self.instrument.command_dict[self.ui.moduleCombobox.itemData(self.ui.moduleCombobox.currentIndex())]:
                for key in command.keys():
                    if key == self.ui.commandCombobox.itemData(self.ui.commandCombobox.currentIndex()):
                        try:
                            # Check if command has choices.
                            if command[key]['Parameters']['Choices'] == 'None':
                                self.logger.debug('%s %s', self.ui.commandCombobox.currentText(), 'Parameters Choices : None')
                                self.ui.choicesComboBox.clear()
                                self.ui.choicesComboBox.setEnabled(False)

                                if self.disable_all_boolean is False:
                                    self.ui.executeButton.setEnabled(True)
                            else:
                                self.ui.choicesComboBox.clear()

                                if self.disable_all_boolean is False:
                                    self.ui.choicesComboBox.setEnabled(True)
                                    self.ui.executeButton.setEnabled(True)

                                # Split the choices up into list.
                                choices = command[key]['Parameters']['Choices'].split(',')
                                self.logger.debug('%s %s %s', self.ui.commandCombobox.currentText(), 'Parameters Choices :',
                                                  str(choices))
                                self.ui.choicesComboBox.addItems(choices)  # Add choices to combobox.

                                # Add choices tool tips to combo box.
                                for i in range(len(choices)):
                                    self.ui.choicesComboBox.setItemData(i, (command[key]['Parameters']['Tooltip']),
                                                                        QtCore.Qt.ToolTipRole)

                            # Check if command has parameters.
                            if command[key]['Parameters']['Regex'] == 'None':
                                self.logger.debug('%s %s', self.ui.commandCombobox.currentText(), 'Parameters Regex : None')
                                self.ui.commandParameter.clear()
                                self.ui.commandParameter.setEnabled(False)
                                self.ui.commandParameter.setStyleSheet('QLineEdit { background-color: #EBEBEB }')
                            else:
                                self.ui.commandParameter.setStyleSheet('QLineEdit { background-color: #FFFFFF }')

                                if self.disable_all_boolean is False:
                                    self.ui.commandParameter.setEnabled(True)
                                    self.ui.executeButton.setEnabled(False)

                                self.ui.commandParameter.setToolTip(command[key]['Parameters']['Tooltip'])
                                self.parameter_regex = command[key]['Parameters']['Regex']

                                self.logger.debug('%s %s %s', self.ui.commandCombobox.currentText(), 'Parameters Regex :',
                                                  self.parameter_regex)

                                regexp = QtCore.QRegExp(self.parameter_regex)
                                validator = QtGui.QRegExpValidator(regexp)
                                self.ui.commandParameter.setValidator(validator)
                        except KeyError as msg:
                            if self.command_parameter_trip == 0:
                                self.logger.warning('First Run ignore KeyError : command populate parameters : %s' % str(msg))
                            else:
                                self.logger.critical('ERROR : Command Parameter Populate KeyError : %s' % str(msg))
                                self.status_message('system', 'ERROR', ('Command Parameter KeyError : %s' % str(msg)), None)
                        else:
                            self.command_parameter_trip += 1
        except KeyError:
            pass

    def chart_control_panel(self, number_of_channels, translated):

        self.ui.showLegend.setEnabled(True)

        self.ui.channel0Button.setVisible(False)
        self.ui.channel0colour.setVisible(False)
        self.ui.channel1Button.setVisible(False)
        self.ui.channel1colour.setVisible(False)
        self.ui.channel2Button.setVisible(False)
        self.ui.channel2colour.setVisible(False)
        self.ui.channel3Button.setVisible(False)
        self.ui.channel3colour.setVisible(False)
        self.ui.channel4Button.setVisible(False)
        self.ui.channel4colour.setVisible(False)
        self.ui.channel5Button.setVisible(False)
        self.ui.channel5colour.setVisible(False)
        self.ui.channel6Button.setVisible(False)
        self.ui.channel6colour.setVisible(False)
        self.ui.channel7Button.setVisible(False)
        self.ui.channel7colour.setVisible(False)
        self.ui.channel8Button.setVisible(False)
        self.ui.channel8colour.setVisible(False)

        if number_of_channels == '1':
            self.ui.channel0Button.setEnabled(True)
            self.ui.channel0Button.setChecked(True)
            self.ui.channel0colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[0] + '; }')
            self.ui.channel0Button.setText(translated.channel_names[0])
            self.ui.channel0Button.setVisible(True)
            self.ui.channel0colour.setVisible(True)
            self.ui.channel1Button.setVisible(False)
            self.ui.channel1colour.setVisible(False)
            self.ui.channel2Button.setVisible(False)
            self.ui.channel2colour.setVisible(False)
            self.ui.channel3Button.setVisible(False)
            self.ui.channel3colour.setVisible(False)
            self.ui.channel4Button.setVisible(False)
            self.ui.channel4colour.setVisible(False)
            self.ui.channel5Button.setVisible(False)
            self.ui.channel5colour.setVisible(False)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel6colour.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel7colour.setVisible(False)
            self.ui.channel8Button.setVisible(False)
            self.ui.channel8colour.setVisible(False)
        elif number_of_channels == '2':
            self.ui.channel0Button.setEnabled(True)
            self.ui.channel0Button.setChecked(True)
            self.ui.channel0colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[0] + '; }')
            self.ui.channel1Button.setEnabled(True)
            self.ui.channel1Button.setChecked(True)
            self.ui.channel1colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[1] + '; }')
            self.ui.channel0Button.setText(translated.channel_names[0])
            self.ui.channel1Button.setText(translated.channel_names[1])
            self.ui.channel0Button.setVisible(True)
            self.ui.channel0colour.setVisible(True)
            self.ui.channel1Button.setVisible(True)
            self.ui.channel1colour.setVisible(True)
            self.ui.channel2Button.setVisible(False)
            self.ui.channel2colour.setVisible(False)
            self.ui.channel3Button.setVisible(False)
            self.ui.channel3colour.setVisible(False)
            self.ui.channel4Button.setVisible(False)
            self.ui.channel4colour.setVisible(False)
            self.ui.channel5Button.setVisible(False)
            self.ui.channel5colour.setVisible(False)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel6colour.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel7colour.setVisible(False)
            self.ui.channel8Button.setVisible(False)
            self.ui.channel8colour.setVisible(False)
        elif number_of_channels == '3':
            self.ui.channel0Button.setEnabled(True)
            self.ui.channel0Button.setChecked(True)
            self.ui.channel0colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[0] + '; }')
            self.ui.channel1Button.setEnabled(True)
            self.ui.channel1Button.setChecked(True)
            self.ui.channel1colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[1] + '; }')
            self.ui.channel2Button.setEnabled(True)
            self.ui.channel2Button.setChecked(True)
            self.ui.channel2colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[2] + '; }')
            self.ui.channel0Button.setText(translated.channel_names[0])
            self.ui.channel1Button.setText(translated.channel_names[1])
            self.ui.channel2Button.setText(translated.channel_names[2])
            self.ui.channel0Button.setVisible(True)
            self.ui.channel0colour.setVisible(True)
            self.ui.channel1Button.setVisible(True)
            self.ui.channel1colour.setVisible(True)
            self.ui.channel2Button.setVisible(True)
            self.ui.channel2colour.setVisible(True)
            self.ui.channel3Button.setVisible(False)
            self.ui.channel3colour.setVisible(False)
            self.ui.channel4Button.setVisible(False)
            self.ui.channel4colour.setVisible(False)
            self.ui.channel5Button.setVisible(False)
            self.ui.channel5colour.setVisible(False)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel6colour.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel7colour.setVisible(False)
            self.ui.channel8Button.setVisible(False)
            self.ui.channel8colour.setVisible(False)
        elif number_of_channels == '4':
            self.ui.channel0Button.setEnabled(True)
            self.ui.channel0Button.setChecked(True)
            self.ui.channel0colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[0] + '; }')
            self.ui.channel1Button.setEnabled(True)
            self.ui.channel1Button.setChecked(True)
            self.ui.channel1colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[1] + '; }')
            self.ui.channel2Button.setEnabled(True)
            self.ui.channel2Button.setChecked(True)
            self.ui.channel2colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[2] + '; }')
            self.ui.channel3Button.setEnabled(True)
            self.ui.channel3Button.setChecked(True)
            self.ui.channel3colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[3] + '; }')
            self.ui.channel0Button.setText(translated.channel_names[0])
            self.ui.channel1Button.setText(translated.channel_names[1])
            self.ui.channel2Button.setText(translated.channel_names[2])
            self.ui.channel3Button.setText(translated.channel_names[3])
            self.ui.channel4Button.setVisible(False)
            self.ui.channel4colour.setVisible(False)
            self.ui.channel5Button.setVisible(False)
            self.ui.channel5colour.setVisible(False)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel6colour.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel7colour.setVisible(False)
            self.ui.channel8Button.setVisible(False)
            self.ui.channel8colour.setVisible(False)
        elif number_of_channels == '5':
            self.ui.channel0Button.setEnabled(True)
            self.ui.channel0Button.setChecked(True)
            self.ui.channel0colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[0] + '; }')
            self.ui.channel1Button.setEnabled(True)
            self.ui.channel1Button.setChecked(True)
            self.ui.channel1colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[1] + '; }')
            self.ui.channel2Button.setEnabled(True)
            self.ui.channel2Button.setChecked(True)
            self.ui.channel2colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[2] + '; }')
            self.ui.channel3Button.setEnabled(True)
            self.ui.channel3Button.setChecked(True)
            self.ui.channel3colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[3] + '; }')
            self.ui.channel4Button.setEnabled(True)
            self.ui.channel4Button.setChecked(True)
            self.ui.channel4colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[4] + '; }')
            self.ui.channel0Button.setText(translated.channel_names[0])
            self.ui.channel1Button.setText(translated.channel_names[1])
            self.ui.channel2Button.setText(translated.channel_names[2])
            self.ui.channel3Button.setText(translated.channel_names[3])
            self.ui.channel4Button.setText(translated.channel_names[4])
            self.ui.channel0Button.setVisible(True)
            self.ui.channel0colour.setVisible(True)
            self.ui.channel1Button.setVisible(True)
            self.ui.channel1colour.setVisible(True)
            self.ui.channel2Button.setVisible(True)
            self.ui.channel2colour.setVisible(True)
            self.ui.channel3Button.setVisible(True)
            self.ui.channel3colour.setVisible(True)
            self.ui.channel4Button.setVisible(True)
            self.ui.channel4colour.setVisible(True)
            self.ui.channel5Button.setVisible(False)
            self.ui.channel5colour.setVisible(False)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel6colour.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel7colour.setVisible(False)
            self.ui.channel8Button.setVisible(False)
            self.ui.channel8colour.setVisible(False)
        elif number_of_channels == '6':
            self.ui.channel0Button.setEnabled(True)
            self.ui.channel0Button.setChecked(True)
            self.ui.channel0colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[0] + '; }')
            self.ui.channel1Button.setEnabled(True)
            self.ui.channel1Button.setChecked(True)
            self.ui.channel1colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[1] + '; }')
            self.ui.channel2Button.setEnabled(True)
            self.ui.channel2Button.setChecked(True)
            self.ui.channel2colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[2] + '; }')
            self.ui.channel3Button.setEnabled(True)
            self.ui.channel3Button.setChecked(True)
            self.ui.channel3colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[3] + '; }')
            self.ui.channel4Button.setEnabled(True)
            self.ui.channel4Button.setChecked(True)
            self.ui.channel4colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[4] + '; }')
            self.ui.channel5Button.setEnabled(True)
            self.ui.channel5Button.setChecked(True)
            self.ui.channel5colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[5] + '; }')
            self.ui.channel0Button.setText(translated.channel_names[0])
            self.ui.channel1Button.setText(translated.channel_names[1])
            self.ui.channel2Button.setText(translated.channel_names[2])
            self.ui.channel3Button.setText(translated.channel_names[3])
            self.ui.channel4Button.setText(translated.channel_names[4])
            self.ui.channel5Button.setText(translated.channel_names[5])
            self.ui.channel0Button.setVisible(True)
            self.ui.channel0colour.setVisible(True)
            self.ui.channel1Button.setVisible(True)
            self.ui.channel1colour.setVisible(True)
            self.ui.channel2Button.setVisible(True)
            self.ui.channel2colour.setVisible(True)
            self.ui.channel3Button.setVisible(True)
            self.ui.channel3colour.setVisible(True)
            self.ui.channel4Button.setVisible(True)
            self.ui.channel4colour.setVisible(True)
            self.ui.channel5Button.setVisible(True)
            self.ui.channel5colour.setVisible(True)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel6colour.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel7colour.setVisible(False)
            self.ui.channel8Button.setVisible(False)
            self.ui.channel8colour.setVisible(False)
        elif number_of_channels == '7':
            self.ui.channel0Button.setEnabled(True)
            self.ui.channel0Button.setChecked(True)
            self.ui.channel0colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[0] + '; }')
            self.ui.channel1Button.setEnabled(True)
            self.ui.channel1Button.setChecked(True)
            self.ui.channel1colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[1] + '; }')
            self.ui.channel2Button.setEnabled(True)
            self.ui.channel2Button.setChecked(True)
            self.ui.channel2colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[2] + '; }')
            self.ui.channel3Button.setEnabled(True)
            self.ui.channel3Button.setChecked(True)
            self.ui.channel3colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[3] + '; }')
            self.ui.channel4Button.setEnabled(True)
            self.ui.channel4Button.setChecked(True)
            self.ui.channel4colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[4] + '; }')
            self.ui.channel5Button.setEnabled(True)
            self.ui.channel5Button.setChecked(True)
            self.ui.channel5colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[5] + '; }')
            self.ui.channel6Button.setEnabled(True)
            self.ui.channel6Button.setChecked(True)
            self.ui.channel6colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[6] + '; }')
            self.ui.channel0Button.setText(translated.channel_names[0])
            self.ui.channel1Button.setText(translated.channel_names[1])
            self.ui.channel2Button.setText(translated.channel_names[2])
            self.ui.channel3Button.setText(translated.channel_names[3])
            self.ui.channel4Button.setText(translated.channel_names[4])
            self.ui.channel5Button.setText(translated.channel_names[5])
            self.ui.channel6Button.setText(translated.channel_names[6])
            self.ui.channel0Button.setVisible(True)
            self.ui.channel0colour.setVisible(True)
            self.ui.channel1Button.setVisible(True)
            self.ui.channel1colour.setVisible(True)
            self.ui.channel2Button.setVisible(True)
            self.ui.channel2colour.setVisible(True)
            self.ui.channel3Button.setVisible(True)
            self.ui.channel3colour.setVisible(True)
            self.ui.channel4Button.setVisible(True)
            self.ui.channel4colour.setVisible(True)
            self.ui.channel5Button.setVisible(True)
            self.ui.channel5colour.setVisible(True)
            self.ui.channel6Button.setVisible(True)
            self.ui.channel6colour.setVisible(True)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel7colour.setVisible(False)
            self.ui.channel8Button.setVisible(False)
            self.ui.channel8colour.setVisible(False)
        elif number_of_channels == '8':
            self.ui.channel0Button.setEnabled(True)
            self.ui.channel0Button.setChecked(True)
            self.ui.channel0colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[0] + '; }')
            self.ui.channel1Button.setEnabled(True)
            self.ui.channel1Button.setChecked(True)
            self.ui.channel1colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[1] + '; }')
            self.ui.channel2Button.setEnabled(True)
            self.ui.channel2Button.setChecked(True)
            self.ui.channel2colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[2] + '; }')
            self.ui.channel3Button.setEnabled(True)
            self.ui.channel3Button.setChecked(True)
            self.ui.channel3colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[3] + '; }')
            self.ui.channel4Button.setEnabled(True)
            self.ui.channel4Button.setChecked(True)
            self.ui.channel4colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[4] + '; }')
            self.ui.channel5Button.setEnabled(True)
            self.ui.channel5Button.setChecked(True)
            self.ui.channel5colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[5] + '; }')
            self.ui.channel6Button.setEnabled(True)
            self.ui.channel6Button.setChecked(True)
            self.ui.channel6colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[6] + '; }')
            self.ui.channel7Button.setEnabled(True)
            self.ui.channel7Button.setChecked(True)
            self.ui.channel7colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[7] + '; }')
            self.ui.channel0Button.setVisible(True)
            self.ui.channel0colour.setVisible(True)
            self.ui.channel1Button.setVisible(True)
            self.ui.channel1colour.setVisible(True)
            self.ui.channel2Button.setVisible(True)
            self.ui.channel2colour.setVisible(True)
            self.ui.channel3Button.setVisible(True)
            self.ui.channel3colour.setVisible(True)
            self.ui.channel4Button.setVisible(True)
            self.ui.channel4colour.setVisible(True)
            self.ui.channel5Button.setVisible(True)
            self.ui.channel5colour.setVisible(True)
            self.ui.channel6Button.setVisible(True)
            self.ui.channel6colour.setVisible(True)
            self.ui.channel7Button.setVisible(True)
            self.ui.channel7colour.setVisible(True)
            self.ui.channel0Button.setText(translated.channel_names[0])
            self.ui.channel1Button.setText(translated.channel_names[1])
            self.ui.channel2Button.setText(translated.channel_names[2])
            self.ui.channel3Button.setText(translated.channel_names[3])
            self.ui.channel4Button.setText(translated.channel_names[4])
            self.ui.channel5Button.setText(translated.channel_names[5])
            self.ui.channel6Button.setText(translated.channel_names[6])
            self.ui.channel7Button.setText(translated.channel_names[7])
            self.ui.channel8Button.setVisible(False)
            self.ui.channel8colour.setVisible(False)
        elif number_of_channels == '9':
            self.ui.channel0Button.setEnabled(True)
            self.ui.channel0Button.setChecked(True)
            self.ui.channel0colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[0] + '; }')
            self.ui.channel1Button.setEnabled(True)
            self.ui.channel1Button.setChecked(True)
            self.ui.channel1colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[1] + '; }')
            self.ui.channel2Button.setEnabled(True)
            self.ui.channel2Button.setChecked(True)
            self.ui.channel2colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[2] + '; }')
            self.ui.channel3Button.setEnabled(True)
            self.ui.channel3Button.setChecked(True)
            self.ui.channel3colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[3] + '; }')
            self.ui.channel4Button.setEnabled(True)
            self.ui.channel4Button.setChecked(True)
            self.ui.channel4colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[4] + '; }')
            self.ui.channel5Button.setEnabled(True)
            self.ui.channel5Button.setChecked(True)
            self.ui.channel5colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[5] + '; }')
            self.ui.channel6Button.setEnabled(True)
            self.ui.channel6Button.setChecked(True)
            self.ui.channel6colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[6] + '; }')
            self.ui.channel7Button.setEnabled(True)
            self.ui.channel7Button.setChecked(True)
            self.ui.channel7colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[7] + '; }')
            self.ui.channel8Button.setEnabled(True)
            self.ui.channel8Button.setChecked(True)
            self.ui.channel8colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[8] + '; }')
            self.ui.channel0Button.setText(translated.channel_names[0])
            self.ui.channel1Button.setText(translated.channel_names[1])
            self.ui.channel2Button.setText(translated.channel_names[2])
            self.ui.channel3Button.setText(translated.channel_names[3])
            self.ui.channel4Button.setText(translated.channel_names[4])
            self.ui.channel5Button.setText(translated.channel_names[5])
            self.ui.channel6Button.setText(translated.channel_names[6])
            self.ui.channel7Button.setText(translated.channel_names[7])
            self.ui.channel8Button.setText(translated.channel_names[8])
            self.ui.channel0Button.setVisible(True)
            self.ui.channel0colour.setVisible(True)
            self.ui.channel1Button.setVisible(True)
            self.ui.channel1colour.setVisible(True)
            self.ui.channel2Button.setVisible(True)
            self.ui.channel2colour.setVisible(True)
            self.ui.channel3Button.setVisible(True)
            self.ui.channel3colour.setVisible(True)
            self.ui.channel4Button.setVisible(True)
            self.ui.channel4colour.setVisible(True)
            self.ui.channel5Button.setVisible(True)
            self.ui.channel5colour.setVisible(True)
            self.ui.channel6Button.setVisible(True)
            self.ui.channel6colour.setVisible(True)
            self.ui.channel7Button.setVisible(True)
            self.ui.channel7colour.setVisible(True)
            self.ui.channel8Button.setVisible(True)
            self.ui.channel8colour.setVisible(True)
        else:
            self.status_message('system', 'ERROR', 'Number of channels out of bounds.', None)
            self.logger.warning('Index Error, Number of channels out of bounds. %s' % number_of_channels)

    # ----------------------------------------
    # Parameter check state method.
    # ----------------------------------------

    def parameter_check_state(self, *args, **kwargs):

        # This bit is a bit of bodge as parameter check state will trigger when loading and raise
        # AttributeError so we just ignore it, not ideal!

        try:
            sender = self.sender()
            validator = sender.validator()
            state = validator.validate(sender.text(), 0)[0]
        except AttributeError:
            pass
        if self.disable_all_boolean is False and self.load_finish is True:

            for command in self.instrument.command_dict[
                    self.ui.moduleCombobox.itemData(self.ui.moduleCombobox.currentIndex())]:

                for key in command.keys():
                    if key == self.ui.commandCombobox.itemData(self.ui.commandCombobox.currentIndex()):
                        try:
                            if command[key]['Parameters']['Regex'] == 'None':
                                self.logger.debug('Command parameters regex is None setting parameter entry box to gray')
                                sender.setStyleSheet('QLineEdit { background-color: #EDEDED }')
                                self.logger.debug('Enabling execute button')
                                self.ui.executeButton.setEnabled(True)
                            else:
                                self.ui.executeButton.setEnabled(False)
                                if state == QtGui.QValidator.Acceptable and len(self.ui.commandParameter.text()) == 0:
                                    sender.setStyleSheet('QLineEdit { background-color: #FFFFFF }')
                                elif state == QtGui.QValidator.Acceptable and len(self.ui.commandParameter.text()) > 0:
                                    color = '#c4df9b'  # green
                                    sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
                                    self.ui.executeButton.setEnabled(True)
                                elif state == QtGui.QValidator.Intermediate and len(self.ui.commandParameter.text()) == 0:
                                    sender.setStyleSheet('QLineEdit { background-color: #FFFFFF }')
                                elif state == QtGui.QValidator.Intermediate and len(self.ui.commandParameter.text()) > 0:
                                    color = '#fff79a'  # yellow
                                    sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
                                else:
                                    sender.setStyleSheet('QLineEdit { background-color: #f6989d')
                        except KeyError:
                            if self.parameter_check_state_trip == 0:
                                pass
                            else:
                                self.logger.debug('Command parameters key error setting parameter entry box to gray')
                                sender.setStyleSheet('QLineEdit { background-color: #EDEDED }')
                        else:
                            self.parameter_check_state_trip += 1

    # ----------------------------------------
    # Menu trigger methods.
    # ----------------------------------------

    def configuration_triggered(self):
        self.logger.info('Calling configuration tool.')
        self.configurationManager.exec_()

        self.status_message('configuration', self.configurationManager.response_message[0],
                            self.configurationManager.response_message[1], None)

        #  Attempt at allowing configuration changes without requiring restart.
        if self.configurationManager.response_message[0] == 'SUCCESS':
            self.initialise_configuration()

    def instrument_attrib_triggered(self):
        self.logger.info('Calling edit instrument attributes.')
        self.instrument_attributes.set(self.instrument, self.instrument_file)

        self.instrument_attributes.exec()

        self.status_message('instrumentAttributes', self.instrument_attributes.response_message[0],
                            self.instrument_attributes.response_message[1], None)

        #  Attempt at allowing configuration changes without requiring restart.
        if self.instrument_attributes.response_message[0] == 'SUCCESS':
            self.initialise_configuration()

    # def futurlec_baudrate_tool_triggered(self):
    #     self.logger.debug('Calling futurlec baudrate configuration tool.')
    #     self.futurlec_baudrate_tool.exec_()

    def instrument_builder_triggered(self):
        self.logger.info('Calling instrument builder.')
        self.instrumentBuilder.exec_()

    def execute_triggered(self):
        addr = self.instrument.instrument_staribus_address

        for command in self.instrument.command_dict[
            self.ui.moduleCombobox.itemData(self.ui.moduleCombobox.currentIndex())]:

            for key in command.keys():
                if key == self.ui.commandCombobox.itemData(self.ui.commandCombobox.currentIndex()):

                    ident = self.ui.commandCombobox.currentText()
                    base = self.ui.moduleCombobox.itemData(self.ui.moduleCombobox.currentIndex())
                    code = self.ui.commandCombobox.itemData(self.ui.commandCombobox.currentIndex())
                    variant = command[key]['Variant']
                    send_to_port = command[key]['SendToPort']

                    self.logger.info('################### Executing command : %s ###################' % ident)

                    if command[key]['BlockedData'] == 'None':
                        blocked_data = None
                        self.logger.debug('Blocked data is None')
                    else:
                        blocked_data = command[key]['BlockedData']
                        self.logger.debug('Blocked data is ' + str(blocked_data))

                    if command[key]['SteppedData'] == 'None':
                        stepped_data = None
                        self.logger.debug('Stepped data is None')
                    else:
                        stepped_data = command[key]['SteppedData']
                        self.logger.debug('Stepped data is ' + str(stepped_data))

                    if command[key]['Parameters']['Choices'] == 'None':
                        choice = None
                        self.logger.debug('Choice is None')
                    else:
                        choice = self.ui.choicesComboBox.currentText()
                        self.logger.debug('Choice is ' + str(choice))

                    if command[key]['Parameters']['Regex'] == 'None':
                        parameter = None
                        self.logger.debug('Parameter is None')
                    else:
                        parameter = self.ui.commandParameter.text()
                        self.logger.debug('Parameter is ' + str(parameter))

                    if command[key]['Response']['Units'] == 'None':
                        units = None
                        self.logger.debug('Units is None')
                    else:
                        units = command[key]['Response']['Units']
                        self.logger.debug('Units is ' + str(units))

                    if command[key]['Response']['Regex'] == 'None':
                        response_regex = None
                        self.logger.debug('Response regex is None')
                    else:
                        response_regex = command[key]['Response']['Regex']
                        self.logger.debug('Response regex is ' + str(response_regex))

                    if self.chart_warning == 0:
                        if sys.platform.startswith('win32'):
                            if ident == 'getData' or ident == 'importLocal':
                                self.status_message('system', 'INFO', 'Chart creation can take a long time. '
                                                                      'Windows may report (Not Responding) please ignore..', None)
                                self.chart_warning = 1
                        else:
                            if ident == 'getData' or ident == 'importLocal':
                                self.status_message('system', 'INFO', 'Chart creation can take a long time..', None)
                                self.chart_warning = 1

                    response = self.command_interpreter.process_command(addr, base, code, variant, send_to_port, blocked_data,
                                                                        stepped_data, choice, parameter, response_regex)

                    # Now we process the response based on command, probably not the most elegant way of doing things but it works.

                    if ident == 'getData' and response[0].startswith('SUCCESS'):
                        # Add the chart widget to the UI.

                        self.logger.debug('Instrument Number of Channels : ' + str(
                            self.instrument.instrument_number_of_channels))

                        self.chart.clear()
                        if self.chart.add_metadata('data') is not True:
                            self.status_message(ident, 'PREMATURE_TERMINATION', 'Unable to add chart metadata', None)
                        else:
                            chart_response = self.chart.add_data(self.instrument.instrument_number_of_channels)
                            if chart_response[0].startswith('SUCCESS'):
                                self.data_from = 'data'
                                self.status_message(ident, response[0], response[1], units)
                                self.chart_control_panel(self.instrument.instrument_number_of_channels, self.instrument)
                                self.ui.chartDecimateCheckBox.setEnabled(True)
                                self.ui.chartDecimateCheckBox.setChecked(False)
                                self.ui.chartAutoRangeCheckBox.setEnabled(True)
                                self.ui.chartAutoRangeCheckBox.setChecked(False)
                                self.ui.showLegend.setChecked(False)
                                self.data_source = 'instrument'
                            else:
                                self.status_message(ident, chart_response[0], chart_response[1], None)
                    elif ident == 'importLocal' and response[0].startswith('SUCCESS'):
                        # Add the chart widget to the UI.
                        self.logger.debug('Imported data Number of Channels : ' + str(
                            self.metadata_deconstructor.instrument_number_of_channels))

                        self.chart.clear()
                        if self.chart.add_metadata('csv') is not True:
                            self.status_message(ident, 'PREMATURE_TERMINATION', 'Unable to add chart metadata', None)
                        else:
                            chart_response = self.chart.add_data(self.metadata_deconstructor.instrument_number_of_channels)
                            if chart_response[0].startswith('SUCCESS'):
                                self.data_from = 'csv'
                                self.status_message(ident, response[0], response[1], units)

                                self.chart_control_panel(self.metadata_deconstructor.instrument_number_of_channels,
                                                         self.metadata_deconstructor)
                                self.ui.chartDecimateCheckBox.setEnabled(True)
                                self.ui.chartDecimateCheckBox.setChecked(False)
                                self.ui.chartAutoRangeCheckBox.setChecked(True)
                                self.ui.showLegend.setChecked(False)
                                self.data_source = 'imported'
                            else:
                                self.status_message(ident, chart_response[0], chart_response[1], None)
                    elif ident == 'getA2D' and response[0].startswith('SUCCESS'):
                        a2dmessage = 'Channel ID ' + str(parameter) + ' = ' + response[1] + 'mV'
                        self.status_message(ident, response[0], a2dmessage, units)
                    else:
                        self.status_message(ident, response[0], response[1], units)

    # ----------------------------------------
    # Chart show legend method.
    # ----------------------------------------

    def chart_show_legend_triggered(self):
        if self.ui.showLegend.isChecked():
            self.chart.chart_legend(True)
        else:
            self.chart.chart_legend(False)

    # ----------------------------------------
    # Chart channel button methods.
    # ----------------------------------------

    def channel0_triggered(self):
        if self.ui.channel0Button.isChecked():
            self.chart.channel_control(0, True)
        else:
            self.chart.channel_control(0, False)

    def channel1_triggered(self):
        if self.ui.channel1Button.isChecked():
            self.chart.channel_control(1, True)
        else:
            self.chart.channel_control(1, False)

    def channel2_triggered(self):
        if self.ui.channel2Button.isChecked():
            self.chart.channel_control(2, True)
        else:
            self.chart.channel_control(2, False)

    def channel3_triggered(self):
        if self.ui.channel3Button.isChecked():
            self.chart.channel_control(3, True)
        else:
            self.chart.channel_control(3, False)

    def channel4_triggered(self):
        if self.ui.channel4Button.isChecked():
            self.chart.channel_control(4, True)
        else:
            self.chart.channel_control(4, False)

    def channel5_triggered(self):
        if self.ui.channel5Button.isChecked():
            self.chart.channel_control(5, True)
        else:
            self.chart.channel_control(5, False)

    def channel6_triggered(self):
        if self.ui.channel6Button.isChecked():
            self.chart.channel_control(6, True)
        else:
            self.chart.channel_control(6, False)

    def channel7_triggered(self):
        if self.ui.channel7Button.isChecked():
            self.chart.channel_control(7, True)
        else:
            self.chart.channel_control(7, False)

    def channel8_triggered(self):
        if self.ui.channel8Button.isChecked():
            self.chart.channel_control(8, True)
        else:
            self.chart.channel_control(8, False)

    def chart_auto_range_triggered(self):
        if self.ui.chartAutoRangeCheckBox.isChecked():
            self.chart.channel_autoscale(True)
        else:
            self.chart.channel_autoscale(False)

    def manual_channel_trigger(self, number_of_channels):

        if number_of_channels == '1':
            pass
        elif number_of_channels == '2':
            self.channel0_triggered(), self.channel1_triggered()
        elif number_of_channels == '3':
            self.channel0_triggered(), self.channel1_triggered(), self.channel2_triggered()
        elif number_of_channels == '4':
            self.channel0_triggered(), self.channel1_triggered(), self.channel2_triggered(), \
            self.channel3_triggered()
        elif number_of_channels == '5':
            self.channel0_triggered(), self.channel1_triggered(), self.channel2_triggered(), \
            self.channel3_triggered(), self.channel4_triggered()
        elif number_of_channels == '6':
            self.channel0_triggered(), self.channel1_triggered(), self.channel2_triggered(), \
            self.channel3_triggered(), self.channel4_triggered(), self.channel5_triggered()
        elif number_of_channels == '7':
            self.channel0_triggered(), self.channel1_triggered(), self.channel2_triggered(), \
            self.channel3_triggered(), self.channel4_triggered(), self.channel5_triggered(), \
            self.channel6_triggered()
        elif number_of_channels == '8':
            self.channel0_triggered(), self.channel1_triggered(), self.channel2_triggered(), \
            self.channel3_triggered(), self.channel4_triggered(), self.channel5_triggered(), \
            self.channel6_triggered(), self.channel7_triggered()
        elif number_of_channels == '9':
            self.channel0_triggered(), self.channel1_triggered(), self.channel2_triggered(), \
            self.channel3_triggered(), self.channel4_triggered(), self.channel5_triggered(), \
            self.channel6_triggered(), self.channel7_triggered(), self.channel8_triggered()

    def chart_decimate_triggered(self):
        if self.chart is not None:

            if self.data_from == 'data':
                number_of_channels = self.instrument.instrument_number_of_channels
            else:
                number_of_channels = self.metadata_deconstructor.instrument_number_of_channels

            self.chart.clear()
            self.chart.add_metadata(self.data_from)

            if self.ui.chartDecimateCheckBox.isChecked():
                self.chart.decimate_data(number_of_channels)
            else:
                self.chart.add_data(number_of_channels)

            self.chart_show_legend_triggered()
            self.manual_channel_trigger(number_of_channels)

    def closeEvent(self, event):
        if self.saved_data_state is False:
            message = 'Are you sure you want to exit?'
        else:
            message = 'WARNING:  You have unsaved data.\n\nAre you sure you want to exit?'

        result = QtGui.QMessageBox.question(None,
                                            "Confirm Exit...",
                                            message,
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        event.ignore()

        if result == QtGui.QMessageBox.Yes:
            event.accept()

    def help_about_triggered(self):
        QtGui.QMessageBox.information(self, 'About', 'StarbaseMini ' + version + '\nBy Mark Horn\n'
                                                           'mhorn71@gmail.com\n(c) 2016')

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = Main()
    myapp.setWindowTitle('StarbaseMini -- Ver %s' % version)
    myapp.showMaximized()
    myapp.show()
    x = app.exec_()
    sys.exit(x)
