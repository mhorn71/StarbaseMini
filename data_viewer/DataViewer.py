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

import logging
import sys

from PyQt4 import QtGui, QtCore

from ui import Ui_DataViewerDialog

class DataViewer(QtGui.QDialog, Ui_DataViewerDialog):
    def __init__(self, data_store):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.data_store = data_store

    def load(self, type):

        if type == 'processed':

            self.setWindowTitle('Processed Data Viewer')

        else:

            self.setWindowTitle('Raw Data Viewer')