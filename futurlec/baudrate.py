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
import logging

from PyQt4 import QtGui

from ui import Ui_FuturlecDialog
import config_utilities
import dao

logger = logging.getLogger('futurlec.baudrate')


class FuturlecBaudrate(QtGui.QDialog, Ui_FuturlecDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

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

        self.application_conf = config_utilities.ConfigTool()

        self.FindInstButton.setFocus()

        self.baudrates = ['9600', '19200', '38400', '57600', '115200']

        # Set baudrate check box and combo box.
        baudrate = self.application_conf.get('StaribusPort', 'baudrate')

        if baudrate == '57600':
            self.defaultCheckBox.setChecked(True)
            self.baudrateComboBox.setEnabled(False)  # Disable combo box if default set.

        self.defaultCheckBox.setToolTip('Sets the default baudrate to 57600')

        self.baudrateComboBox.addItems(self.baudrates)
        self.baudrateComboBox.setCurrentIndex(self.baudrates.index(baudrate))