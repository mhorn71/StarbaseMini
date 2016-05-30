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
import csv


class CsvParser:
    def __init__(self, data_store):

        self.data_store = data_store

    def parse(self, file_name, metadata_deconstructor):
        # First 32 chars are date, time, temp, and sample rate plus spaces.
        # We also need to search of ETX

        logger = logging.getLogger('datatranslator.CsvParser.parse')

        # Metadata list holder.
        main_list = []

        # Clear the data store.
        self.data_store.clear()

        # Clear the current metadata
        metadata_deconstructor.clear()

        # Try to open the file supplied and read the contents.
        try:
            with open(file_name) as csvfile:

                content = csv.reader(csvfile)

                for line in content:

                    if line[0].startswith('Obser'):

                        metadata_deconstructor.meta_parser(line)

                    elif re.match('^\d\d\d\d-\d\d-\d\d', line[0]):

                        main_list.append(line)

                csvfile.close()

        except IOError as msg:

            logger.warning('Unable to open file : %s %s' % (file_name, str(msg)))

            return 'PREMATURE_TERMINATION', 'Unable to open : %s' % file_name

        else:

            new_main_list = []

            if len(main_list) != 0:

                self.data_store.channel_count = (len(main_list[0]) - 2)

                for data in main_list:

                    data_line = []
                    data_line.clear()

                    if re.match('^\d\d\d\d-\d\d-\d\d', data[0]) and re.match('^\d\d:\d\d:\d\d', data[1]):

                        date_ = data[0].split('-')

                        time_ = data[1].split(':')

                        data_line.append(datetime.datetime(int(date_[0]), int(date_[1]), int(date_[2]),
                                                          int(time_[0]), int(time_[1]), int(time_[2])))

                        for i in data[2:]:

                            data_line.append(i)

                        new_main_list.append(data_line)

                if len(new_main_list) > 0:

                    self.data_store.RawDataCsv = new_main_list

                    self.data_store.DataSource = 'CSV'

                    self.data_store.RawDataCsvAvailable = True

                    print(self.data_store.RawDataCsv)

                    return 'SUCCESS', 'Imported file : %s' % file_name

                else:

                    self.data_store.clear()

                    logger.warning('No data found!!')

                    return 'PREMATURE_TERMINATION', 'NO DATA'