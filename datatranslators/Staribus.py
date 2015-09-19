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
import datetime
import re
import numpy as np


class StaribusParser:
    def __init__(self, channels):
        self.logger = logging.getLogger('datatranslator.StaribusBlock')
        self.loggera = logging.getLogger('datatranslator.StaribusBlock.block_parser')
        self.loggerb = logging.getLogger('datatranslator.StaribusBlock.csv_parser')

        self.number_of_channels = channels

        self.data_array = None

        self.datetime = []
        self.channel_1 = []
        self.channel_2 = []
        self.channel_3 = []
        self.channel_4 = []
        self.channel_5 = []
        self.channel_6 = []
        self.channel_7 = []
        self.channel_8 = []
        self.channel_9 = []

        self.clear()

    def clear(self):
        self.logger.info('Clearing data.')
        del self.datetime[:]
        del self.channel_1[:]
        del self.channel_2[:]
        del self.channel_3[:]
        del self.channel_4[:]
        del self.channel_5[:]
        del self.channel_6[:]
        del self.channel_7[:]
        del self.channel_8[:]
        del self.channel_9[:]
        del self.data_array
        self.data_array = None

    def block_parser(self, data, command_variant):
        # First 32 chars are date, time, temp, and sample rate plus spaces.
        # We also need to search of ETX

        data = data.split(' ')

        self.loggera.debug('Channel count : %s' % self.number_of_channels)

        try:
            # create datetime object
            date = str(data[0]).split('-')  # split date field up
            time = str(data[1]).split(':')  # split time field up
            epoch = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))

            if self.number_of_channels == '1':
                self.loggera.critical('Number of channels out of range : %s' % self.number_of_channels)
                return 'PREMATURE_TERMINATION', 'Number of channels out of range.'
            elif self.number_of_channels == '2':
                self.loggera.info('Sample Length d{4}')
                sample_length = '\d{4}'
            elif self.number_of_channels == '3':
                if command_variant == '0004':
                    self.loggera.info('Sample Length cv 0004 mag format.')
                    sample_length = '([+|\-]\d{3}[+\-]\d{3})'
                else:
                    sample_length = '\d{8}'
                    self.loggera.info('Sample Length d{8}')
            elif self.number_of_channels == '4':
                sample_length = '\d{12}'
                self.loggera.info('Sample Length d{12}')
            elif self.number_of_channels == '5':
                sample_length = '\d{16}'
                self.loggera.info('Sample Length d{16}')
            elif self.number_of_channels == '6':
                sample_length = '\d{20}'
                self.loggera.info('Sample Length d{20}')
            elif self.number_of_channels == '7':
                sample_length = '\d{24}'
                self.loggera.info('Sample Length d{24}')
            elif self.number_of_channels == '8':
                sample_length = '\d{28}'
                self.loggera.info('Sample Length d{28}')
            elif self.number_of_channels == '9':
                sample_length = '\d{32}'
                self.loggera.info('Sample Length d{32}')
            else:
                self.loggera.critical('Number of channels out of range : %s' % self.number_of_channels)
                return 'PREMATURE_TERMINATION', 'Number of channels out of range.'

            for datum in re.findall(sample_length, data[6]):  # for every group of 16 digits

                if len(datum) == 0:
                    return False

                dat = re.findall('....', str(datum))   # split each sample_length into groups of 4
                self.loggera.debug('Sample dat list : %s' % repr(dat))

                self.datetime.append(epoch)  # append current datetime object to sampletime
                self.loggera.debug('Appending to datetime : %s' % repr(epoch))
                self.channel_1.append(data[2])  # append temperature to temperature array
                self.logger.debug('Appending temp to channel 1 : %s' % data[2])

                if self.number_of_channels == '2':
                    self.channel_2.append(dat[0]) # append data to channel arrays
                elif self.number_of_channels == '3':
                    self.channel_2.append(dat[0])
                    self.channel_3.append(dat[1])
                elif self.number_of_channels == '4':
                    self.channel_2.append(dat[0])
                    self.channel_3.append(dat[1])
                    self.channel_4.append(dat[2])
                elif self.number_of_channels == '5':
                    self.channel_2.append(dat[0])
                    self.channel_3.append(dat[1])
                    self.channel_4.append(dat[2])
                    self.channel_5.append(dat[3])
                elif self.number_of_channels == '6':
                    self.channel_2.append(dat[0])
                    self.channel_3.append(dat[1])
                    self.channel_4.append(dat[2])
                    self.channel_5.append(dat[3])
                    self.channel_6.append(dat[4])
                elif self.number_of_channels == '7':
                    self.channel_2.append(dat[0])
                    self.channel_3.append(dat[1])
                    self.channel_4.append(dat[2])
                    self.channel_5.append(dat[3])
                    self.channel_6.append(dat[4])
                    self.channel_7.append(dat[5])
                elif self.number_of_channels == '8':
                    self.channel_2.append(dat[0])
                    self.channel_3.append(dat[1])
                    self.channel_4.append(dat[2])
                    self.channel_5.append(dat[3])
                    self.channel_6.append(dat[4])
                    self.channel_7.append(dat[5])
                    self.channel_8.append(dat[6])
                elif self.number_of_channels == '9':
                    self.channel_2.append(dat[0])
                    self.channel_3.append(dat[1])
                    self.channel_4.append(dat[2])
                    self.channel_5.append(dat[3])
                    self.channel_6.append(dat[4])
                    self.channel_7.append(dat[5])
                    self.channel_8.append(dat[6])
                    self.channel_9.append(dat[7])

                epoch = epoch + datetime.timedelta(seconds=int(data[3]))  # create next sample datetime object.
        except (ValueError, IndexError) as msg:
            self.loggera.warning(str(msg))
            self.loggera.warning('Failed Staribus Block : %s' % repr(data))
        else:
            return True

    def csv_parser(self, data, channel_count):
        # First 32 chars are date, time, temp, and sample rate plus spaces.
        # We also need to search of ETX

        if re.match('^\d\d\d\d-\d\d-\d\d$', data[0]):
            date = str(data[0]).split('-')  # split date field up
        else:
            self.logger.warning('Unable to split date : %s' % repr(data[0]))
            return False

        if re.match('^\d\d:\d\d:\d\d', data[1]):
            time = str(data[1]).split(':')  # split time field up
        else:
            self.logger.warning('Unable to split time : %s' % repr(data[1]))
            return False

        epoch = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))

        try:
            if channel_count == '1':
                self.loggerb.critical('Channel count out of bounds : %s' % channel_count)
                return False
            elif channel_count == '2':
                self.channel_1.append(data[2])
                self.channel_2.append(data[3])
            elif channel_count == '3':
                self.channel_1.append(data[2])
                self.channel_2.append(data[3])
                self.channel_3.append(data[4])
            elif channel_count == '4':
                self.channel_1.append(data[2])
                self.channel_2.append(data[3])
                self.channel_3.append(data[4])
                self.channel_4.append(data[5])
            elif channel_count == '5':
                self.channel_1.append(data[2])
                self.channel_2.append(data[3])
                self.channel_3.append(data[4])
                self.channel_4.append(data[5])
                self.channel_5.append(data[6])
            elif channel_count == '6':
                self.channel_1.append(data[2])
                self.channel_2.append(data[3])
                self.channel_3.append(data[4])
                self.channel_4.append(data[5])
                self.channel_5.append(data[6])
                self.channel_6.append(data[7])
            elif channel_count == '7':
                self.channel_1.append(data[2])
                self.channel_2.append(data[3])
                self.channel_3.append(data[4])
                self.channel_4.append(data[5])
                self.channel_5.append(data[6])
                self.channel_6.append(data[7])
                self.channel_7.append(data[8])
            elif channel_count == '8':
                self.channel_1.append(data[2])
                self.channel_2.append(data[3])
                self.channel_3.append(data[4])
                self.channel_4.append(data[5])
                self.channel_5.append(data[6])
                self.channel_6.append(data[7])
                self.channel_7.append(data[8])
                self.channel_8.append(data[9])
            elif channel_count == '9':
                self.channel_1.append(data[2])
                self.channel_2.append(data[3])
                self.channel_3.append(data[4])
                self.channel_4.append(data[5])
                self.channel_5.append(data[6])
                self.channel_6.append(data[7])
                self.channel_7.append(data[8])
                self.channel_8.append(data[9])
                self.channel_9.append(data[10])
            else:
                self.loggerb.critical('Channel count out of bounds : %s' % channel_count)
                return False
        except (ValueError, IndexError) as msg:
            self.loggerb.critical(str(msg))
            return False
        else:
            self.datetime.append(epoch)  # append current datetime object to sampletime
            return True

    def create_data_array(self, channel_count):
        if channel_count == '2':
            self.logger.debug('Creating 2 * n data array')
            self.data_array = np.array((self.channel_1, self.channel_2))
        elif channel_count == '3':
            self.logger.debug('Creating 3 * n data array')
            self.data_array = np.array((self.channel_1, self.channel_2, self.channel_3))
        elif channel_count == '4':
            self.logger.debug('Creating 4 * n data array')
            self.data_array = np.array((self.channel_1, self.channel_2, self.channel_3, self.channel_4))
        elif channel_count == '5':
            self.logger.debug('Creating 5 * n data array')
            self.data_array = np.array((self.channel_1, self.channel_2, self.channel_3, self.channel_4, self.channel_5))
        elif channel_count == '6':
            self.logger.debug('Creating 6 * n data array')
            self.data_array = np.array((self.channel_1, self.channel_2, self.channel_3, self.channel_4, self.channel_5,
                                        self.channel_6))
        elif channel_count == '7':
            self.logger.debug('Creating 7 * n data array')
            self.data_array = np.array((self.channel_1, self.channel_2, self.channel_3, self.channel_4, self.channel_5,
                                        self.channel_6, self.channel_7))
        elif channel_count == '8':
            self.logger.debug('Creating 8 * n data array')
            self.data_array = np.array((self.channel_1, self.channel_2, self.channel_3, self.channel_4, self.channel_5,
                                        self.channel_6, self.channel_7, self.channel_8))
        elif channel_count == '9':
            self.logger.debug('Creating 9 * n data array')
            self.data_array = np.array((self.channel_1, self.channel_2, self.channel_3, self.channel_4, self.channel_5,
                                        self.channel_6, self.channel_7, self.channel_8, self.channel_9))

    def parameter_converter(self, cb, cc, cv, param):

        command = cb + cc + cv

        if re.match('^[A-Za-z]*$', param):
            param = param.lower()

        if re.match('^0305000[1-4]$', command):  # setRate
            param = param.zfill(4)
        elif re.match('^0200000[1-4]$', command):  # getA2D
            param = param.zfill(3)
        elif re.match('^true$', param) and re.match('^[0001|0002|0003|0004]$', cv):  # boolean true
            param = 'Y'
        elif re.match('^false$', param) and re.match('^[0001|0002|0003|0004]$', cv):  # boolean false
            param = 'N'
        else:
            pass

        return param
