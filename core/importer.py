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
import logging

from PyQt4 import QtGui


def importer(user_home, data_home):

    logger = logging.getLogger('core.importer')

    # Check if instrument data path exists and if so open folder to choose file.

    try:

        if os.path.isdir(data_home):

            file_name = QtGui.QFileDialog.getOpenFileName(None, 'Import File', data_home, "CSV files (*.csv)")

            logger.debug('Data path set to : ' + data_home)

        else:

            file_name = QtGui.QFileDialog.getOpenFileName(None, 'Import File', user_home, "CSV files (*.csv)")

            logger.debug('Data path set to : ' + user_home)

    except TypeError:

        file_name = QtGui.QFileDialog.getOpenFileName(None, 'Import File', user_home, "CSV files (*.csv)")

        logger.debug('Data path set to : ' + user_home)

    # Return ABORT if no File selected.

    if file_name == '':

        logger.debug('No file selected ABORT.')

        return 'ABORT', None

    else:

        logger.debug('User has selected file : %s' % file_name)

        return 'SUCCESS', file_name