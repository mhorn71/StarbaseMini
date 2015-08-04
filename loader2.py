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

version = '0.0.2'


class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):

        # Initialise UI
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialise configuration.
        try:
            self.config = config_utilities.ConfigTool()
        except (FileNotFoundError, OSError) as msg:
            print('Fatal Error : %s exiting.' % str(msg))
            # todo remove sys.exit and add UI status message.
            sys.exit(1)

        # Generate user configuration if it's missing.
        try:
            self.config.check_conf_exists()
        except IOError as msg:
            print('Fatal IOError : %s exiting.' % str(msg))
            # todo remove sys.exit and add UI status message.
            sys.exit(1)

        # Get instrument identifier.
        try:
            self.instrument_identifier = self.config.get('Application', 'instrument_identifier')
        except ValueError as msg:
            print('Fatal ValueError : %s exiting.' % str(msg))
            # todo remove sys.exit and add UI status message.
            sys.exit(1)

        #  Load and initialise logging configuration from user configuration file.
        logging.config.fileConfig(self.config.conf_file, disable_existing_loggers=True)
        self.logger = logging.getLogger('main')
        self.logger.info('-------------- APPLICATION STARTUP --------------')

        # Load set instrument XML, selectedInstrument returns the relative path and XML file name.
        try:
            instruments = 'instruments' + os.path.sep + 'instruments.xml'
            my_instruments = xml_utilities.Instruments(instruments)
        except (FileNotFoundError, ValueError, LookupError) as msg:
            self.logger.critical('Unable to load instruments.xml %s' % str(msg))
            print('Unable to load instruments.xml %s exiting.' % str(msg))
            # todo remove sys.exit and add UI status message.
            sys.exit(1)
        else:
            try:
                filename = my_instruments.get_filename(self.instrument_identifier)
                filename = 'instruments' + os.path.sep + filename
                self.instrument = xml_utilities.Instrument(filename)
            except (FileNotFoundError, ValueError, LookupError) as msg:
                self.logger.critical('Unable to load instrument xml %s' % str(msg))
                print('Unable to load instrument xml %s exiting.' % str(msg))
                # todo remove sys.exit and add UI status message.
                sys.exit(1)
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
            print('Configuration ValueError : %s exiting.' % str(msg))
            # todo remove sys.exit and add UI status message.
            sys.exit(1)
        else:
            self.logger.debug('Initial parameter for instrument_autodetect : %s.' % instrument_autodetect)
            self.logger.debug('Initial parameter for instrument_data_path : %s.' % instrument_data_path)
            self.logger.debug('Initial parameter for starinet_relay_boolean : %s.' % starinet_relay_boolean)
            self.logger.debug('Initial parameter for starinet_address : %s.' % starinet_address)
            self.logger.debug('Initial parameter for starinet_port : %s.' % starinet_port)
            self.logger.debug('Initial parameter for serial_port : %s.' % serial_port)
            self.logger.debug('Initial parameter for serial_baudrate : %s.' % serial_baudrate)
            self.logger.debug('Initial parameter for serial_port_timeout : %s.' % serial_port_timeout)

        # Instrument autodetect initialisation.
        if instrument_autodetect == 'True':
            self.logger.info('Instrument autodetect is True.')
            if self.instrument.instrument_staribus_address == 'None':
                self.logger.warning('Instrument autodetect true however instrument appears to be Starinet so passing.')
                instrument_autodetect_status_boolean = False
            else:
                ports = utilities.serial_port_scanner()
                if ports is None:
                    self.logger.warning('No serial ports found to scan for instrument.')
                    instrument_autodetect_status_boolean = False
                else:
                    instrument_port = utilities.check_serial_port_staribus_instrument(
                        self.instrument.instrument_staribus_address, ports, serial_baudrate)
                    if instrument_port is None:
                        self.logger.warning('Staribus instrument not found for address %s' %
                                            self.instrument.instrument_staribus_address)
                        instrument_autodetect_status_boolean = False
                    elif len(instrument_port) > 1:
                        self.logger.warning('Multiple Staribus instruments found defaulting to first.')
                        self.logger.info('Setting serial port to %s' % instrument_port[0])
                        serial_port = instrument_port[0]
                        instrument_autodetect_status_boolean = True
                    else:
                        self.logger.info('Setting serial port to %s' % instrument_port)
                        serial_port = instrument_port[0]
                        instrument_autodetect_status_boolean = True

            if instrument_autodetect_status_boolean is True:
                try:
                    self.config.set('StaribusPort', 'staribus_port', serial_port)
                except (ValueError, IOError) as msg:
                    self.logger.critical('Fatal Error Unable to set serial port : %s' % msg)
                    print('Fatal Error Unable to set serial port : %s exiting.' % msg)
                    # todo remove sys.exit and add UI status message.
                    sys.exit(1)

        # Initialise Starinet relay.
        if starinet_relay_boolean == 'True' and instrument_autodetect == 'True':
            if instrument_autodetect_status_boolean is True:
                # todo UI status message.
                self.disable_all()
                starinet_connector.StarinetConnectorStart(starinet_address, starinet_port, serial_port, serial_baudrate,
                                                          serial_port_timeout)
                self.logger.info('Starinet relay initialised.')
            else:
                # todo UI status message
                self.disable_all()
                self.logger.warning('Starinet relay and Instrument autodetect are True but no Instrument found.')
                self.logger.critical('Starinet relay cannot initialise as serial port isn\'t set.')
        elif starinet_relay_boolean =='True':
            if serial_port is None:
                # todo UI status message.
                self.disable_all()
                self.logger.critical('Starinet relay cannot initialise as serial port isn\'t set.')
            else:
                # todo UI status message.
                self.disable_all()
                starinet_connector.StarinetConnectorStart(starinet_address, starinet_port, serial_port, serial_baudrate,
                                                          serial_port_timeout)
                self.logger.info('Starinet relay initialised.')

        # Initialise configurationManager
        self.configurationManager = config_utilities.ConfigManager()

        # Initialise Futurlec Baudrate tool
        self.futurlec_baudrate_tool = futurlec.FuturlecBaudrate()

        # Menu items
        self.logger.debug('Setting menu item triggers.')
        # self.ui.actionExit.triggered.connect(self.exit)
        # self.ui.actionConfiguration.triggered.connect(self.configuration_triggered)
        # self.ui.actionInstrumentBuilder.triggered.connect(self.instrument_builder_triggered)
        self.ui.actionControllerEditor.triggered.connect(self.futurlec_baudrate_tool_triggered)
        # self.ui.actionManual.triggered.connect(self.help_manual_triggered)
        # self.ui.actionAbout.triggered.connect(self.help_about_triggered)

        # Disable Parameter Entry, Choices Combobox and Execute Button
        self.ui.executeButton.setEnabled(False)
        self.ui.commandParameter.setEnabled(False)
        self.ui.choicesComboBox.setEnabled(False)

        # Module, Command and Choices ComboBox Triggers.
        self.ui.moduleCombobox.currentIndexChanged.connect(self.populate_ui_command)
        self.ui.commandCombobox.currentIndexChanged.connect(self.command_parameter_populate)

        # Parameter entry emit and connect signals
        self.ui.commandParameter.textChanged.connect(self.parameter_check_state)
        self.ui.commandParameter.textChanged.emit(self.ui.commandParameter.text())

        # Style sheets
        style_boolean = False

        if sys.platform.startswith('darwin'):
            stylesheet = 'css/macStyle.css'
            style_boolean = True
        elif sys.platform.startswith('win32'):
            stylesheet = 'css/winStyle.css'
            style_boolean = True
        elif sys.platform.startswith('linux'):
            stylesheet = 'css/nixStyle.css'
            style_boolean = True

        if style_boolean:
            with open(stylesheet, 'r') as style:
                self.setStyleSheet(style.read())

        # Base attributes.
        self.saved_data_state = False

        # Fire populate_ui_module for the first time.
        self.populate_ui_module()

        # Initialise Chart Control Panel
        self.chart_control_panel_populate()

    # ----------------------------------------
    # For here on is the UI populate methods.
    # ----------------------------------------

    def populate_ui_module(self):
        # populate module combobox.
        self.logger.debug('Populating module combobox')

        index = 0

        for plugin in self.instrument.module_list:
            self.logger.debug('Populate module combobox with : %s' % str(plugin))
            self.ui.moduleCombobox.addItem(plugin[0], plugin[2])
            self.ui.moduleCombobox.setItemData(index, plugin[1], QtCore.Qt.ToolTipRole)

            index += 1

    def populate_ui_command(self):
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

    # Get the command parameters for the current set command.
    def command_parameter_populate(self):

        # Check if command has choices.
        if self.instrument.command_dict[self.ui.commandCombobox.currentText()]['Parameters']['Choices'] == 'None':
            self.logger.debug('%s %s', self.ui.commandCombobox.currentText(), 'Parameters Choices : None')
            self.ui.choicesComboBox.clear()
            self.ui.choicesComboBox.setEnabled(False)
            self.ui.executeButton.setEnabled(True)
        else:
            self.ui.choicesComboBox.clear()
            self.ui.choicesComboBox.setEnabled(True)
            self.ui.executeButton.setEnabled(True)

            # Split the choices up into list.
            choices = \
                self.instrument.command_dict[self.ui.commandCombobox.currentText()]['Parameters']['Choices'].split(',')
            self.logger.debug('%s %s %s', self.ui.commandCombobox.currentText(), 'Parameters Choices :', str(choices))
            self.ui.choicesComboBox.addItems(choices)  # Add choices to combobox.

            # Add choices tool tips to combo box.
            for i in range(len(choices)):
                self.ui.choicesComboBox.setItemData(i,
                                                    self.instrument.command_dict[self.ui.commandCombobox.currentText()]
                                                    ['Parameters']['Tooltip'], QtCore.Qt.ToolTipRole)

        # Check if command has parameters.
        if self.instrument.command_dict[self.ui.commandCombobox.currentText()]['Parameters']['Regex'] == 'None':
            self.logger.debug('%s %s', self.ui.commandCombobox.currentText(), 'Parameters Regex : None')
            self.ui.commandParameter.clear()
            self.ui.commandParameter.setEnabled(False)
            self.ui.commandParameter.setStyleSheet('QLineEdit { background-color: #EBEBEB }')
        else:
            self.ui.commandParameter.setEnabled(True)
            self.ui.commandParameter.setStyleSheet('QLineEdit { background-color: #FFFFFF }')
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

    def chart_control_panel_populate(self):
        numChannels = self.instrument.instrument_number_of_channels

        self.ui.channel0Button.setEnabled(False)
        self.ui.channel1Button.setEnabled(False)
        self.ui.channel2Button.setEnabled(False)
        self.ui.channel3Button.setEnabled(False)
        self.ui.channel4Button.setEnabled(False)
        self.ui.channel5Button.setEnabled(False)
        self.ui.channel6Button.setEnabled(False)
        self.ui.channel7Button.setEnabled(False)
        self.ui.channel8Button.setEnabled(False)

        if numChannels == '2':
            self.ui.channel0Button.setText(self.instrument.channel_names[0])
            self.ui.channel1Button.setText(self.instrument.channel_names[1])
            self.ui.channel2Button.setVisible(False)
            self.ui.channel3Button.setVisible(False)
            self.ui.channel4Button.setVisible(False)
            self.ui.channel5Button.setVisible(False)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel8Button.setVisible(False)
        elif numChannels == '3':
            self.ui.channel0Button.setText(self.instrument.channel_names[0])
            self.ui.channel1Button.setText(self.instrument.channel_names[1])
            self.ui.channel2Button.setText(self.instrument.channel_names[2])
            self.ui.channel3Button.setVisible(False)
            self.ui.channel4Button.setVisible(False)
            self.ui.channel5Button.setVisible(False)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel8Button.setVisible(False)
        elif numChannels == '4':
            self.ui.channel0Button.setText(self.instrument.channel_names[0])
            self.ui.channel1Button.setText(self.instrument.channel_names[1])
            self.ui.channel2Button.setText(self.instrument.channel_names[2])
            self.ui.channel3Button.setText(self.instrument.channel_names[3])
            self.ui.channel4Button.setVisible(False)
            self.ui.channel5Button.setVisible(False)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel8Button.setVisible(False)
        elif numChannels == '5':
            self.ui.channel0Button.setText(self.instrument.channel_names[0])
            self.ui.channel1Button.setText(self.instrument.channel_names[1])
            self.ui.channel2Button.setText(self.instrument.channel_names[2])
            self.ui.channel3Button.setText(self.instrument.channel_names[3])
            self.ui.channel4Button.setText(self.instrument.channel_names[4])
            self.ui.channel5Button.setVisible(False)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel8Button.setVisible(False)
        elif numChannels == '6':
            self.ui.channel0Button.setText(self.instrument.channel_names[0])
            self.ui.channel1Button.setText(self.instrument.channel_names[1])
            self.ui.channel2Button.setText(self.instrument.channel_names[2])
            self.ui.channel3Button.setText(self.instrument.channel_names[3])
            self.ui.channel4Button.setText(self.instrument.channel_names[4])
            self.ui.channel5Button.setText(self.instrument.channel_names[5])
            self.ui.channel6Button.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel8Button.setVisible(False)
        elif numChannels == '7':
            self.ui.channel0Button.setText(self.instrument.channel_names[0])
            self.ui.channel1Button.setText(self.instrument.channel_names[1])
            self.ui.channel2Button.setText(self.instrument.channel_names[2])
            self.ui.channel3Button.setText(self.instrument.channel_names[3])
            self.ui.channel4Button.setText(self.instrument.channel_names[4])
            self.ui.channel5Button.setText(self.instrument.channel_names[5])
            self.ui.channel6Button.setText(self.instrument.channel_names[6])
            self.ui.channel7Button.setVisible(False)
            self.ui.channel8Button.setVisible(False)
        elif numChannels == '8':
            self.ui.channel0Button.setText(self.instrument.channel_names[0])
            self.ui.channel1Button.setText(self.instrument.channel_names[1])
            self.ui.channel2Button.setText(self.instrument.channel_names[2])
            self.ui.channel3Button.setText(self.instrument.channel_names[3])
            self.ui.channel4Button.setText(self.instrument.channel_names[4])
            self.ui.channel5Button.setText(self.instrument.channel_names[5])
            self.ui.channel6Button.setText(self.instrument.channel_names[6])
            self.ui.channel7Button.setText(self.instrument.channel_names[7])
            self.ui.channel8Button.setVisible(False)
        elif numChannels == '9':
            self.ui.channel0Button.setText(self.instrument.channel_names[0])
            self.ui.channel1Button.setText(self.instrument.channel_names[1])
            self.ui.channel2Button.setText(self.instrument.channel_names[2])
            self.ui.channel3Button.setText(self.instrument.channel_names[3])
            self.ui.channel4Button.setText(self.instrument.channel_names[4])
            self.ui.channel5Button.setText(self.instrument.channel_names[5])
            self.ui.channel6Button.setText(self.instrument.channel_names[6])
            self.ui.channel7Button.setText(self.instrument.channel_names[7])
            self.ui.channel8Button.setText(self.instrument.channel_names[8])

    # ----------------------------------------
    # Parameter check state method.
    # ----------------------------------------

    def parameter_check_state(self, *args, **kwargs):

        self.logger.debug('################ PARAMETER CHECK STATE ################')

        # This bit is a bit of bodge as parameter check state will trigger when loading and raise
        # AttributeError so we just ignore it, not ideal!

        try:
            sender = self.sender()
            validator = sender.validator()
            state = validator.validate(sender.text(), 0)[0]
        except AttributeError:
            pass

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
            self.logger.debug('Command parameters key error setting parameter entry box to gray')
            sender.setStyleSheet('QLineEdit { background-color: #EDEDED }')

    # ----------------------------------------
    # Disable ui controls method.
    # ----------------------------------------

    def disable_all(self):
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
    # Menu trigger methods.
    # ----------------------------------------

    def futurlec_baudrate_tool_triggered(self):
        self.logger.debug('Calling futurlec baudrate configuration tool.')
        self.futurlec_baudrate_tool.exec_()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = Main()
    myapp.setWindowTitle('Starbase-Mini -- Ver %s' % version)
    myapp.showMaximized()
    myapp.show()
    x = app.exec_()
    sys.exit(x)