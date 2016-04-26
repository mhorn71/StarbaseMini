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
import csv
import logging
import re

from PyQt4 import QtGui

import config_utilities


def importer(datatranslator, metadata):

    logger = logging.getLogger('core.importer')
    
    # First get instrument data path from configuration.
    App_Config = config_utilities.ConfigLoader()
    data_path = App_Config.get('Application', 'instrument_data_path')

    obser_trip = 0
    date_trip = 0

    # Get home path in case instrument data path isn't set.
    home = os.path.expanduser("~")

    # Check if instrument data path exists and if so open folder to choose file.
    try:
        if os.path.isdir(data_path):
            fname = QtGui.QFileDialog.getOpenFileName(None, 'Import File', data_path, "CSV files (*.csv)")
            logger.debug('Data path set to : ' + data_path)
        else:
            fname = QtGui.QFileDialog.getOpenFileName(None, 'Import File', home, "CSV files (*.csv)")
            logger.debug('Data path set to : ' + home)
    except TypeError:
        fname = QtGui.QFileDialog.getOpenFileName(None, 'Import File', home, "CSV files (*.csv)")
        logger.debug('Data path set to : ' + home)

    # Return ABORT if no File selected.
    if fname == '':
        logger.debug('No file selected ABORT.')
        return 'ABORT', None
    else:
        datatranslator.clear()
        logger.debug('Datatranslator clear called.')
        metadata.clear()
        logger.debug('Metadata clear called.')
        try:
            with open(fname) as csvfile:
                logger.debug('Opening file : ' + fname)
                reader = csv.reader(csvfile)
                logger.debug('CSV reader called.')
                for row in reader:
                    if len(row) == 0:  # bodge for windows as we seems to get a row of zero length sometimes
                        logger.debug('Zero length row found ignoring.')
                        pass
                    else:
                        if row[0].startswith('Obser'):
                            obser_trip += 1
                            metadata.meta_parser(row)
                        elif re.match('^\d\d\d\d-\d\d-\d\d$', row[0]):
                            date_trip += 1

                            if metadata.instrument_number_of_channels is None:
                                logger.critical('Unable to locate observation channel count')
                                return 'PREMATURE_TERMINATION', 'Unable to locate observation channel count'

                            if datatranslator.csv_parser(row, metadata.instrument_number_of_channels):
                                pass
                            else:
                                logger.critical('Unable to parse row :%s' % str(row))
                                return 'PREMATURE_TERMINATION', 'Unable to parse data'
                        else:
                            logger.debug('No valid rows found.')
                            pass

                if obser_trip == 0:
                    logger.warning('No row starting with Obser!!!')
                else:
                    logger.debug('Found %s rows starting with Obser.' % str(obser_trip))

                if date_trip == 0:
                    logger.warning('No row starting with date!!!')
                else:
                    logger.debug('Found %s rows starting with date.' % str(date_trip))

        except IOError as msg:
            logger.critical(str(msg))
            return 'PREMATURE_TERMINATION', 'Unable to open file.'
        else:
            if (len(datatranslator.datetime)) == 0:
                return 'PREMATURE_TERMINATION', 'No data found.'
            else:
                return 'SUCCESS', fname




