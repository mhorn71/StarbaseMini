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

import utilities
from core import InstrumentBuilder
from core import Baudrate
from ui import Ui_MainWindow
import xml_utilities
import config_utilities


version = '0.0.19'


class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):

        # Base attributes.
        self.saved_data_state = False
        self.command_base = 'None'
        self.command_code = 'None'
        self.command_variant = 'None'
        self.command_name = 'None'
        self.parameter_units = 'None'
        self.parameter_regex = 'None'

        # Initialise configuration will auto generate user configuration if missing.
        self.config = config_utilities.ConfigTool()

        #  Load and initialise logging configuration from user configuration file.
        logging.config.fileConfig(self.config.conf_file, disable_existing_loggers=True)
        self.logger = logging.getLogger('main')
        self.logger.info('-------------- APPLICATION STARTUP --------------')

        # Load Ui Components we need to do this before we check for connector or we won't be able to disable the UI
        # components.

        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


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

        # Menu items
        self.logger.debug('Setting menu item triggers.')
        self.ui.actionExit.triggered.connect(self.exit)
        self.ui.actionConfiguration.triggered.connect(self.configuration_triggered)
        self.ui.actionInstrumentBuilder.triggered.connect(self.instrument_builder_triggered)
        self.ui.actionControllerEditor.triggered.connect(self.futurlec_tool_triggered)
        self.ui.actionManual.triggered.connect(self.help_manual_triggered)
        self.ui.actionAbout.triggered.connect(self.help_about_triggered)

        # Button connectors
        self.ui.executeButton.clicked.connect(self.execute_triggered)

        # Disable Parameter Entry, Choices Combobox and Execute Button
        self.ui.executeButton.setEnabled(False)
        self.ui.commandParameter.setEnabled(False)
        self.ui.choicesComboBox.setEnabled(False)

        # Module, Command and Choices ComboBox Triggers.
        self.ui.moduleCombobox.currentIndexChanged.connect(self.module_combo_triggered)
        self.ui.commandCombobox.currentIndexChanged.connect(self.command_parameter_populate)

        # Parameter entry emit and connect signals
        self.ui.commandParameter.textChanged.connect(self.parameter_check_state)
        self.ui.commandParameter.textChanged.emit(self.ui.commandParameter.text())

        # Load set instrument XML, selectedInstrument returns the relative path and XML file name.
        try:
            instruments = 'instruments' + os.path.sep + 'instruments.xml'
            my_instruments = xml_utilities.Instruments(instruments)
        except FileNotFoundError as msg:
            self.logger.critical('Unable to load instruments.xml %s' % str(msg))
            print('Unable to load instruments.xml %s' % str(msg))
            sys.exit(1)
        else:
            try:
                file_name = my_instruments.get_file(self.config.get('Application', 'instrument_name'))
                file_name = 'instruments' + os.path.sep + file_name
                self.instrument = xml_utilities.Instrument(file_name)
            except FileNotFoundError as msg:
                self.logger.critical('Unable to load instrument xml %s' % str(msg))
                print('Unable to load instrument xml %s' % str(msg))
                sys.exit(1)

        if self.config.get('Application', 'detect_staribus_port') == 'True' and \
                self.instrument.instrument_staribus_address != 'None':
            address = self.instrument.instrument_staribus_address
            baudrate = self.config.get('StaribusPort', 'baudrate')
            ports = utilities.serial_port_scanner()

            if ports is not None:
                instrument_port = utilities.check_serial_port_staribus_instrument(address, ports, baudrate)

                if instrument_port > 1:
                    self.logger.warn('More than one instrument found please set serial port by hand.')

            # Need bit here to set instrument port in configuration.

        # If StarinetConnector is set then initialise starinetConnector.
        if self.config.get('StarinetConnector', 'active') == 'True':

            self.logger.info('Initialising StarinetConnector')

            if len(self.config.get('StaribusPort', 'port')) == 0:
                self.logger.critical('No Staribus port set.')
                critical = True

            ip = self.config.get('StarinetConnector', 'address')
            port = self.config.get('StarinetConnector', 'port')

            # Check IP and Port look sane.
            if utilities.check_ip(ip):
                pass
            else:
                self.logger.critical('Starinet Connector Address Malformed!!')
                critical = True

            if utilities.check_starinet_port(port):
                pass
            else:
                self.logger.critical('Starinet Connect Port Malformed')
                critical = True

            # Disable Normal GUI Operation as we're acting as Starinet Connector.
            self.disable_all()

            if critical is True:
                self.ui_message('Check log file critical error has occurred.')
            else:
                self.ui_message('StarinetConnector Mode :: Instrument Control Panel Disabled.')

            connectorBool = True

            # Load the starinetConnector
            try:
                import core.streams.starinetConnector
            except Exception:
                pass

        elif self.config.get('StarinetConnector', 'active') == 'False':

            # Initialise instrument configuration.
            self.logger.info('Initialising Instrument.')

            # Populate the UI Combo boxes and set initial state.
            self.populate_ui_module()

            connectorBool = False

        else:

            self.logger.critical('Unable to parse configuration for StarinetConnector.')
            # utils.exit_message('Unable to parse configuration for StarinetConnector.')

        # Check if connector is being used.
        if connectorBool:
            pass
        else:
            # Check is staribus address is set and if so initiate Starbus transport.
            if self.instrument.instrument_staribus_address != 'None':
                if len(self.config.get('StaribusPort', 'port')) == 0:
                    self.logger.critical('No Staribus port set.')
                    self.ui_message('Check log file critical error has occurred.')
                else:
                    self.ui_message('Staribus instrument initialised.')
            elif self.instrument.instrument_starinet_address != 'None':
                self.ui_message('Starinet instrument initialised.')
            else:
                self.ui_message('Unable to parse either Staribus or Starinet instrument.  Check log file.')

        # Initialise configurationManager
        self.configurationManager = config_utilities.ConfigManager()

        # Initialise instrumentBuilder
        self.instrumentBuilder = InstrumentBuilder()

        # Initialise Futurlec Baudrate tool
        self.futurlec_tool = Baudrate()

        # Initialise Chart Control Panel
        self.chart_control_panel_populate()

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

    def populate_ui_module(self):
        # populate module combobox.
        self.logger.debug('Populating module combobox')

        index = 0

        for plugin in self.instrument.module_list:
            self.ui.moduleCombobox.addItem(plugin[0], plugin[2])
            self.ui.moduleCombobox.setItemData(index, plugin[1], QtCore.Qt.ToolTipRole)

            index += 1

    def populate_ui_command(self):

        plugin_index = self.ui.moduleCombobox.currentIndex()

        self.ui.commandCombobox.clear()

        print(self.instrument.command_list[plugin_index])

        index = 0

        # for cmd in self.instrument.command_list[plugin_index]:
        #     self.ui.commandCombobox.addItem(cmd[0])
        #
        # for plugin in self.instrument.instrument_mc_list:
        #     if self.command_base in plugin:
        #         for command in plugin[3:]:
        #             self.ui.commandCombobox.addItem(command[0])
        #             self.ui.commandCombobox.setItemData(index, command[3], QtCore.Qt.ToolTipRole)
        #
        #             index += 1
        #
        # self.command_parameter_populate()

    # Get the command parameters for the current set command.
    def command_parameter_populate(self):
        # Find the current set module in the instrument_mc_list
        for plugin in self.instrument.instrument_mc_list:
            if plugin[0] == self.ui.moduleCombobox.currentText():
                # Find the current set command in the instrument_mc_list plugin command lists.
                for command_list in plugin:
                    if command_list[0] == self.ui.commandCombobox.currentText():
                        self.command_name = command_list[0]
                        self.command_code = command_list[1]
                        self.command_variant = command_list[2]

                        # Check if command has choices.
                        if command_list[7] == 'None':
                            self.ui.choicesComboBox.clear()
                            self.ui.choicesComboBox.setEnabled(False)
                            self.ui.executeButton.setEnabled(True)
                        else:
                            self.ui.choicesComboBox.clear()
                            self.ui.choicesComboBox.setEnabled(True)
                            self.ui.executeButton.setEnabled(True)
                            choices = command_list[7].split(',')  # Split the choices up into list.
                            self.ui.choicesComboBox.addItems(choices)  # Add choices to combobox.

                            # Add choices tool tips to combo box.
                            for i in range(len(choices)):
                                self.ui.choicesComboBox.setItemData(i, command_list[9], QtCore.Qt.ToolTipRole)

                        # Check if command has parameters.
                        if command_list[8] == 'None':
                            self.ui.commandParameter.clear()
                            self.ui.commandParameter.setEnabled(False)
                            self.ui.commandParameter.setStyleSheet('QLineEdit { background-color: #EBEBEB }')
                        else:
                            self.ui.commandParameter.setEnabled(True)
                            self.ui.commandParameter.setStyleSheet('QLineEdit { background-color: #FFFFFF }')
                            self.ui.executeButton.setEnabled(False)
                            self.ui.commandParameter.setToolTip(command_list[9])
                            self.parameter_regex = command_list[8]
                            regexp = QtCore.QRegExp(self.parameter_regex)
                            validator = QtGui.QRegExpValidator(regexp)
                            self.ui.commandParameter.setValidator(validator)

    def module_combo_triggered(self):
        # Module Combo Box Changed, set new command_base
        self.command_base = self.ui.moduleCombobox.itemData(self.ui.moduleCombobox.currentIndex())
        self.logger.debug('Command base set to %s' % self.command_base)

        self.populate_ui_command()

    def parameter_check_state(self, *args, **kwargs):

        self.logger.debug('################ PARAMETER CHECK STATE ################')

        self.logger.debug('%s %s', 'Check state function run for command', self.command_name)

        # This bit is a bit of bodge as parameter check state will trigger when loading and raise
        # AttributeError so we just ignore it, not ideal!

        try:
            sender = self.sender()
            validator = sender.validator()
            state = validator.validate(sender.text(), 0)[0]
        except AttributeError:
            pass

        if self.parameter_regex == 'None':

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

    # Just a break for space. ;-))

    def execute_triggered(self):
        print(self.ui.commandCombobox.itemData(self.ui.commandCombobox.currentIndex()))

    def ui_message(self, message):
        message = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' :: ' + message
        self.ui.statusMessage.setText(message)

    def configuration_triggered(self):
        self.logger.info('Calling configuration tool.')
        self.configurationManager.exec_()

    def instrument_builder_triggered(self):
        self.logger.info('Calling instrument builder.')
        self.instrumentBuilder.exec_()

    def futurlec_tool_triggered(self):
        self.logger.info('Calling futurlec baudrate configuration tool.')
        self.futurlec_tool.exec_()

    def help_manual_triggered(self):
        pass

    def help_about_triggered(self):
        pass

    def exit(self):
        # if self.saved_data_state is False and len(self.datastore.raw_datastore) == 0:
        if self.saved_data_state is False:
            message = 'Are you sure you want to quit?'
        else:
            message = 'WARNING:  You have unsaved data.\nAre you sure you want to quit?'

        reply = QtGui.QMessageBox.question(self, 'Message',
            message, QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.logger.info('Client exit')
            sys.exit(0)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = Main()
    myapp.setWindowTitle('Starbase-Mini -- Ver %s' % version)
    myapp.showMaximized()
    myapp.show()
    x = app.exec_()
    sys.exit(x)
