__author__ = 'mark'
# StarbaseMini Staribus/Starinet Client for the British Astronomical Association Staribus Protocol
# Copyright (C) 2016  Mark Horn
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
import logging
import csv

from PyQt5 import QtWidgets


def exporter(type, metadata, data_store, user_home, data_home):

    logger = logging.getLogger('core.exporter')

    # Default filename

    if type == 'processed':

        filename = 'ProcessedData_' + datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")

        data_source = data_store.ProcessedData

        if len(data_source) == 0:

            return 'PREMATURE_TERMINATION', 'No processed data to export.'

    else:

        filename = 'RawData_' + datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")

        data_source = data_store.RawData

        if len(data_source) == 0:

            return 'PREMATURE_TERMINATION', 'No raw data to export.'

    # Check if instrument data path exists and if so open folder to choose file.

    if os.path.isdir(data_home):

        data_file = data_home + os.path.sep + filename

    else:

        data_file = user_home + os.path.sep + filename

    file_name = QtWidgets.QFileDialog.getSaveFileName(None, 'Export File', data_file, "CSV files (*.csv)")

    print(file_name)

    # Return ABORT if no File selected.

    if file_name[0] == '':

        return 'ABORT', None

    else:

        with open(file_name[0], "w", newline='') as csv_file:

            data_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for i in metadata.metadata_creator(data_store.DataSource):

                data_writer.writerow(i)

            for data in data_source.tolist():

                date, time = data[0].strftime('%Y-%m-%d,%H:%M:%S').split(',')

                data[0] = date
                data.insert(1, time)

                data_writer.writerow(data)

        csv_file.close()

        logger.info('File Exported : %s' % file_name[0])

        if type == 'processed':

            data_store.ProcessedDataSaved = True

            logger.info('ProcessDataSaved set to True')

        else:

            data_store.RawDataSaved = True

            logger.info('RawDataSaved set to True')

        return 'SUCCESS', file_name[0]