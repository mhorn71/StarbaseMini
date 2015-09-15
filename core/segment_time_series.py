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
import datetime

import config_utilities


class SegmentTimeSeries:
    def __init__(self):
        self.logger = logging.getLogger('core.segmentTimeSeries')

        # First get instrument data path from configuration.
        App_Config = config_utilities.ConfigLoader()
        data_path = App_Config.get('Application', 'instrument_data_path')

        # Get home path in case instrument data path isn't set.
        home = os.path.expanduser("~")

        if data_path is None:
            self.data_file = home + os.path.sep
            self.logger.debug('Data file : %s' % self.data_file)
        else:
            if os.path.isdir(data_path):
                self.data_file = data_path + os.path.sep
                self.logger.debug('Data file : %s' % self.data_file)
            else:
                self.data_file = home + os.path.sep
                self.logger.debug('Data file : %s' % self.data_file)

        self.datatranslator = None
        self.number_of_channels = None
        self.metadata = None
        self.fname = None
        self.csv = ''
        self.data_type = None

    def data_setup(self, datatranslator, source, metadata, data_type):
        self.datatranslator = datatranslator
        self.logger.debug('Data translator object : %s' % repr(datatranslator))
        self.number_of_channels = source.instrument_number_of_channels
        self.logger.debug('Channel count : %s' % self.number_of_channels)
        self.metadata = metadata
        self.logger.debug('Metadata object : %s' % repr(metadata))
        self.data_type = data_type
        self.logger.debug('Data type : %s' % self.data_type)

    def segment_day(self):
        try:
            timestamp = str(self.datatranslator.datetime[0]).split(' ')
        except IndexError:
            return 'ABORT', 'NODATA'

        count = len(self.datatranslator.datetime)

        lasttimestamp = str(self.datatranslator.datetime[count-1]).split(' ')

        if timestamp[0] == lasttimestamp[0]:
            self.logger.info('Not enough data to segment.')
            return 'ABORT', 'Not enough data to segment use exporter instead.'

        self.fname = self.data_file + 'RawData_' + timestamp[0] + '.csv'

        if os.path.isfile(self.fname):
            seq = "0"

            self.fname = self.data_file + 'RawData_' + timestamp[0] + '.%s' + '.csv'

            while os.path.isfile(self.fname % seq):
                seq = int(seq or "0") + 1

            self.fname = self.data_file + 'RawData_' + timestamp[0] + '.%s' + '.csv'
            self.fname = self.fname % seq

        self.csv = ''

        for i in range(count):

            if re.match(timestamp[0], str(self.datatranslator.datetime[i])):

                date = str(self.datatranslator.datetime[i]).replace(' ', ',')

                if self.number_of_channels == '2':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + '\r\n'
                elif self.number_of_channels == '3':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + '\r\n'
                elif self.number_of_channels == '4':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                           str(self.datatranslator.channel_4[i]) + '\r\n'
                elif self.number_of_channels == '5':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                           str(self.datatranslator.channel_4[i]) + ',' + \
                           str(self.datatranslator.channel_5[i]) + '\r\n'
                elif self.number_of_channels == '6':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                           str(self.datatranslator.channel_4[i]) + ',' + \
                           str(self.datatranslator.channel_5[i]) + ',' + \
                           str(self.datatranslator.channel_6[i]) + '\r\n'
                elif self.number_of_channels == '7':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                           str(self.datatranslator.channel_4[i]) + ',' + \
                           str(self.datatranslator.channel_5[i]) + ',' + \
                           str(self.datatranslator.channel_6[i]) + \
                           ',' + str(self.datatranslator.channel_7[i]) + '\r\n'
                elif self.number_of_channels == '8':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                           str(self.datatranslator.channel_4[i]) + ',' + \
                           str(self.datatranslator.channel_5[i]) + ',' + \
                           str(self.datatranslator.channel_6[i]) + \
                           ',' + str(self.datatranslator.channel_7[i]) + ',' + \
                           str(self.datatranslator.channel_8[i]) + '\r\n'
                elif self.number_of_channels == '9':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                           str(self.datatranslator.channel_4[i]) + ',' + \
                           str(self.datatranslator.channel_5[i]) + ',' + \
                           str(self.datatranslator.channel_6[i]) + \
                           ',' + str(self.datatranslator.channel_7[i]) + ',' + \
                           str(self.datatranslator.channel_7[i]) + \
                           ',' + str(self.datatranslator.channel_9[i]) + '\r\n'

            else:
                self.logger.debug('Writing data for time stamp %s' % timestamp[0])
                response = self.segment_write()

                if response[0].startswith('PREMATURE_TERMINATION'):
                    self.logger.debug(response)
                    return response
                else:
                    timestamp = str(self.datatranslator.datetime[i]).split(' ')
                    self.fname = self.data_file + 'RawData_' + timestamp[0] + '.csv'

                    if os.path.isfile(self.fname):

                        seq = "0"

                        self.fname = self.data_file + 'RawData_' + timestamp[0] + '.%s' + '.csv'

                        while os.path.isfile(self.fname % seq):
                            seq = int(seq or "0") + 1

                        self.fname = self.data_file + 'RawData_' + timestamp[0] + '.%s' + '.csv'
                        self.fname = self.fname % seq

                    self.csv = ''

                    date = str(self.datatranslator.datetime[i]).replace(' ', ',')

                    if self.number_of_channels == '2':
                        self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                               str(self.datatranslator.channel_2[i]) + '\r\n'
                    elif self.number_of_channels == '3':
                        self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                               str(self.datatranslator.channel_2[i]) + \
                               ',' + str(self.datatranslator.channel_3[i]) + '\r\n'
                    elif self.number_of_channels == '4':
                        self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                               str(self.datatranslator.channel_2[i]) + \
                               ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                               str(self.datatranslator.channel_4[i]) + '\r\n'
                    elif self.number_of_channels == '5':
                        self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                               str(self.datatranslator.channel_2[i]) + \
                               ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                               str(self.datatranslator.channel_4[i]) + ',' + \
                               str(self.datatranslator.channel_5[i]) + '\r\n'
                    elif self.number_of_channels == '6':
                        self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                               str(self.datatranslator.channel_2[i]) + \
                               ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                               str(self.datatranslator.channel_4[i]) + ',' + \
                               str(self.datatranslator.channel_5[i]) + ',' + \
                               str(self.datatranslator.channel_6[i]) + '\r\n'
                    elif self.number_of_channels == '7':
                        self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                               str(self.datatranslator.channel_2[i]) + \
                               ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                               str(self.datatranslator.channel_4[i]) + ',' + \
                               str(self.datatranslator.channel_5[i]) + ',' + \
                               str(self.datatranslator.channel_6[i]) + \
                               ',' + str(self.datatranslator.channel_7[i]) + '\r\n'
                    elif self.number_of_channels == '8':
                        self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                               str(self.datatranslator.channel_2[i]) + \
                               ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                               str(self.datatranslator.channel_4[i]) + ',' + \
                               str(self.datatranslator.channel_5[i]) + ',' + \
                               str(self.datatranslator.channel_6[i]) + \
                               ',' + str(self.datatranslator.channel_7[i]) + ',' + \
                               str(self.datatranslator.channel_8[i]) + '\r\n'
                    elif self.number_of_channels == '9':
                        self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                               str(self.datatranslator.channel_2[i]) + \
                               ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                               str(self.datatranslator.channel_4[i]) + ',' + \
                               str(self.datatranslator.channel_5[i]) + ',' + \
                               str(self.datatranslator.channel_6[i]) + \
                               ',' + str(self.datatranslator.channel_7[i]) + ',' + \
                               str(self.datatranslator.channel_7[i]) + \
                               ',' + str(self.datatranslator.channel_9[i]) + '\r\n'

        self.logger.debug('Writing data for time stamp %s' % timestamp[0])
        response = self.segment_write()

        if response[0].startswith('PREMATURE_TERMINATION'):
            self.logger.debug(response)
            return response

        return 'SUCCESS', None

    def segment_week(self):
        try:
            timestamp = str(self.datatranslator.datetime[0]).split(' ')
        except IndexError:
            return 'ABORT', 'NODATA'

        count = len(self.datatranslator.datetime)

        lasttimestamp = str(self.datatranslator.datetime[count-1]).split(' ')

        da = timestamp[0].split('-')

        year, week, weekday = datetime.date(int(da[0]), int(da[1]), int(da[2])).isocalendar()

        self.fname = self.data_file + 'RawData_Week_' + str(week) + '_' + timestamp[0] + '.csv'

        if os.path.isfile(self.fname):
            seq = "0"

            self.fname = self.data_file + 'RawData_' + str(week) + '_' + timestamp[0] + '.%s' + '.csv'

            while os.path.isfile(self.fname % seq):
                seq = int(seq or "0") + 1

            self.fname = self.data_file + 'RawData_' + str(week) + '_' + timestamp[0] + '.%s' + '.csv'
            self.fname = self.fname % seq

        self.csv = ''

        for i in range(count):

            timestamp = str(self.datatranslator.datetime[i]).split(' ')

            da = timestamp[0].split('-')

            year, current_week, weekday = datetime.date(int(da[0]), int(da[1]), int(da[2])).isocalendar()

            if re.match(str(week), str(current_week)):

                date = str(self.datatranslator.datetime[i]).replace(' ', ',')

                if self.number_of_channels == '2':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + '\r\n'
                elif self.number_of_channels == '3':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + '\r\n'
                elif self.number_of_channels == '4':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                           str(self.datatranslator.channel_4[i]) + '\r\n'
                elif self.number_of_channels == '5':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                           str(self.datatranslator.channel_4[i]) + ',' + \
                           str(self.datatranslator.channel_5[i]) + '\r\n'
                elif self.number_of_channels == '6':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                           str(self.datatranslator.channel_4[i]) + ',' + \
                           str(self.datatranslator.channel_5[i]) + ',' + \
                           str(self.datatranslator.channel_6[i]) + '\r\n'
                elif self.number_of_channels == '7':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                           str(self.datatranslator.channel_4[i]) + ',' + \
                           str(self.datatranslator.channel_5[i]) + ',' + \
                           str(self.datatranslator.channel_6[i]) + \
                           ',' + str(self.datatranslator.channel_7[i]) + '\r\n'
                elif self.number_of_channels == '8':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                           str(self.datatranslator.channel_4[i]) + ',' + \
                           str(self.datatranslator.channel_5[i]) + ',' + \
                           str(self.datatranslator.channel_6[i]) + \
                           ',' + str(self.datatranslator.channel_7[i]) + ',' + \
                           str(self.datatranslator.channel_8[i]) + '\r\n'
                elif self.number_of_channels == '9':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                           str(self.datatranslator.channel_4[i]) + ',' + \
                           str(self.datatranslator.channel_5[i]) + ',' + \
                           str(self.datatranslator.channel_6[i]) + \
                           ',' + str(self.datatranslator.channel_7[i]) + ',' + \
                           str(self.datatranslator.channel_7[i]) + \
                           ',' + str(self.datatranslator.channel_9[i]) + '\r\n'

            else:
                self.logger.debug('Writing data for time stamp %s' % timestamp[0])

                response = self.segment_write()

                if response[0].startswith('PREMATURE_TERMINATION'):
                    self.logger.debug(response)
                    return response
                else:

                    timestamp = str(self.datatranslator.datetime[i]).split(' ')

                    da = timestamp[0].split('-')

                    year, week, weekday = datetime.date(int(da[0]), int(da[1]), int(da[2])).isocalendar()

                    self.fname = self.data_file + 'RawData_Week_' + str(week) + '_' + timestamp[0] + '.csv'

                    self.fname = self.data_file + 'RawData_Week_' + str(week) + '_' + timestamp[0] + '.csv'

                    if os.path.isfile(self.fname):
                        seq = "0"

                        self.fname = self.data_file + 'RawData_' + str(week) + '_' + timestamp[0] + '.%s' + '.csv'

                        while os.path.isfile(self.fname % seq):
                            seq = int(seq or "0") + 1

                        self.fname = self.data_file + 'RawData_' + str(week) + '_' + timestamp[0] + '.%s' + '.csv'
                        self.fname = self.fname % seq

                    self.csv = ''

                    date = str(self.datatranslator.datetime[i]).replace(' ', ',')

                    if self.number_of_channels == '2':
                        self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                               str(self.datatranslator.channel_2[i]) + '\r\n'
                    elif self.number_of_channels == '3':
                        self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                               str(self.datatranslator.channel_2[i]) + \
                               ',' + str(self.datatranslator.channel_3[i]) + '\r\n'
                    elif self.number_of_channels == '4':
                        self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                               str(self.datatranslator.channel_2[i]) + \
                               ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                               str(self.datatranslator.channel_4[i]) + '\r\n'
                    elif self.number_of_channels == '5':
                        self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                               str(self.datatranslator.channel_2[i]) + \
                               ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                               str(self.datatranslator.channel_4[i]) + ',' + \
                               str(self.datatranslator.channel_5[i]) + '\r\n'
                    elif self.number_of_channels == '6':
                        self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                               str(self.datatranslator.channel_2[i]) + \
                               ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                               str(self.datatranslator.channel_4[i]) + ',' + \
                               str(self.datatranslator.channel_5[i]) + ',' + \
                               str(self.datatranslator.channel_6[i]) + '\r\n'
                    elif self.number_of_channels == '7':
                        self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                               str(self.datatranslator.channel_2[i]) + \
                               ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                               str(self.datatranslator.channel_4[i]) + ',' + \
                               str(self.datatranslator.channel_5[i]) + ',' + \
                               str(self.datatranslator.channel_6[i]) + \
                               ',' + str(self.datatranslator.channel_7[i]) + '\r\n'
                    elif self.number_of_channels == '8':
                        self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                               str(self.datatranslator.channel_2[i]) + \
                               ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                               str(self.datatranslator.channel_4[i]) + ',' + \
                               str(self.datatranslator.channel_5[i]) + ',' + \
                               str(self.datatranslator.channel_6[i]) + \
                               ',' + str(self.datatranslator.channel_7[i]) + ',' + \
                               str(self.datatranslator.channel_8[i]) + '\r\n'
                    elif self.number_of_channels == '9':
                        self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                               str(self.datatranslator.channel_2[i]) + \
                               ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                               str(self.datatranslator.channel_4[i]) + ',' + \
                               str(self.datatranslator.channel_5[i]) + ',' + \
                               str(self.datatranslator.channel_6[i]) + \
                               ',' + str(self.datatranslator.channel_7[i]) + ',' + \
                               str(self.datatranslator.channel_7[i]) + \
                               ',' + str(self.datatranslator.channel_9[i]) + '\r\n'

        self.logger.debug('Writing data for time stamp %s' % timestamp[0])

        response = self.segment_write()

        if response[0].startswith('PREMATURE_TERMINATION'):
            self.logger.debug(response)
            return response

        return 'SUCCESS', None

    def segment_write(self):
        try:
            file = open(self.fname, 'a+')
            self.logger.debug('Writing to file :%s' % self.fname)
        except IOError as msg:
            self.logger.critical(str(msg))
            return 'PREMATURE_TERMINATION', 'Unable to create file'
        else:
            try:
                observatory_metadata = self.metadata.observatory_metadata()
                if observatory_metadata is not None:
                    self.logger.debug('Appending Observatory Metadata to csv file.')
                    file.write(observatory_metadata)

                observer_metadata = self.metadata.observer_metadata()
                if observer_metadata is not None:
                    self.logger.debug('Appending Observer Metadata to csv file.')
                    file.write(observer_metadata)

                observation_metadata = self.metadata.observation_metadata(self.data_type)
                if observation_metadata is not None:
                    self.logger.debug('Appending Observation Metadata to csv file.')
                    file.write(observation_metadata)

                file.write(self.csv)
                self.logger.debug('Closing csv file.')
                file.close()
            except IOError as msg:
                self.logger.critical(str(msg))
                return 'PREMATURE_TERMINATION', 'Unable to create file'
            else:
                self.logger.info('File Exported :%s' % self.fname)
                return 'SUCCESS', None

