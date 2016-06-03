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

import numpy as np
import logging


class DataStore(object):
    def __init__(self):

        # The raw data as returned from the controller in whatever format that might be, StaribusBlocks only at
        # present.  WARNING - the data store in RawDataBlocks will be in reverse e.g if we have block 0000 - 000A
        # index 0 of the list will be 000A whereas index 9 will be 0000

        self.RawDataBlocks = []

        # A simple condition so we know if RawDataBlocks has data True we have data False we haven't

        self.RawDataBlocksAvailable = False

        # The raw csv data

        self.RawDataCsv = []

        # Data that has been translated from whatever format the controller has provided,
        # StaribusBlocks only at present.  Make sure this ends up np.array

        self.RawData = []

        # Data that has been passed through one of the filters. Make sure this ends up np.array

        self.ProcessedData = []

        # A simple condition so we know if RawDataCsv has data True we have data False we haven't

        self.RawDataCsvAvailable = False

        # Where the data came from either CSV file or Controller

        self.DataSource = None

        # A simple condition so we know if the RawData has been saved, true is saved, false isn't saved.

        self.RawDataSaved = False

        # A simple condition so we know if the ProcessedData has been saved, true is saved, false isn't saved

        self.ProcessedDataSaved = False # False if ProcessedData hasn't been saved, or True if it has

        # Observation Note Changed.

        self.ObservationNotesChanged = False

        # Channel count of current data.

        self.channel_count = 0

        # Controller data block parser this is set from the instrument_datatranslator_class_loader

        self.block_parser = None

    def print_state(self):

        print("Data source : %s" % str(self.DataSource))
        print("\nRaw data blocks length : %s" % str(len(self.RawDataBlocks)))
        print("Raw data blocks : %s" % str(self.RawDataBlocks))
        print("Raw data blocks available : %s" % str(self.RawDataBlocksAvailable))
        print("\nRaw data csv blocks : %s" % str(self.RawDataCsv))
        print("Raw data csv available : %s" % str(self.RawDataCsvAvailable))
        print("Raw data : %s" % str(self.RawData))
        print("Raw data saved : %s" % str(self.RawDataSaved))
        print("\nProcessed data length : %s" % str(len(self.ProcessedData)))
        print("Processed data saved : %s" % str(self.ProcessedDataSaved))
        print("\nChannel count : %s" % self.channel_count)

    def data_state(self):

        logger = logging.getLogger('datastore.DataStore.data_state')

        if len(self.ProcessedData) != 0 and self.ProcessedDataSaved is False:

            logger.debug("We have Processed Data but it isn't saved yet.")

            return False, "You have unsaved processed data."

        elif len(self.RawData) != 0 and self.RawDataSaved is False and self.DataSource == 'Controller':

            logger.debug("We have RawData but it isn't saved yet.")

            return False, "You have unsaved raw data."

        elif len(self.RawData) != 0 and self.RawDataSaved is False and self.ObservationNotesChanged is True:

            logger.debug("Unsaved Metadata.")

            return False, "You have unsaved metadata."

        elif self.ObservationNotesChanged is True:

            logger.debug("Unsaved Metadata.")

            return False, "You have unsaved metadata."

        else:

            logger.debug("We appear to have a clean data store.")

            return True, "Data store ready to accept data."

    def default_state(self):

        ''' Return True if all settings are reset to default other returns False'''

        if len(self.RawData) != 0 or len(self.ProcessedData) != 0 or self.DataSource is not None or \
           len(self.RawDataBlocks) != 0 or self.RawDataSaved is not False or self.ProcessedDataSaved is not False \
            or self.RawDataBlocksAvailable is not False or self.RawDataCsvAvailable \
                is not False or self.ObservationNotesChanged is not False:

            return False

        else:

            return True

    def clear(self):

        ''' Set all attributes back to default state.'''

        self.RawDataBlocks.clear()

        self.RawDataCsv.clear()

        del self.RawData  # Delete instead of clear as we could have a numpy array.

        self.RawData = [] # Recreate deleted variable.

        del self.ProcessedData # Delete instead of clear as we could have a numpy array.

        self.ProcessedData = [] # Recreate deleted variable.

        self.RawDataBlocksAvailable = False

        self.RawDataCsvAvailable = False

        self.DataSource = None

        self.RawDataSaved = False

        self.ProcessedDataSaved = False

        self.ObservationNotesChanged = False

        self.channel_count = 0

    def create_arrays(self):

        logger = logging.getLogger('datastore.DataStore.create_arrays')

        # Here we create the numpy arrays based on the shape of the data presented.

        # CSV Data ..

        if self.DataSource == 'CSV':

            self.RawData = np.array(self.RawDataCsv)

            self.RawDataCsvAvailable = True

            return True

        elif self.DataSource == 'Controller':

            # Parse Blocks

            # clear any data held in translator

            self.block_parser.clear()

            if self.block_parser.block_parser(self):

                logger.debug('We appeared to parse block')

                self.RawData = np.array(self.block_parser.parsed_data_list)

                return True

            else:

                return False




