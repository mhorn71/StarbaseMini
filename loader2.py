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
from ui import Ui_MainWindow
import xml_utilities
import config_utilities
import starinet_connector

version = '0.0.1'


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
                self.logger.critical('Starinet relay cannot initialise as serial port isn\'t set.')
            else:
                # todo UI status message.
                self.disable_all()
                starinet_connector.StarinetConnectorStart(starinet_address, starinet_port, serial_port, serial_baudrate,
                                                          serial_port_timeout)
                self.logger.info('Starinet relay initialised.')

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


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = Main()
    myapp.setWindowTitle('Starbase-Mini -- Ver %s' % version)
    myapp.showMaximized()
    myapp.show()
    x = app.exec_()
    sys.exit(x)