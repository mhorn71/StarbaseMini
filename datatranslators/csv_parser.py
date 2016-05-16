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


class CsvParser:
    def __init__(self, data_store):

        self.data_store = data_store

    def parse(self, file_name, datatranslator):
        # First 32 chars are date, time, temp, and sample rate plus spaces.
        # We also need to search of ETX

        logger = logging.getLogger('datatranslator.CsvParser.parse')

        # Metadata list holder.
        metadata_list = []

        # Observation data list holder
        data_list = []

        # Try to open the file supplied and read the contents.
        try:
            with open(file_name) as csvfile:
                content = csvfile.readlines()
        except IOError:
            return 'PREMATURE_TERMINATION', 'Unable to open : %s' % file_name
        else:
            csvfile.close()

        # Now check each line it should start with either metadata or it must be data, we also strip any newlines.

        for line in content:
            if len(line) != 0:
                if line.startswith('Obser'):
                    metadata_list.append(line.strip('\n'))
                elif re.match('^\d\d\d\d-\d\d-\d\d', line):
                    data_list.append(line.strip('\r\n'))

        # If the metadata list appears to have data append it to data_store.MetadataCsv

        if len(metadata_list) != 0:
            for metadata in metadata_list:
                self.data_store.MetadataCsv.append(metadata)

        # Check we actually have data and if we do split the data by comma and then
        # convert date and time to datetime object

        if len(data_list) != 0:

            for data in data_list:

                # create a list for use to store each line of data

                data_line = []
                data_line.clear()

                split_data = data.split(',')

                # Check the split_data has a minimum length of 4 otherwise we can't parse.

                if len(split_data) < 4:

                    self.data_store.clear()

                    return 'PREMATURE_TERMINATION', 'Not enough fields to parse!!'

                # Now attempt to extract and split date field.

                if re.match('^\d\d\d\d-\d\d-\d\d$', split_data[0]):

                    date = str(split_data[0]).split('-')  # split date field up

                    # Now attempt to extract and split time field.

                    if re.match('^\d\d:\d\d:\d\d', split_data[1]):

                        time = str(split_data[1]).split(':')  # split time field up

                    else:

                        time = None

                # Next check we have a date and time, and if we do create a datetime object

                if time is not None:

                    datetime_obj = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]),
                                                     int(time[1]), int(time[2]))

                    data_line.append(datetime_obj)

                    # set the channel count in the data store.

                    self.data_store.channel_count = (len(split_data) - 2)

                    # Attempt to get datatranslator regex.

                    try:
                        regex = datatranslator.data_regex
                    except AttributeError:
                        regex = "*"

                    # Append each item of what should be channel data to the data_list.

                    for i in range(2, len(split_data)):

                        if re.match(regex, split_data[i]):

                            data_line.append(split_data[i])

                        else:

                            self.data_store.clear()

                            return 'PREMATURE_TERMINATION', 'Unable to parse data.'

                    # TODO change this so we create np array instead of bog standard list.

                    self.data_store.RawDataCsv.append(data_line)

        if len(self.data_store.RawDataCsv) != 0:

            self.data_store.DataSource = 'CSV'

            self.data_store.RawDataCsvAvailable = True

            return 'SUCCESS', 'Imported file : %s' % file_name

        else:

            self.data_store.clear()

            return 'PREMATURE_TERMINATION', 'No data found!!'
