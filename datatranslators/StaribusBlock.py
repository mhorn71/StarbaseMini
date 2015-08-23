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


class StaribusBlockParser:
    def __init__(self, channels):
        self.logger = logging.getLogger('datatranslator.StaribusBlock')

        self.number_of_channels = channels

        self.clear()

    def clear(self):
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

    def parser(self, data):
        # First 32 chars are date, time, temp, and sample rate plus spaces.
        # We also need to search of ETX

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
                    dat = re.findall('\d{4}', str(datum))   # split each sample_length into groups of 4

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
            return 'PREMATURE_TERMINATION', None
        else:
            return True

    def exporter(self, file):
        pass

    def importer(self, file):
        pass
