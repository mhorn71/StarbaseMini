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


class StaribusBlockParser:
    def __init__(self):

        logger = logging.getLogger('datatranslators.StaribusBlocks.Staribus.StaribusBlockParser.init')

        logger.debug('Initialised StaribusBlockParser.')

        self.data_regex = '^\d.\d$|^\d.\d\d$|^\d\d.\d$|^\d\d.\d\d$|^\d\d.\d\d\d$|^[-\+]\d\d\d$|^\d\d\d\d$'

        self.parsed_data_list = []

    def clear(self):

        logger = logging.getLogger('datatranslators.StaribusBlocks.Staribus.StaribusBlockParser')

        logger.info('Clearing data.')

        self.parsed_data_list.clear()

    def block_parser(self, data_store):

        logger = logging.getLogger('datatranslators.StaribusBlocks.Staribus.block_parser')

        if data_store.channel_count == 1:

            logger.critical('Number of channels out of range : %s' % data_store.channel_count)

            return False

        elif data_store.channel_count == 2:

            logger.debug('sample_length = 4')

            sample_length = '.{4}'

        elif data_store.channel_count == 3:

            logger.debug('sample_length = 8')

            sample_length = '.{8}'

        elif data_store.channel_count == 4:

            logger.debug('sample_length = 12')

            sample_length = '.{12}'

        elif data_store.channel_count == 5:

            logger.debug('sample_length = 16')

            sample_length = '.{16}'

        elif data_store.channel_count == 6:

            logger.debug('sample_length = 20')

            sample_length = '.{20}'

        elif data_store.channel_count == 7:

            logger.debug('sample_length = 24')

            sample_length = '.{24}'

        elif data_store.channel_count == 8:

            logger.debug('sample_length = 28')

            sample_length = '.{28}'

        elif data_store.channel_count == 9:

            logger.debug('sample_length = 32')

            sample_length = '.{32}'

        else:

            logger.critical('Number of channels out of range : %s' % data_store.channel_count)

            return False

        # First 32 chars are date, time, temp, and sample rate plus spaces.
        # We also need to search of ETX

        for lista in reversed(data_store.RawDataBlocks):

            data = lista.split(' ')

            logger.debug('data list length : %s' % str(len(data)))
    
            try:
                # create datetime object
                date = str(data[0]).split('-')  # split date field up
                time = str(data[1]).split(':')  # split time field up
                epoch = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))

                for datum in re.findall(sample_length, data[6]):  # for every group of sample length
    
                    if len(datum) == 0:

                        logger.warning('datum list length is zero.')

                        return False
    
                    dat = re.findall('....', str(datum))   # split each sample_length into groups of 4

                    logger.debug('dat length : %s' % str(len(dat)))

                    # logger.debug('Sample dat list : %s' % repr(dat))

                    if data_store.channel_count == 2:

                        self.parsed_data_list.append([epoch, data[2], dat[0]])

                    elif data_store.channel_count == 3:

                        self.parsed_data_list.append([epoch, data[2], dat[0], dat[1]])

                    elif data_store.channel_count == 4:

                        self.parsed_data_list.append([epoch, data[2], dat[0], dat[1], dat[2]])

                    elif data_store.channel_count == 5:

                        self.parsed_data_list.append([epoch, data[2], dat[0], dat[1], dat[2], dat[3]])

                    elif data_store.channel_count == 6:

                        self.parsed_data_list.append([epoch, data[2], dat[0], dat[1], dat[2], dat[3], dat[4]])

                    elif data_store.channel_count == 7:

                        self.parsed_data_list.append([epoch, data[2], dat[0], dat[1], dat[2], dat[3], dat[4], dat[5]])

                    elif data_store.channel_count == 8:

                        self.parsed_data_list.append([epoch, data[2], dat[0], dat[1], dat[2], dat[3], dat[4], dat[5],
                                                      dat[6]])

                    elif data_store.channel_count == 9:

                        self.parsed_data_list.append([epoch, data[2], dat[0], dat[1], dat[2], dat[3], dat[4], dat[5],
                                                      dat[6], dat[7]])
    
                    epoch = epoch + datetime.timedelta(seconds=int(data[3]))  # create next sample datetime object.

            except (ValueError, IndexError) as msg:

                logger.warning(str(msg))

                logger.warning('Failed Staribus Block : %s' % repr(data))

        if len(self.parsed_data_list) == 0:

            return False

        else:

            return True
