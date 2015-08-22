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

import os

from PyQt4 import QtGui

import config_utilities


def importer():

    # First get instrument data path from configuration.
    App_Config = config_utilities.ConfigTool()
    data_path = App_Config.get('Application', 'instrument_data_path')

    # Get home path in case instrument data path isn't set.
    home = os.path.expanduser("~")

    # Check if instrument data path exists and if so open folder to choose file.
    if os.path.isdir(data_path):
        fname = QtGui.QFileDialog.getOpenFileName(None, 'Import File', data_path, "CSV files (*.csv)")
    else:
        fname = QtGui.QFileDialog.getOpenFileName(None, 'Import File', home, "CSV files (*.csv)")

    # Return ABORT if no File selected.
    if fname == '':
        return 'ABORT', None
    else:
        return 'SUCCESS', fname



