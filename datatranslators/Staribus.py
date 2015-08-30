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

        print(data)

        data = data.split(' ')
        try:
            # create datetime object
            date = str(data[0]).split('-')  # split date field up
            time = str(data[1]).split(':')  # split time field up
            epoch = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))

            if self.number_of_channels == '1':
                return 'PREMATURE_TERMINATION', 'Number of channels out of range.'
            elif self.number_of_channels == '2':
                sample_length = '\d{4}'
            elif self.number_of_channels == '3':
                if command_variant == '0004':
                    sample_length = '([+|\-]\d{3}[+\-]\d{3})'
                else:
                    sample_length = '\d{8}'
            elif self.number_of_channels == '4':
                sample_length = '\d{12}'
            elif self.number_of_channels == '5':
                sample_length = '\d{16}'
            elif self.number_of_channels == '6':
                sample_length = '\d{20}'
            elif self.number_of_channels == '7':
                sample_length = '\d{24}'
            elif self.number_of_channels == '8':
                sample_length = '\d{28}'
            elif self.number_of_channels == '9':
                sample_length = '\d{32}'
            else:
                return 'PREMATURE_TERMINATION', 'Number of channels out of range.'

            for datum in re.findall(sample_length, data[6]):  # for every group of 16 digits

                print(len(datum))

                if len(datum) == 0:
                    return False

                dat = re.findall('....', str(datum))   # split each sample_length into groups of 4

                self.datetime.append(epoch)  # append current datetime object to sampletime
                self.channel_1.append(data[2])  # append temperature to temperature array

                if self.number_of_channels == '2':
                    self.channel_2.append(int(dat[0]))  # append data to channel arrays
                elif self.number_of_channels == '3':
                    self.channel_2.append(int(dat[0]))
                    self.channel_3.append(int(dat[1]))
                elif self.number_of_channels == '4':
                    self.channel_2.append(int(dat[0]))
                    self.channel_3.append(int(dat[1]))
                    self.channel_4.append(int(dat[2]))
                elif self.number_of_channels == '5':
                    self.channel_2.append(int(dat[0]))
                    self.channel_3.append(int(dat[1]))
                    self.channel_4.append(int(dat[2]))
                    self.channel_5.append(int(dat[3]))
                elif self.number_of_channels == '6':
                    self.channel_2.append(int(dat[0]))
                    self.channel_3.append(int(dat[1]))
                    self.channel_4.append(int(dat[2]))
                    self.channel_5.append(int(dat[3]))
                    self.channel_6.append(int(dat[4]))
                elif self.number_of_channels == '7':
                    self.channel_2.append(int(dat[0]))
                    self.channel_3.append(int(dat[1]))
                    self.channel_4.append(int(dat[2]))
                    self.channel_5.append(int(dat[3]))
                    self.channel_6.append(int(dat[4]))
                    self.channel_7.append(int(dat[5]))
                elif self.number_of_channels == '8':
                    self.channel_2.append(int(dat[0]))
                    self.channel_3.append(int(dat[1]))
                    self.channel_4.append(int(dat[2]))
                    self.channel_5.append(int(dat[3]))
                    self.channel_6.append(int(dat[4]))
                    self.channel_7.append(int(dat[5]))
                    self.channel_8.append(int(dat[6]))
                elif self.number_of_channels == '9':
                    self.channel_2.append(int(dat[0]))
                    self.channel_3.append(int(dat[1]))
                    self.channel_4.append(int(dat[2]))
                    self.channel_5.append(int(dat[3]))
                    self.channel_6.append(int(dat[4]))
                    self.channel_7.append(int(dat[5]))
                    self.channel_8.append(int(dat[6]))
                    self.channel_9.append(int(dat[7]))

                epoch = epoch + datetime.timedelta(seconds=int(data[3]))  # create next sample datetime object.
        except (ValueError, IndexError) as msg:
            self.logger.critical(str(msg))
            return False
        else:
            return True

    def csv_parser(self, data):
        # First 32 chars are date, time, temp, and sample rate plus spaces.
        # We also need to search of ETX

        if re.match('^\d\d\d\d-\d\d-\d\d$', data[0]):
            date = str(data[0]).split('-')  # split date field up
        else:
            return False

        if re.match('^\d\d:\d\d:\d\d', data[1]):
            time = str(data[1]).split(':')  # split time field up
        else:
            return False

        epoch = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))

        try:
            if self.number_of_channels == '1':
                return False
            elif self.number_of_channels == '2':
                self.channel_1.append(int(data[2]))
                self.channel_2.append(int(data[3]))
            elif self.number_of_channels == '3':
                self.channel_1.append(int(data[2]))
                self.channel_2.append(int(data[3]))
                self.channel_3.append(int(data[4]))
            elif self.number_of_channels == '4':
                self.channel_1.append(int(data[2]))
                self.channel_2.append(int(data[3]))
                self.channel_3.append(int(data[4]))
                self.channel_4.append(int(data[5]))
            elif self.number_of_channels == '5':
                self.channel_1.append(int(data[2]))
                self.channel_2.append(int(data[3]))
                self.channel_3.append(int(data[4]))
                self.channel_4.append(int(data[5]))
                self.channel_5.append(int(data[6]))
            elif self.number_of_channels == '6':
                self.channel_1.append(int(data[2]))
                self.channel_2.append(int(data[3]))
                self.channel_3.append(int(data[4]))
                self.channel_4.append(int(data[5]))
                self.channel_5.append(int(data[6]))
                self.channel_6.append(int(data[7]))
            elif self.number_of_channels == '7':
                self.channel_1.append(int(data[2]))
                self.channel_2.append(int(data[3]))
                self.channel_3.append(int(data[4]))
                self.channel_4.append(int(data[5]))
                self.channel_5.append(int(data[6]))
                self.channel_6.append(int(data[7]))
                self.channel_7.append(int(data[8]))
            elif self.number_of_channels == '8':
                self.channel_1.append(int(data[2]))
                self.channel_2.append(int(data[3]))
                self.channel_3.append(int(data[4]))
                self.channel_4.append(int(data[5]))
                self.channel_5.append(int(data[6]))
                self.channel_6.append(int(data[7]))
                self.channel_7.append(int(data[8]))
                self.channel_8.append(int(data[9]))
            elif self.number_of_channels == '9':
                self.channel_1.append(int(data[2]))
                self.channel_2.append(int(data[3]))
                self.channel_3.append(int(data[4]))
                self.channel_4.append(int(data[5]))
                self.channel_5.append(int(data[6]))
                self.channel_6.append(int(data[7]))
                self.channel_7.append(int(data[8]))
                self.channel_8.append(int(data[9]))
                self.channel_9.append(int(data[10]))
            else:
                return False
        except (ValueError, IndexError) as msg:
            self.logger.critical(str(msg))
            return False
        else:
            self.datetime.append(epoch)  # append current datetime object to sampletime
            return True

    def create_data_array(self):
        if self.number_of_channels == '2':
            self.data_array = np.array((self.channel_1, self.channel_2))
        elif self.number_of_channels == '3':
            self.data_array = np.array((self.channel_1, self.channel_2, self.channel_3))
        elif self.number_of_channels == '4':
            self.data_array = np.array((self.channel_1, self.channel_2, self.channel_3, self.channel_4))
        elif self.number_of_channels == '5':
            self.data_array = np.array((self.channel_1, self.channel_2, self.channel_3, self.channel_4, self.channel_5))
        elif self.number_of_channels == '6':
            self.data_array = np.array((self.channel_1, self.channel_2, self.channel_3, self.channel_4, self.channel_5,
                                        self.channel_6))
        elif self.number_of_channels == '7':
            self.data_array = np.array((self.channel_1, self.channel_2, self.channel_3, self.channel_4, self.channel_5,
                                        self.channel_6, self.channel_7))
        elif self.number_of_channels == '8':
            self.data_array = np.array((self.channel_1, self.channel_2, self.channel_3, self.channel_4, self.channel_5,
                                        self.channel_6, self.channel_7, self.channel_8))
        elif self.number_of_channels == '9':
            self.data_array = np.array((self.channel_1, self.channel_2, self.channel_3, self.channel_4, self.channel_5,
                                        self.channel_6, self.channel_7, self.channel_8, self.channel_9))

    def parameter_converter(self, cb, cc, cv, param):

        command = cb + cc + cv

        if re.match('^[A-Za-z]*$', param):
            param = param.lower()

        if re.match('^0305000[0-4]$', command):  # setRate
            param = param.zfill(4)
        elif re.match('^0200000[0-4]$', command):  # getA2D
            param = param.zfill(3)
        elif re.match('^true$', param) and re.match('^[0-4]', cv):  # boolean true
            param = 'Y'
        elif re.match('^false$', param) and re.match('^[0-4]', cv):  # boolean false
            param = 'N'
        else:
            pass

        return param
