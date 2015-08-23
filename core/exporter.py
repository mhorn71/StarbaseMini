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
import datetime

from PyQt4 import QtGui

import config_utilities


def exporter(datatranslator, number_of_channels, metadata):

    # First get instrument data path from configuration.
    App_Config = config_utilities.ConfigTool()
    data_path = App_Config.get('Application', 'instrument_data_path')

    # Get home path in case instrument data path isn't set.
    home = os.path.expanduser("~")

    # Default filename
    filename = 'RawData_' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Check if instrument data path exists and if so open folder to choose file.
    if os.path.isdir(data_path):
        data_file = data_path + os.path.sep + filename
    else:
        data_file = home + os.path.sep + filename

    fname = QtGui.QFileDialog.getSaveFileName(None, 'Export File', data_file, "CSV files (*.csv)")

    # Return ABORT if no File selected.
    if fname == '':
        return 'ABORT', None
    else:

        # todo add csv creation routine here.

        try:
            file = open(fname, 'a+')
        except IOError as msg:
            return 'PREMATURE_TERMINATION', 'Unable to create file'
            # todo add logger
        else:
            try:
                observatory_metadata = metadata.observatory_metadata()
                if observatory_metadata is not None:
                    file.write(observatory_metadata)

                observer_metadata = metadata.observer_metadata()
                if observer_metadata is not None:
                    file.write(observer_metadata)

                observation_metadata = metadata.observation_metadata()
                if observation_metadata is not None:
                    file.write(observation_metadata)

                file.close()
            except IOError as msg:
                return 'PREMATURE_TERMINATION', 'Unable to create file'
                # todo add logger
            else:
                return 'SUCCESS', fname

