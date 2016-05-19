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

from PyQt4 import QtGui


def exporter(type, metadata_creator, data_store, user_home, data_home):

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

    file_name = QtGui.QFileDialog.getSaveFileName(None, 'Export File', data_file, "CSV files (*.csv)")

    # Return ABORT if no File selected.

    if file_name == '':

        return 'ABORT', None

    else:

        csv = ''

        # for each list in data_store.RawData

        for lista in data_source:

            # Convert from numpy array to normal list

            lista.tolist()

            # Convert datatime object in to formatted string.

            date = lista[0].strftime('%Y-%m-%d,%H:%M:%S')

            # For all data exluding the datatime object join it together with a comma

            data = ','.join(lista[1:])

            # Add carriage return and line feed to data

            data += '\r\n'

            # Append date and data to csv

            csv += date + ',' + data

        if len(csv) == 0:

            return 'PREMATURE_TERMINATION', 'Unable to create csv from data.'

        else:

            try:

                file = open(file_name, 'w')

            except IOError as msg:

                logger.critical(str(msg))

                return 'PREMATURE_TERMINATION', ('Unable to create file : %s' % file_name)

            else:

                if data_store.DataSource == 'CSV':

                    if len(data_store.MetadataCsv) != 0:

                        for listb in data_store.MetadataCsv:

                            file.write(listb + '\r\n')

                elif data_store.DataSource == 'Controller':

                    if metadata_creator.observatory_metadata() is not None:

                        file.write(metadata_creator.observatory_metadata())

                    if metadata_creator.observer_metadata() is not None:

                        file.write(metadata_creator.observer_metadata())

                    if metadata_creator.observation_metadata() is not None:

                        file.write(metadata_creator.observation_metadata())

                    if data_store.ObserverationNoteMetadata is not None:

                        file.write(data_store.ObserverationNoteMetadata)

            file.write(csv)

            file.close()

            logger.info('File Exported : %s' % file_name)

            if type == 'processed':

                data_store.ProcessedDataSaved = True

                logger.info('ProcessDataSaved set to True')

            else:

                data_store.RawDataSaved = True

                logger.info('RawDataSaved set to True')

            return 'SUCCESS', file_name