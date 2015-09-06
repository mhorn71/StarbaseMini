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

import config_utilities


class SegmentTimeSeries:
    def __init__(self, parent):
        self.logger = logging.getLogger('core.segmentTimeSeries')

        # First get instrument data path from configuration.
        App_Config = config_utilities.ConfigTool()
        data_path = App_Config.get('Application', 'instrument_data_path')

        # Get home path in case instrument data path isn't set.
        home = os.path.expanduser("~")

        if os.path.isdir(data_path):
            self.data_file = data_path + os.path.sep
        else:
            self.data_file = home + os.path.sep

        self.datatranslator = None
        self.channel_count = None
        self.metadata = None
        self.fname = None
        self.csv = ''

    def data_setup(self, datatranslator, number_of_channels, metadata):
        self.datatranslator = datatranslator
        self.channel_count = number_of_channels
        self.metadata = metadata

    def segment_day(self):
        try:
            timestamp = str(self.datatranslator.datetime[0]).split(' ')
        except IndexError:
            return 'ABORT', 'NODATA'

        count = len(self.datatranslator.datetime)

        lasttimestamp = str(self.datatranslator.datetime[count-1]).split(' ')

        if timestamp[0] == lasttimestamp[0]:
            return 'ABORT', 'Not enough data to segment use exporter instead.'

        self.fname = self.data_file + 'RawData_' + timestamp[0] + '.csv'

        self.csv = ''

        for i in range(count):

            if re.match(timestamp[0], str(self.datatranslator.datetime[i])):

                date = str(self.datatranslator.datetime[i]).replace(' ', ',')

                if self.channel_count == '2':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + '\r\n'
                elif self.channel_count == '3':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + '\r\n'
                elif self.channel_count == '4':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                           str(self.datatranslator.channel_4[i]) + '\r\n'
                elif self.channel_count == '5':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                           str(self.datatranslator.channel_4[i]) + ',' + \
                           str(self.datatranslator.channel_5[i]) + '\r\n'
                elif self.channel_count == '6':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                           str(self.datatranslator.channel_4[i]) + ',' + \
                           str(self.datatranslator.channel_5[i]) + ',' + \
                           str(self.datatranslator.channel_6[i]) + '\r\n'
                elif self.channel_count == '7':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                           str(self.datatranslator.channel_4[i]) + ',' + \
                           str(self.datatranslator.channel_5[i]) + ',' + \
                           str(self.datatranslator.channel_6[i]) + \
                           ',' + str(self.datatranslator.channel_7[i]) + '\r\n'
                elif self.channel_count == '8':
                    self.csv += date + ',' + str(self.datatranslator.channel_1[i]) + ',' + \
                           str(self.datatranslator.channel_2[i]) + \
                           ',' + str(self.datatranslator.channel_3[i]) + ',' + \
                           str(self.datatranslator.channel_4[i]) + ',' + \
                           str(self.datatranslator.channel_5[i]) + ',' + \
                           str(self.datatranslator.channel_6[i]) + \
                           ',' + str(self.datatranslator.channel_7[i]) + ',' + \
                           str(self.datatranslator.channel_8[i]) + '\r\n'
                elif self.channel_count == '9':
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
                    self.fname = self.data_file + 'RawData_Segmented_' + timestamp[0] + '.csv'
                    self.csv = ''
                    return 'SUCCESS', 'segmentTimeSeries day not yet implemented AAA'

        return 'SUCCESS', 'segmentTimeSeries day not yet implemented' + ' ' + timestamp[0] + ' ' + str(count)

    def segment_week(self):
        print(self.data_file)
        return 'ABORT', 'segmentTimeSeries week not yet implemented'

    def segment_write(self):
        print('segment write')
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

                observation_metadata = self.metadata.observation_metadata()
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
                self.logger.info('File Exported')
                return 'SUCCESS', None

