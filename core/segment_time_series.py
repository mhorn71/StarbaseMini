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
import re
import logging


class SegmentTimeSeries:
    def __init__(self):
        logger = logging.getLogger('core.segmentTimeSeries')

        self.metadata_creator = None

        self.data_store = None

        self.data_home = None

        self.file_name = None

        self.write_file_name = None

        self.csv = ''

        logger.debug('Initialised SegmentTimeSeries')

    # def data_setup(self, datatranslator, source, metadata, data_type):
    def data_setup(self, metadata_creator, data_store, user_home, data_home):

        logger = logging.getLogger('core.segmentTimeSeries.data_setup')

        self.metadata_creator = metadata_creator

        if os.path.isdir(data_home):

            self.data_home = data_home

        else:

            self.data_home = user_home

        logger.debug('Data home set to : %s' % str(self.data_home))

        self.data_store = data_store

    def segment_timeseries(self, type, period):

        logger = logging.getLogger('core.segmentTimeSeries.segment_timeseries')

        # Make sure self.csv hasn't any data held in it.

        self.csv = ''

        # type is 'raw' or 'processed'

        if type == 'raw':

            logger.debug('Data type : %s' % type)

            # If data store is zero length return premature termination.

            if len(self.data_store.RawData) == 0:

                logger.debug('No raw data to segment')

                return 'PREMATURE_TERMINATION', 'No raw data to segment.'

            else:

                data_source = self.data_store.RawData.tolist()

                if period == 'day':

                    logger.debug('Period set to : %s' % period)

                    file_name_preference = 'RawData_'

                    logger.debug('file_name_preference set to : %s' % file_name_preference)

                elif period == 'week':

                    logger.debug('Period set to : %s' % period)

                    file_name_preference = 'RawData_Week_'

                    logger.debug('file_name_preference set to : %s' % file_name_preference)

                else:

                    logger.debug('Aborting unknown period : %s' % period)

                    return 'PREMATURE_TERMINATION', 'Unknown period.'

        elif type == 'processed':

            logger.debug('Data type : %s' % type)

            if len(self.data_store.ProcessedData) == 0:

                logger.debug('No processed data to segment')

                return 'PREMATURE_TERMINATION', 'No procesed data to segment.'

            else:

                data_source = self.data_store.ProcessedData.tolist()

                if period == 'day':

                    logger.debug('Period set to : %s' % period)

                    file_name_preference = 'ProcessedData_'

                    logger.debug('file_name_preference set to : %s' % file_name_preference)

                elif period == 'week':

                    logger.debug('Period set to : %s' % period)

                    file_name_preference = 'ProcessedData_Week_'

                    logger.debug('file_name_preference set to : %s' % file_name_preference)

                else:

                    logger.debug('Aborting unknown period : %s' % period)

                    return 'PREMATURE_TERMINATION', 'Unknown period.'

        else:

            logger.debug('Unable to parse data type, raw or processed.')

            return 'PREMATURE_TERMINATION', None

        counter = 0

        epoch_trip = False

        for lista in data_source:

            current_time_stamp = lista[0].strftime("%Y-%m-%d")

            year, week, weekday = lista[0].isocalendar()

            # Set current epoch based on segment period.

            if period == 'day':

                current_epoch = weekday

            elif period == 'week':

                current_epoch = week

            # Store the original time stamp and epoch until we have saved the file.

            if not epoch_trip:

                original_time_stamp = current_time_stamp

                original_epoch = current_epoch

                epoch_trip = False

            # Set the file name based on period

            if period == 'day':

                self.file_name = self.data_home + os.sep + file_name_preference + original_time_stamp

            elif period == 'week':

                self.file_name = (self.data_home + os.sep + file_name_preference + str(original_epoch) + '_' +
                                  original_time_stamp)

            if os.path.isfile(self.file_name + '.csv'):

                sequence = 0

                while os.path.isfile(self.file_name + '.' + str(sequence) + '.csv'):

                    sequence += 1

                else:

                    if not epoch_trip:

                        original_epoch = current_epoch

                    self.write_file_name = self.file_name + '.' + str(sequence) + '.csv'

            else:

                self.write_file_name = self.file_name + '.csv'

            if not re.match(str(current_epoch), str(original_epoch)):

                logger.debug("Current epoch and original epoch don't match writing current data to file")
                logger.debug('Current Epoch : %s  -- Original Epoch : %s' % (str(current_epoch), str(original_epoch)))

                if self.segment_write():

                    self.write_file_name = self.file_name + '.csv'

                    self.add_to_csv(lista)

                    counter += 1

                    epoch_trip = False

                else:

                    return 'PREMATURE_TERMINATION', None

            else:

                epoch_trip = True

                self.add_to_csv(lista)

                counter += 1

        if len(self.csv) != 0:

            logger.debug('We finished parsing data writing to data to file.')

            if not self.segment_write():

                return 'PREMATURE_TERMINATION', None

        logger.debug('Total data source length : %s' % len(data_source))
        logger.debug('Total segmented data length : %s' % str(counter))

        # If data is raw and data source is controller set RawDataSaved to true.

        if type == 'raw' and self.data_store.DataSource == 'Controller':

            self.data_store.RawDataSaved = True

        return 'SUCCESS', None

    def add_to_csv(self, line):

        # Convert datatime object in to formatted string.

        date = line[0].strftime('%Y-%m-%d,%H:%M:%S')

        # For all data exluding the datatime object join it together with a comma

        data = ','.join(line[1:])

        # Add carriage return and line feed to data

        data += '\r\n'

        # Append date and data to csv

        self.csv += date + ',' + data

    def segment_write(self):

        logger = logging.getLogger('core.segmentTimeSeries.segment_write')

        try:

            file = open(self.write_file_name, 'w')

            logger.debug('Writing to file :%s' % self.write_file_name)

        except IOError as msg:

            logger.critical(str(msg))

            return False

        else:

            try:

                if self.data_store.DataSource == 'Controller':

                    if self.metadata_creator.observatory_metadata() is not None:

                        logger.debug('Writing Observatory Metadata to csv file.')

                        file.write(self.metadata_creator.observatory_metadata())

                    if self.metadata_creator.observer_metadata() is not None:

                        logger.debug('Writing Observer Metadata to csv file.')

                        file.write(self.metadata_creator.observer_metadata())

                    if self.metadata_creator.observation_metadata() is not None:

                        logger.debug('Writing Observation Metadata to csv file.')

                        file.write(self.metadata_creator.observation_metadata())

                    if self.data_store.ObserverationNoteMetadata is not None:

                        file.write(self.data_store.ObserverationNoteMetadata)

                elif self.data_store.DataSource == 'CSV':

                    if len(self.data_store.MetadataCsv) != 0:

                        for listb in self.data_store.MetadataCsv:

                            file.write(listb + '\r\n')

                else:

                    logger.critical('Unable to determine data source : %s' % str(self.data_store.DataSource))

                    return False

                file.write(self.csv)

                logger.debug('Closing csv file.')

                file.close()

            except IOError as msg:

                logger.critical(str(msg))

                return False

            else:

                self.csv = ''

                logger.info('Data saved.')

                return True

