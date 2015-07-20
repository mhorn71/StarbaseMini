__author__ = 'mark'

import sys
import logging.config
import logging
import datetime

from PyQt4 import QtGui, QtCore

try:
    from PyQt4.QtCore import QString
except ImportError:
    QString = str

import core.utilities as utils
from core.configLoader import confLoader
from core.configTool import configManager
import core.staribusPortDetect as staribusPortDetect
from core.ui.mainwindow import Ui_MainWindow
from core.xmlLoad import Instrument
from core.xmlLoad import Instruments


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
        self.config = confLoader()

        #  Load and initialise logging configuration from user configuration file.
        logging.config.fileConfig(self.config.conf_file, disable_existing_loggers=True)
        self.logger = logging.getLogger('main')
        self.logger.info('-------------- APPLICATION STARTUP --------------')

        # Load Ui Components we need to do this before we check for connector or we won't be able to disable the UI
        # components.

        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Menu items
        self.logger.debug('Setting menu item triggers.')
        self.ui.actionExit.triggered.connect(self.exit)
        self.ui.actionConfiguration.triggered.connect(self.configuration_triggered)
        self.ui.actionMetadataEditor.triggered.connect(self.metadata_editor_triggered)
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
        my_instrument = Instruments()
        file_name = my_instrument.get_file(self.config.get('Application', 'instrument_name'))
        self.instrument = Instrument(file_name)

        if self.config.get('Application', 'detect_staribus_port') == 'True' and \
                self.instrument.instrument_staribus_address != 'None':
            address = self.instrument.instrument_staribus_address
            baudrate = self.config.get('StaribusPort', 'baudrate')
            staribusPortDetect.autodetect(address, baudrate)

        # If StarinetConnector is set then initialise starinetConnector.
        if self.config.get('StarinetConnector', 'active') == 'True':

            self.logger.info('Initialising StarinetConnector')

            if len(self.config.get('StaribusPort', 'port')) == 0:
                self.logger.critical('No Staribus port set.')
                critical = True

            ip = self.config.get('StarinetConnector', 'address')
            port = self.config.get('StarinetConnector', 'port')

            # Check IP and Port look sane.
            if utils.ip_checker(ip):
                pass
            else:
                self.logger.critical('Starinet Connector Address Malformed!!')
                critical = True

            if utils.port_checker(port):
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
            utils.exit_message('Unable to parse configuration for StarinetConnector.')

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
        self.configurationManager = configManager()

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

        for plugin in self.instrument.instrument_mc_list:
            self.ui.moduleCombobox.addItem(plugin[0], plugin[2])
            self.ui.moduleCombobox.setItemData(index, plugin[1], QtCore.Qt.ToolTipRole)

            index += 1

    def populate_ui_command(self):

        self.ui.commandCombobox.clear()

        index = 0

        for plugin in self.instrument.instrument_mc_list:
            if self.command_base in plugin:
                for command in plugin[3:]:
                    self.ui.commandCombobox.addItem(command[0])
                    self.ui.commandCombobox.setItemData(index, command[3], QtCore.Qt.ToolTipRole)

                    index += 1

        self.command_parameter_populate()

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

    # Just a break for space. ;-))

    def execute_triggered(self):
        print(self.ui.commandCombobox.itemData(self.ui.commandCombobox.currentIndex()))

    def ui_message(self, message):
        message = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' :: ' + message
        self.ui.statusMessage.setText(message)

    def configuration_triggered(self):
        self.logger.info('Calling configuration tool.')
        self.configurationManager.exec_()

    def metadata_editor_triggered(self):
        pass

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
