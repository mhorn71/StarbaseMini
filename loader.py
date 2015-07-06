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
import core.starinetConnector as starinetConnector
from core.configLoader import confLoader
from core.ui.mainwindow import Ui_MainWindow
from core.xmlLoad import Instrument
from core.instrumentChooser import selectedInstrument


version = '0.0.18'

class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):

        # Initialise configuration will auto generate user configuration if missing.
        self.config = confLoader()

        #  Load and initialise logging configuration from user configuration file.
        logging.config.fileConfig(self.config.conf_file, disable_existing_loggers=False)
        self.logger = logging.getLogger('loader')
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

        self.ui.moduleCombobox.currentIndexChanged.connect(self.module_combo_triggered)

        self.saved_data_state = False
        self.command_base = ''
        self.command_code = ''
        self.command_variant = ''

        # If StarinetConnector is set then initialise starinetConnector.
        if self.config.get('StarinetConnector', 'active') == 'True':

            self.logger.info('Initialising StarinetConnector')

            # Check IP and Port look sane.
            if utils.ip_checker(self.config.get('StarinetConnector', 'address')):
                self.ui_message('Starinet Connector Address Malformed!!')

            if utils.port_checker(self.config.get('StarinetConnector', 'port')):
                self.ui_message('Starinet Connect Port Malformed')

            # Disable Normal GUI Operation as we're acting as Starinet Connector.
            self.disable()

            connector = starinetConnector.connector(self)

        elif self.config.get('StarinetConnector', 'active') == 'False':

            # Initialise instrument configuration.
            self.logger.info('Initialising Instrument.')

            # Load set instrument XML, selectedInstrument returns the relative path and XML file name.
            self.instrument = Instrument(selectedInstrument(self))

            # Populate the UI Combo boxes and set initial state.
            self.populate_ui_module()

        else:

            self.logger.critical('Unable to parse configuration for StarinetConnector.')
            utils.exit_message('Unable to parse configuration for StarinetConnector.')

    def disable(self):
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
        self.ui_message('StarinetConnector Mode | Instrument Control Panel Disabled.')

    def populate_ui_module(self):
        # populate module combobox.
        self.logger.debug('Populating module combobox')

        index = 0

        for plugin in self.instrument.instrument_mc_list:
            self.ui.moduleCombobox.addItem(plugin[0], plugin[2])
            self.ui.moduleCombobox.setItemData(index, plugin[1], QtCore.Qt.ToolTipRole)

            index += 1

        self.ui_message('Instrument PopulateUI')

    def populate_ui_command(self):

        self.ui.commandCombobox.clear()

        index = 0

        for plugin in self.instrument.instrument_mc_list:
            if self.command_base in plugin:
                for command in plugin[3:]:
                    self.ui.commandCombobox.addItem(command[0], (command[1], command[2]))
                    self.ui.commandCombobox.setItemData(index, command[3], QtCore.Qt.ToolTipRole)
                    # We need some bits in here to look for choices or parameters.

    def module_combo_triggered(self):
        # Module Combo Box Changed, set new command_base
        self.command_base = self.ui.moduleCombobox.itemData(self.ui.moduleCombobox.currentIndex())
        self.logger.debug('Command base set to %s' % self.command_base)

        self.populate_ui_command()

    # Just a break for space. ;-))


    def ui_message(self, message):
        message = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' | ' + message
        self.ui.statusMessage.setText(message)

    def configuration_triggered(self):
        pass

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
