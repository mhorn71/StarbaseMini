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

version = '0.0.1'


class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):

        # Initialise configuration.
        try:
            self.config = config_utilities.ConfigTool()
        except FileNotFoundError as msg:
            print('Fatal FileNotFoundError : %s' % str(msg))
            sys.exit(1)
        except OSError as msg:
            print('Fatal OSError : %s' % str(msg))
            sys.exit(1)

        # Generate user configuration if it's missing.
        try:
            self.config.check_conf_exists()
        except IOError as msg:
            print('Fatal IOError : %s' % str(msg))
            sys.exit(1)

        # Get instrument name from configuration.
        try:
            self.instrument_name = self.config.get('Application', 'instrument_name')
        except ValueError as msg:
            print('Fatal ValueError : %s' % str(msg))

        #  Load and initialise logging configuration from user configuration file.
        logging.config.fileConfig(self.config.conf_file, disable_existing_loggers=True)
        self.logger = logging.getLogger('main')
        self.logger.info('-------------- APPLICATION STARTUP --------------')

        # Load set instrument XML, selectedInstrument returns the relative path and XML file name.
        try:
            instruments = 'instruments' + os.path.sep + 'instruments.xml'
            my_instruments = xml_utilities.Instruments(instruments)
        except FileNotFoundError as msg:
            self.logger.critical('Unable to load instruments.xml %s' % str(msg))
            print('Unable to load instruments.xml %s' % str(msg))
            sys.exit(1)
        except ValueError as msg:
            self.logger.critical('Unable to load instruments.xml %s' % str(msg))
            print('Unable to load instruments.xml %s' % str(msg))
            sys.exit(1)
        except LookupError as msg:
            self.logger.critical('Unable to load instruments.xml %s' % str(msg))
            print('Unable to load instruments.xml %s' % str(msg))
            sys.exit(1)
        else:
            try:
                file_name = my_instruments.get_file(self.instrument_name)
                file_name = 'instruments' + os.path.sep + file_name
                self.instrument = xml_utilities.Instrument(file_name)
            except FileNotFoundError as msg:
                self.logger.critical('Unable to load instrument xml %s' % str(msg))
                print('Unable to load instrument xml %s' % str(msg))
                sys.exit(1)
            except ValueError as msg:
                self.logger.critical('Unable to load instrument xml %s' % str(msg))
                print('Unable to load instrument xml %s' % str(msg))
                sys.exit(1)
            except LookupError as msg:
                self.logger.critical('Unable to load instrument xml %s' % str(msg))
                print('Unable to load instrument xml %s' % str(msg))
                sys.exit(1)
            else:
                self.logger.info('Instrument XML loaded for %s', self.instrument_name)

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


        # Base attributes.
        self.saved_data_state = False


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = Main()
    myapp.setWindowTitle('Starbase-Mini -- Ver %s' % version)
    myapp.showMaximized()
    myapp.show()
    x = app.exec_()
    sys.exit(x)