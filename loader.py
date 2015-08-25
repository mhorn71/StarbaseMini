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
import futurlec
import instument_builder
import interpreter
import constants
import datatranslators
import metadata

version = '1.0.256'


class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):

        # Fatal error trip
        fatal_error = False
        config_error = False

        # Parameter / check state, regex parameter.
        self.parameter_regex = '^.*$'

        # DataBlock
        self.DataBlock = []
        self.DataBlockBool = False

        # Base attributes.
        self.saved_data_state = False

        # Disable UI boolean.
        self.disable_all_boolean = False

        # Initialise UI
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

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

        # Initialise configuration.
        try:
            self.config = config_utilities.ConfigTool()
        except (FileNotFoundError, OSError) as msg:
            msg = ('Configuration Tool : %s' % str(msg))
            self.status_message('system', 'CRITICAL_ERROR', str(msg), None)
            self.disable_all()
            fatal_error = True
            config_error = True
        else:
            # Generate user configuration if it's missing.
            try:
                self.config.check_conf_exists()
            except IOError as msg:
                msg = ('Configuration IOError : %s' % str(msg))
                self.status_message('system', 'CRITICAL_ERROR', str(msg), None)
                fatal_error = True
                config_error = True

        if fatal_error is False:
            # Get instrument identifier.
            try:
                self.instrument_identifier = self.config.get('Application', 'instrument_identifier')
            except ValueError as msg:
                msg = ('Instrument Identifier ValueError : %s' % str(msg))
                self.status_message('system', 'CRITICAL_ERROR', str(msg), None)

            #  Load and initialise logging configuration from user configuration file.
            logging.config.fileConfig(self.config.conf_file, disable_existing_loggers=True)
            self.logger = logging.getLogger('main')
            self.logger.info('-------------- APPLICATION STARTUP --------------')

            # Load set instrument XML, selectedInstrument returns the relative path and XML file name.
            try:
                instruments = 'instruments' + os.path.sep + 'instruments.xml'
                my_instruments = xml_utilities.Instruments(instruments)
            except (FileNotFoundError, ValueError, LookupError, AttributeError) as msg:
                fatal_error = True
                self.logger.critical('Unable to load instruments.xml %s' % str(msg))
                self.status_message('system', 'CRITICAL_ERROR', str(msg), None)
            else:
                try:
                    filename = my_instruments.get_filename(self.instrument_identifier)
                    filename = 'instruments' + os.path.sep + filename
                    self.instrument = xml_utilities.Instrument(filename)
                except (FileNotFoundError, ValueError, LookupError, AttributeError) as msg:
                    self.logger.critical('Unable to load instrument xml %s' % str(msg))
                    fatal_error = True
                    self.status_message('system', 'CRITICAL_ERROR', str(msg), None)
                else:
                    self.logger.debug('Instrument XML found at : %s' % filename)
                    self.logger.info('Instrument XML loaded for : %s', self.instrument_identifier)

            # Load application parameters.
            try:
                instrument_autodetect = self.config.get('Application', 'instrument_autodetect')
                instrument_data_path = self.config.get('Application', 'instrument_data_path')
                starinet_relay_boolean = self.config.get('StarinetRelay', 'active')
                starinet_address = self.config.get('StarinetRelay', 'address')
                starinet_port = self.config.get('StarinetRelay', 'starinet_port')
                serial_port = self.config.get('StaribusPort', 'staribus_port')
                serial_baudrate = self.config.get('StaribusPort', 'baudrate')
                serial_port_timeout = self.config.get('StaribusPort', 'timeout')
            except ValueError as msg:
                self.logger.critical('Configuration ValueError : %s' % str(msg))
                msg = ('Configuration ValueError : %s exiting.' % str(msg))
                fatal_error = True
                self.status_message('system', 'CRITICAL_ERROR', str(msg), None)
            else:
                self.logger.debug('Initial parameter for instrument_autodetect : %s' % instrument_autodetect)
                self.logger.debug('Initial parameter for instrument_data_path : %s' % instrument_data_path)
                self.logger.debug('Initial parameter for starinet_relay_boolean : %s' % starinet_relay_boolean)
                self.logger.debug('Initial parameter for starinet_relay_address : %s' % starinet_address)
                self.logger.debug('Initial parameter for starinet_relay_port : %s' % starinet_port)
                self.logger.debug('Initial parameter for serial_port : %s' % serial_port)
                self.logger.debug('Initial parameter for serial_baudrate : %s' % serial_baudrate)
                self.logger.debug('Initial parameter for serial_port_timeout : %s' % serial_port_timeout)

        # Initialise datatranslator
        # added data translators here.
        if self.instrument.instrument_datatranslator == 'StaribusBlock':
            self.datatranslator = datatranslators.StaribusParser(self.instrument.instrument_number_of_channels)
            # Initialise metadata
            self.metadata_creator = metadata.StaribusMetaDataCreator(self)
            self.metadata_deconstructor = metadata.StaribusMetaDataDeconstructor(self)
        else:
            self.logger.critical('Unable to locate Instrument DataTranslator')
            self.status_message('system', 'CRITICAL_ERROR', 'Unable to locate Instrument DataTranslator', None)
            fatal_error = True

        if fatal_error is False:
            # Instrument autodetect initialisation.
            if instrument_autodetect == 'True':
                self.logger.info('Instrument autodetect is True.')
                if self.instrument.instrument_starinet_address != 'None':
                    self.logger.info('Instrument autodetect true however instrument appears to be Starinet.')
                    instrument_autodetect_status_boolean = False
                else:
                    ports = utilities.serial_port_scanner()
                    if ports is None:
                        self.logger.warning('No serial ports found to scan for instrument.')
                        instrument_autodetect_status_boolean = False
                        self.disable_all()
                        self.status_message('system', 'WARNING', 'No serial ports found, ui controls disabled.', None)
                    else:
                        instrument_port = utilities.check_serial_port_staribus_instrument(
                            self.instrument.instrument_staribus_address, ports, serial_baudrate)
                        if instrument_port is None:
                            self.logger.warning('Staribus instrument not found for address %s' %
                                                self.instrument.instrument_staribus_address)
                            instrument_autodetect_status_boolean = False
                        elif len(instrument_port) > 1:
                            self.logger.warning('Multiple Staribus instruments found defaulting to first.')
                            self.status_message('system', 'WARNING',
                                                'Multiple Staribus instruments found defaulting to first.', None)
                            self.logger.info('Setting serial port to %s' % instrument_port[0])
                            serial_port = instrument_port[0]
                            instrument_autodetect_status_boolean = True
                        else:
                            self.status_message('system', 'INFO',  ('%s instrument found.' %
                                                                    self.instrument.instrument_identifier), None)
                            self.logger.info('Setting serial port to %s' % instrument_port[0])
                            serial_port = instrument_port[0]
                            instrument_autodetect_status_boolean = True

                if instrument_autodetect_status_boolean is True:
                    try:
                        self.config.set('StaribusPort', 'staribus_port', serial_port)
                    except (ValueError, IOError) as msg:
                        self.logger.critical('Fatal Error Unable to set serial port : %s' % msg)
                        msg = ('Unable to set serial port : %s' % msg)
                        self.status_message('system', 'CRITICAL_ERROR', str(msg), None)

            # Initialise Starinet relay.
            if starinet_relay_boolean == 'True' and instrument_autodetect == 'True':
                if instrument_autodetect_status_boolean is True:
                    self.disable_all()
                    starinet_connector.StarinetConnectorStart(starinet_address, starinet_port, serial_port,
                                                              serial_baudrate, serial_port_timeout)
                    self.logger.info('Starinet relay initialised.')
                    msg = 'Starinet relay initialised.'
                    self.status_message('system', 'INFO', msg, None)
                else:
                    self.disable_all()
                    self.logger.warning('Starinet relay and Instrument autodetect are True but no Instrument found.')
                    msg = 'Starinet relay and Instrument autodetect are True but no Instrument found.'
                    self.status_message('system', 'WARNING', msg, None)
                    self.logger.critical('Starinet relay cannot initialise as serial port isn\'t set.')
                    msg = 'Starinet relay cannot initialise as serial port isn\'t set.'
                    self.status_message('system', 'ERROR', msg, None)
            elif starinet_relay_boolean =='True':
                if serial_port is None:
                    self.disable_all()
                    self.logger.critical('Starinet relay cannot initialise as serial port isn\'t set.')
                    msg = 'Starinet relay cannot initialise as serial port isn\'t set.'
                    self.status_message('system', 'ERROR', msg, None)
                else:
                    self.disable_all()
                    starinet_connector.StarinetConnectorStart(starinet_address, starinet_port, serial_port,
                                                              serial_baudrate, serial_port_timeout)
                    self.logger.info('Starinet relay initialised.')
                    msg = 'Starinet relay initialised.'
                    self.status_message('system', 'INFO', msg, None)

            # Initialise Command Interpreter
            try:
                if starinet_relay_boolean == 'False':
                    if self.instrument.instrument_starinet_address != 'None':
                        self.logger.info('Initialising Command Interpreter for Starinet')
                        self.command_interpreter = interpreter.CommandInterpreter(self)
                    elif self.instrument.instrument_staribus_address != 'None':
                        if utilities.check_serial_port(self.config.get('StaribusPort', 'staribus_port')):
                            self.logger.info('Initialising Command Interpreter for Staribus')
                            self.command_interpreter = interpreter.CommandInterpreter(self)
                        else:
                            self.disable_all()
                            self.status_message('system', 'ERROR',
                                                'Unable to set stream type - UI controls disabled.', None)
                    else:
                        self.logger.critical('Unable able to determine stream type.')
                        self.status_message('system', 'ERROR',
                                            'Unable able to determine stream type - UI controls disabled.', None)
                        self.disable_all()
            except (TypeError, IOError) as msg:
                self.logger.critical(str(msg))
                self.status_message('system', 'CRITICAL_ERROR', str(msg), None)
                self.disable_all()

            # Trip counters, these are so we ignore dict KeyError's when first populating which seems to differ
            # from one platform to another and I have no idea why.  Answers on a postcard please. ;-))
            self.ui_module_trip = 0
            self.ui_command_trip = 0
            self.command_parameter_trip = 0
            self.parameter_check_state_trip = 0

            # Disable all channel buttons to start with.
            self.ui.channel0Button.setEnabled(False)
            self.ui.channel1Button.setEnabled(False)
            self.ui.channel2Button.setEnabled(False)
            self.ui.channel3Button.setEnabled(False)
            self.ui.channel4Button.setEnabled(False)
            self.ui.channel5Button.setEnabled(False)
            self.ui.channel6Button.setEnabled(False)
            self.ui.channel7Button.setEnabled(False)
            self.ui.channel8Button.setEnabled(False)

            # Disable Parameter Entry, Choices Combobox and Execute Button
            self.ui.executeButton.setEnabled(False)
            self.ui.commandParameter.setEnabled(False)
            self.ui.choicesComboBox.setEnabled(False)

            # Button connectors
            self.ui.executeButton.clicked.connect(self.execute_triggered)

            # Module, Command and Choices ComboBox Triggers.
            self.ui.moduleCombobox.currentIndexChanged.connect(self.populate_ui_command)
            self.ui.commandCombobox.currentIndexChanged.connect(self.command_parameter_populate)

            # Parameter entry emit and connect signals
            self.ui.commandParameter.textChanged.connect(self.parameter_check_state)
            self.ui.commandParameter.textChanged.emit(self.ui.commandParameter.text())

            # Fire populate_ui_module for the first time.
            self.populate_ui_module()

            # Initialise Chart Control Panel
            self.chart_control_panel_populate()

            # Initialisation Statup Finish Status Message.
            self.status_message('system', 'INFO', 'Application Started.', None)

        elif fatal_error is True:
            self.disable_all()

        # Menu items
        self.logger.debug('Setting menu item triggers.')
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionConfiguration.triggered.connect(self.configuration_triggered)
        self.ui.actionInstrumentBuilder.triggered.connect(self.instrument_builder_triggered)
        self.ui.actionControllerEditor.triggered.connect(self.futurlec_baudrate_tool_triggered)
        # self.ui.actionManual.triggered.connect(self.help_manual_triggered)
        # self.ui.actionAbout.triggered.connect(self.help_about_triggered)

        # Initialise configurationManager
        if config_error is False:
            self.configurationManager = config_utilities.ConfigManager()

        # Initialise Futurlec Baudrate tool
        self.futurlec_baudrate_tool = futurlec.FuturlecBaudrate()

        # Initialise instrumentBuilder
        self.instrumentBuilder = instument_builder.InstrumentBuilder()

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

        # Setup charting
        self.mplwindow = self.ui.mplwindow
        self.mplvl = self.ui.mplvl

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
                self.ui.commandCombobox.addItem(cmd)
                self.ui.commandCombobox.setItemData(index, self.instrument.command_dict[cmd]['Description'],
                                                    QtCore.Qt.ToolTipRole)
    
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
        try:
            # Check if command has choices.
            if self.instrument.command_dict[self.ui.commandCombobox.currentText()]['Parameters']['Choices'] == 'None':
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
                choices = \
                    (self.instrument.command_dict[self.ui.commandCombobox.currentText()]
                     ['Parameters']['Choices'].split(','))
                self.logger.debug('%s %s %s', self.ui.commandCombobox.currentText(), 'Parameters Choices :',
                                  str(choices))
                self.ui.choicesComboBox.addItems(choices)  # Add choices to combobox.
    
                # Add choices tool tips to combo box.
                for i in range(len(choices)):
                    self.ui.choicesComboBox.setItemData(i, (
                        self.instrument.command_dict[self.ui.commandCombobox.currentText()]['Parameters']['Tooltip']),
                                                        QtCore.Qt.ToolTipRole)
    
            # Check if command has parameters.
            if self.instrument.command_dict[self.ui.commandCombobox.currentText()]['Parameters']['Regex'] == 'None':
                self.logger.debug('%s %s', self.ui.commandCombobox.currentText(), 'Parameters Regex : None')
                self.ui.commandParameter.clear()
                self.ui.commandParameter.setEnabled(False)
                self.ui.commandParameter.setStyleSheet('QLineEdit { background-color: #EBEBEB }')
            else:
                self.ui.commandParameter.setStyleSheet('QLineEdit { background-color: #FFFFFF }')

                if self.disable_all_boolean is False:
                    self.ui.commandParameter.setEnabled(True)
                    self.ui.executeButton.setEnabled(False)

                self.ui.commandParameter.setToolTip(self.instrument.command_dict[self.ui.commandCombobox.currentText()]
                                                    ['Parameters']['Tooltip'])
                self.parameter_regex = \
                    self.instrument.command_dict[self.ui.commandCombobox.currentText()]['Parameters']['Regex']
    
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
            
    def chart_control_panel_populate(self):

        if self.instrument.instrument_number_of_channels == '2':
            self.ui.channel0Button.setText(self.instrument.channel_names[0])
            self.ui.channel1Button.setText(self.instrument.channel_names[1])
            self.ui.channel2Button.setVisible(False)
            self.ui.channel3Button.setVisible(False)
            self.ui.channel4Button.setVisible(False)
            self.ui.channel5Button.setVisible(False)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel8Button.setVisible(False)
        elif self.instrument.instrument_number_of_channels == '3':
            self.ui.channel0Button.setText(self.instrument.channel_names[0])
            self.ui.channel1Button.setText(self.instrument.channel_names[1])
            self.ui.channel2Button.setText(self.instrument.channel_names[2])
            self.ui.channel3Button.setVisible(False)
            self.ui.channel4Button.setVisible(False)
            self.ui.channel5Button.setVisible(False)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel8Button.setVisible(False)
        elif self.instrument.instrument_number_of_channels == '4':
            self.ui.channel0Button.setText(self.instrument.channel_names[0])
            self.ui.channel1Button.setText(self.instrument.channel_names[1])
            self.ui.channel2Button.setText(self.instrument.channel_names[2])
            self.ui.channel3Button.setText(self.instrument.channel_names[3])
            self.ui.channel4Button.setVisible(False)
            self.ui.channel5Button.setVisible(False)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel8Button.setVisible(False)
        elif self.instrument.instrument_number_of_channels == '5':
            self.ui.channel0Button.setText(self.instrument.channel_names[0])
            self.ui.channel1Button.setText(self.instrument.channel_names[1])
            self.ui.channel2Button.setText(self.instrument.channel_names[2])
            self.ui.channel3Button.setText(self.instrument.channel_names[3])
            self.ui.channel4Button.setText(self.instrument.channel_names[4])
            self.ui.channel5Button.setVisible(False)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel8Button.setVisible(False)
        elif self.instrument.instrument_number_of_channels == '6':
            self.ui.channel0Button.setText(self.instrument.channel_names[0])
            self.ui.channel1Button.setText(self.instrument.channel_names[1])
            self.ui.channel2Button.setText(self.instrument.channel_names[2])
            self.ui.channel3Button.setText(self.instrument.channel_names[3])
            self.ui.channel4Button.setText(self.instrument.channel_names[4])
            self.ui.channel5Button.setText(self.instrument.channel_names[5])
            self.ui.channel6Button.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel8Button.setVisible(False)
        elif self.instrument.instrument_number_of_channels == '7':
            self.ui.channel0Button.setText(self.instrument.channel_names[0])
            self.ui.channel1Button.setText(self.instrument.channel_names[1])
            self.ui.channel2Button.setText(self.instrument.channel_names[2])
            self.ui.channel3Button.setText(self.instrument.channel_names[3])
            self.ui.channel4Button.setText(self.instrument.channel_names[4])
            self.ui.channel5Button.setText(self.instrument.channel_names[5])
            self.ui.channel6Button.setText(self.instrument.channel_names[6])
            self.ui.channel7Button.setVisible(False)
            self.ui.channel8Button.setVisible(False)
        elif self.instrument.instrument_number_of_channels == '8':
            self.ui.channel0Button.setText(self.instrument.channel_names[0])
            self.ui.channel1Button.setText(self.instrument.channel_names[1])
            self.ui.channel2Button.setText(self.instrument.channel_names[2])
            self.ui.channel3Button.setText(self.instrument.channel_names[3])
            self.ui.channel4Button.setText(self.instrument.channel_names[4])
            self.ui.channel5Button.setText(self.instrument.channel_names[5])
            self.ui.channel6Button.setText(self.instrument.channel_names[6])
            self.ui.channel7Button.setText(self.instrument.channel_names[7])
            self.ui.channel8Button.setVisible(False)
        elif self.instrument.instrument_number_of_channels == '9':
            self.ui.channel0Button.setText(self.instrument.channel_names[0])
            self.ui.channel1Button.setText(self.instrument.channel_names[1])
            self.ui.channel2Button.setText(self.instrument.channel_names[2])
            self.ui.channel3Button.setText(self.instrument.channel_names[3])
            self.ui.channel4Button.setText(self.instrument.channel_names[4])
            self.ui.channel5Button.setText(self.instrument.channel_names[5])
            self.ui.channel6Button.setText(self.instrument.channel_names[6])
            self.ui.channel7Button.setText(self.instrument.channel_names[7])
            self.ui.channel8Button.setText(self.instrument.channel_names[8])
        else:
            self.status_message('system', 'ERROR', 'Number of channels out of bounds.', None)
            self.logger.warning('Index Error, Number of channels out of bounds. %s' %
                                self.instrument.instrument_number_of_channels)

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
        if self.disable_all_boolean is False:
            try:
                if self.instrument.command_dict[self.ui.commandCombobox.currentText()]['Parameters']['Regex'] == 'None':
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
    # Disable ui controls method.
    # ----------------------------------------

    def disable_all(self):
        self.disable_all_boolean = True
        self.logger.info('Disabling all UI input widgets.')
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

    # ----------------------------------------
    # Status Message method.
    # ----------------------------------------

    def status_message(self, ident, status, response_value, units):

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
    # Menu trigger methods.
    # ----------------------------------------

    def configuration_triggered(self):
        self.logger.info('Calling configuration tool.')
        self.configurationManager.exec_()

    def futurlec_baudrate_tool_triggered(self):
        self.logger.debug('Calling futurlec baudrate configuration tool.')
        self.futurlec_baudrate_tool.exec_()

    def instrument_builder_triggered(self):
        self.logger.info('Calling instrument builder.')
        self.instrumentBuilder.exec_()

    def execute_triggered(self):
        addr = self.instrument.instrument_staribus_address
        ident = self.ui.commandCombobox.currentText()
        base = self.instrument.command_dict[ident]['Base']
        code = self.instrument.command_dict[ident]['Code']
        variant = self.instrument.command_dict[ident]['Variant']
        send_to_port = self.instrument.command_dict[ident]['SendToPort']

        if self.instrument.command_dict[ident]['BlockedData'] == 'None':
            blocked_data = None
        else:
            blocked_data = self.instrument.command_dict[ident]['BlockedData']

        if self.instrument.command_dict[ident]['SteppedData'] == 'None':
            stepped_data = None
        else:
            stepped_data = self.instrument.command_dict[ident]['SteppedData']

        if self.instrument.command_dict[ident]['Parameters']['Choices'] == 'None':
            choice = None
        else:
            choice = self.ui.choicesComboBox.currentText()

            if choice == 'True':
                choice = self.instrument.boolean_true
            elif choice == 'False':
                choice = self.instrument.boolean_false
            else:
                pass

        if self.instrument.command_dict[ident]['Parameters']['Regex'] == 'None':
            parameter = None
        else:
            parameter = self.ui.commandParameter.text()

        if self.instrument.command_dict[ident]['Response']['Units'] == 'None':
            units = None
        else:
            units = self.instrument.command_dict[ident]['Response']['Units']

        if self.instrument.command_dict[ident]['Response']['Regex'] == 'None':
            response_regex = None
        else:
            response_regex = self.instrument.command_dict[ident]['Response']['Regex']

        response = self.command_interpreter.process_command(addr, base, code, variant, send_to_port, blocked_data,
                                                            stepped_data, choice, parameter, response_regex)

        if ident == 'getData' and response[0].startswith('SUCCESS'):
            print('We should generate a chart at this point.')
            self.status_message(ident, response[0], response[1], units)
        elif ident == 'importLocal' and response[0].startswith('SUCCESS'):
            print('We should generate a chart at this point.')
            self.status_message(ident, response[0], response[1], units)
        else:
            self.status_message(ident, response[0], response[1], units)

    def closeEvent(self,event):
        if self.saved_data_state is False:
            message = 'Are you sure you want to exit?'
        else:
            message = 'WARNING:  You have unsaved data.\n\nAre you sure you want to exit?'

        result = QtGui.QMessageBox.question(self,
                                            "Confirm Exit...",
                                            message,
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        event.ignore()

        if result == QtGui.QMessageBox.Yes:
            event.accept()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = Main()
    myapp.setWindowTitle('StarbaseMini -- Ver %s' % version)
    # myapp.showMaximized()
    myapp.show()
    x = app.exec_()
    sys.exit(x)