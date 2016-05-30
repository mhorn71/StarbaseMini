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
import re
import logging
import sys

from PyQt4 import QtGui

import dao
import datatypes
import utilities


class CommandInterpreter():
    def __init__(self, data_store, metadata):

        # Style sheets

        if sys.platform.startswith('darwin'):

            with open('css/macStyle.css', 'r') as style:

                self.StyleSheet = style.read()

        elif sys.platform.startswith('win32'):

            with open('css/winStyle.css', 'r') as style:

                self.StyleSheet = style.read()

        elif sys.platform.startswith('linux'):

            with open('css/nixStyle.css', 'r') as style:

                self.StyleSheet = style.read()

        else:

            self.StyleSheet = None

        # Data store object

        self.data_store = data_store

        self.response_regex = None

        self.check_response_message = 'INVALID_RESPONSE_MESSAGE', None

        self.dao_processor = dao.DaoProcessor()

        self.application_configuration = None

        self.metadata = metadata

        self.instrument = None

    def close(self):

        logger = logging.getLogger('interpreter.CommandInterpreter.close')

        if self.dao_processor is not None:

            logger.debug('Closing dao_processor')

            self.dao_processor.close()

        else:

            logger.debug('No dao_processor to close')

    def start(self, parent):

        logger = logging.getLogger('interpreter.CommandInterpreter.start')

        self.application_configuration = parent.application_configuration
        self.instrument = parent.instrument

        try:

            if self.dao_processor is None:

                logger.debug('Initialising dao_processor')

                self.initialise_dao()

            else:
                logger.debug('Closing dao_processor')

                self.dao_processor.close()

                logger.debug('Initialising dao_processor')

                self.initialise_dao()

        except IOError:

            raise IOError

    def initialise_dao(self):

        logger = logging.getLogger('interpreter.CommandInterpreter.initialise_dao')

        # Set starinet_address and starinet_port to None these parameter will get set depending on supplied
        # configuration

        if self.instrument.instrument_staribus_address != '000':

            logger.debug('Instrument appears to be Staribus, address : %s' %
                         self.instrument.instrument_staribus_address)

            if self.instrument.instrument_staribus2starinet == 'False':

                logger.info('Setting stream to Staribus')

                stream = 'Staribus'

            else:

                logger.info('Staribus to Starinet Converter enabled setting stream to Starinet')

                stream = 'Starinet'

                logger.debug('Routing staribus packets to IP : %s Port : %s' %
                             (self.instrument.instrument_starinet_address,
                              self.instrument.instrument_starinet_port))
        else:

            logger.debug('Setting stream to Starinet')

            stream = 'Starinet'

            logger.debug('Starinet address and port : %s:%s' % (self.instrument.instrument_starinet_address,
                                                                self.instrument.instrument_starinet_port))

        try:

            self.dao_processor.start(self.instrument.instrument_staribus_port,
                                     self.instrument.instrument_staribus_baudrate,
                                     self.instrument.instrument_staribus_timeout,
                                     self.instrument.instrument_starinet_address,
                                     self.instrument.instrument_starinet_port,
                                     stream, self.instrument.instrument_staribus_type)
        except IOError as msg:

            logger.critical('Unable to initiate dao.DaoProcessor : %s' % str(msg))

            raise IOError(msg)

    def command_attributes(self, module, command):

        logger = logging.getLogger('interpreter.command_attributes')

        # Here we search the instrument command dictionary and get the command values.

        # set ident to None as we'll use that to make sure we actually found the command in the dictionary

        ident = None

        for command_in_dict in self.instrument.command_dict[module]:

            for key in command_in_dict.keys():

                if key == command:

                    ident = command_in_dict[key]['Identifier']

                    base = module
                    code = command
                    variant = command_in_dict[key]['Variant']
                    send_to_port = command_in_dict[key]['SendToPort']


                    if command_in_dict[key]['BlockedData'] == 'None':

                        blocked_data = None

                        logger.debug('Blocked data is None')

                    else:

                        blocked_data = command_in_dict[key]['BlockedData']

                        logger.debug('Blocked data is ' + str(blocked_data))

                    if command_in_dict[key]['SteppedData'] == 'None':

                        stepped_data = None

                        logger.debug('Stepped data is None')

                    else:

                        stepped_data = command_in_dict[key]['SteppedData']

                        logger.debug('Stepped data is ' + str(stepped_data))

                    if command_in_dict[key]['Parameters']['TrafficDataType'] == 'None':

                        traffic_data_type = None

                        logger.debug('TrafficDataType is None')

                    else:

                        traffic_data_type = command_in_dict[key]['Parameters']['TrafficDataType']

                    if command_in_dict[key]['Parameters']['Choices'] == 'None':

                        choice = None

                        logger.debug('Choice is None')

                    else:

                        choice = command_in_dict[key]['Parameters']['Choices']

                        logger.debug('Choice is ' + str(choice))

                    if command_in_dict[key]['Parameters']['Regex'] == 'None':

                        parameter = None

                        logger.debug('Parameter is None')

                    else:

                        parameter = command_in_dict[key]['Parameters']['Regex']

                        logger.debug('Parameter is ' + str(parameter))

                        # Run the parameter through the data type converter and apply traffic data type.

                        parameter = command_in_dict[key]['Parameters']['Regex']

                    if command_in_dict[key]['Response']['Units'] == 'None':

                        units = None

                        logger.debug('Units is None')

                    else:

                        units = command_in_dict[key]['Response']['Units']

                        logger.debug('Units is ' + str(units))

                    if command_in_dict[key]['Response']['Regex'] == 'None':

                        response_regex = None

                        logger.debug('Response regex is None')

                    else:

                        response_regex = command_in_dict[key]['Response']['Regex']

                        logger.debug('Response regex is ' + str(response_regex))

                    if command_in_dict[key]['Response']['DataTypeName'] == 'None':

                        response_data_type_name = None

                        logger.debug('Response data type name is None')

                    else:

                        response_data_type_name = command_in_dict[key]['Response']['DataTypeName']

                        logger.debug('Response data type name is ' + str(response_data_type_name))

        # If ident is None then we can't have located the command in the dictionary.

        if ident is None:

            return None

        else:

            return ident, base, code, variant, send_to_port, blocked_data, stepped_data, traffic_data_type, choice, parameter, \
                   units, response_regex, response_data_type_name

    def command_parser(self, module, command, choice, parameter):

        logger = logging.getLogger('interpreter.command_parser')

        # Here we search the instrument command dictionary and get the command values.

        # set ident to None as we'll use that to make sure we actually found the command in the dictionary

        ident = None

        for command_in_dict in self.instrument.command_dict[module]:

            for key in command_in_dict.keys():

                if key == command:

                    ident = command_in_dict[key]['Identifier']

                    base = module
                    code = command
                    variant = command_in_dict[key]['Variant']
                    send_to_port = command_in_dict[key]['SendToPort']

                    logger.info('################### Executing command : %s ###################' % ident)

                    if command_in_dict[key]['BlockedData'] == 'None':

                        blocked_data = None

                        logger.debug('Blocked data is None')

                    else:

                        blocked_data = command_in_dict[key]['BlockedData']

                        logger.debug('Blocked data is ' + str(blocked_data))

                    if command_in_dict[key]['SteppedData'] == 'None':

                        stepped_data = None

                        logger.debug('Stepped data is None')

                    else:

                        stepped_data = command_in_dict[key]['SteppedData']

                        logger.debug('Stepped data is ' + str(stepped_data))

                    if command_in_dict[key]['Parameters']['TrafficDataType'] == 'None':

                        traffic_data_type = None

                        logger.debug('TrafficDataType is None')

                    else:

                        traffic_data_type = command_in_dict[key]['Parameters']['TrafficDataType']

                    if command_in_dict[key]['Parameters']['Choices'] == 'None':

                        choice = None

                        logger.debug('Choice is None')

                    else:

                        logger.debug('Choice is ' + str(choice))

                        # create a list of choices available.

                        choices_list = command_in_dict[key]['Parameters']['Choices']

                        choices_list = choices_list.split(',')

                        #  We get the index number of the choice here as we have access to the instrument dict.

                        if traffic_data_type != 'None':

                            if traffic_data_type == 'NumericIndexedList':

                                choice = choices_list.index(choice)

                            else:

                                choice = datatypes.DataTypeConverter(traffic_data_type, choice)

                    if command_in_dict[key]['Parameters']['Regex'] == 'None':

                        parameter = None

                        logger.debug('Parameter is None')

                    else:

                        logger.debug('Parameter is ' + str(parameter))

                        # Run the parameter through the data type converter and apply traffic data type.

                        parameter = datatypes.DataTypeConverter(traffic_data_type, parameter)

                    if command_in_dict[key]['Response']['Units'] == 'None':

                        units = None

                        logger.debug('Units is None')

                    else:

                        units = command_in_dict[key]['Response']['Units']

                        logger.debug('Units is ' + str(units))

                    if command_in_dict[key]['Response']['Regex'] == 'None':

                        response_regex = None

                        logger.debug('Response regex is None')

                    else:

                        response_regex = command_in_dict[key]['Response']['Regex']

                        logger.debug('Response regex is ' + str(response_regex))

                    if command_in_dict[key]['Response']['DataTypeName'] == 'None':

                        response_data_type_name = None

                        logger.debug('Response data type name is None')

                    else:

                        response_data_type_name = command_in_dict[key]['Response']['DataTypeName']

                        logger.debug('Response data type name is ' + str(response_data_type_name))

        # The data at this point should be as sane as we can determine from the Instrument XML, so will return it.

        # ident  = Can't be none
        # base = Must be UnsignedHexByte
        # code = Must be UnsignedHexByte
        # send_to__port = Must be true/True or false/False
        # blocked_data = Must be a list of two UnsignedHexBytes
        # stepped_data = Not implemented so must be None
        # traffic_data_type = We've all ready looked at this above so we don't check again here.
        # choice =
        # parameter
        # units
        # response_regex
        # response_data_type_name

        # If ident is None then we can't have located the command in the dictionary.

        if ident is None:

            return None

        else:

            return ident, base, code, variant, send_to_port, blocked_data, stepped_data, traffic_data_type, choice, parameter, \
                   units, response_regex, response_data_type_name

    def process_command(self, module, command, choice, parameter):

        logger = logging.getLogger('interpreter.process_command')

        # First parse the command dictionary for the command and do any traffic data type changes we need to do.

        command_list = self.command_parser(module, command, choice, parameter)

        # command_list will have the following values to indexes as stated below, or None if parse fails.

        # command_list : index - ( ident : 0, base : 1 , code : 2, variant : 3, send_to_port : 4, blocked_data : 5,
        # stepped_data : 6, traffic_data_type : 7, choice : 8, parameter : 9, units : 10, response_regex : 11,
        # response_data_type_name : 12 )

        if command_list is None:

            return 'system', 'PREMATURE_TERMINATION', 'Command not found!!', None

        # Ok if we got this far then we must at least have some data so let's try to run it.

        # Now we find out what type of command we're running, single, blocked or stepped.

        # command_list : index - ( ident : 0, base : 1 , code : 2, variant : 3, send_to_port : 4, blocked_data : 5,
        # stepped_data : 6, traffic_data_type : 7, choice : 8, parameter : 9, units : 10, response_regex : 11,
        # response_data_type_name : 12 )

        if command_list[5] is None and command_list[6] is None:

            if command_list[4] == 'True':

                response = self.single_command(self.instrument.instrument_staribus_address, command_list[0],
                                               command_list[1], command_list[2], command_list[3], command_list[8],
                                               command_list[9], command_list[11], command_list[10])

            else:

                logger.critical('Unable to run command as send to port is true and there are no single commands with that setting')

                return command_list[0], 'PREMATURE_TERMINATION', 'Unable to run command with send to port false', None

        elif command_list[5] is not None:

            response = self.blocked_command(self.instrument.instrument_staribus_address, command_list[0],
                                            command_list[1], command_list[5])

        elif command_list[6] is not None:

            response = command_list[0], 'ABORT', 'Stepped data command is not yet implemented.', None

        else:

            response = command_list[0], 'PREMATURE_TERMINATION', None, None

        return response

    def check_response(self, response, response_regex):

        logger = logging.getLogger('interpreter.check_response')

        #  Not sure this logic makes sense in all cases so beware demons maybe present!!

        if response_regex is not None and response_regex != 'ACK':

            logger.debug('Regex is not None and not ACK')

            logger.debug('Regex : %s' % response_regex)

            if response[1] is not None:

                logger.debug('response[1] : %s' % str(response[1]))

                if re.match(response_regex, response[1]):

                    logger.debug('response[1] matches response_regex')

                    return True

                else:

                    logger.debug("response[1] doesn't match response_regex")

                    return False
            else:

                logger.debug("response[1] is None, returning true")

                return True

        else:

            logger.debug("response_regex is ACK, returning true")

            return True

    # Normal single command.

    def single_command(self, instrument_address, ident, base, code, variant, choice, parameter, response_regex, units):

        logger = logging.getLogger('interpreter.single_command')

        logger.debug('Single command being run.')

        if choice is not None:

            param = choice

        elif parameter is not None:

            param = parameter

        else:

            param = None

        response = self.dao_processor.star_message(instrument_address, base, code, variant, param)

        logger.debug('Response : %s ' % str(response))

        if self.check_response(response, response_regex):

            response = (ident, response[0], response[1], units)

            return response

        else:

            return ident, 'PREMATURE_TERMINATION', None, None

    # Blocked command

    def blocked_command(self, instrument_address, ident, module, blocked):

        '''
        Blocked data commands are almost certainly getData, Starbase probably does this in a much nicer way.
        '''

        logger = logging.getLogger('interpreter.blocked_command')

        # First thing to do is split blocked into a list and make sure we have two commands

        command_codes = blocked.split(',')

        if len(command_codes) < 2:

            logger.warning("BlockedDataCommand hasn't enough command codes specified.")

            return ident, 'PREMATURE_TERMINATION', 'Only one command specified in blocked command, must be minimum of two', None

        # We assume that a blocked data command is getData.

        # Try to locate the primary command in the instrument dictionary.

        primary_command_list = self.command_attributes(module, command_codes[0])

        if primary_command_list is None:

            logger.critical("BlockedDataCommand Unable to locate primary command in instrument dictionary.")

            return ident, 'PREMATURE_TERMINATION', 'Unable to locate primary command in instrument dictionary', None

        else:

            logger.debug('Blocked data command primary command appears to be : %s' % primary_command_list[0])

        # Check send to port is true for primary command otherwise we don't know what to do with it.

        if primary_command_list[4] != 'True':

            logger.critical('Unable to run command as send to port is true and there are no single commands with that setting')

            return primary_command_list[0], 'PREMATURE_TERMINATION', 'Unable to run command with send to port false', None

        # Try to locate the secondary command in the instrument dictionary.

        secondary_command_list = self.command_attributes(module, command_codes[1])

        if secondary_command_list is None:

            logger.critical("BlockedDataCommand Unable to locate secondary command in instrument dictionary.")

            return ident, 'PREMATURE_TERMINATION', 'Unable to locate secondary command in instrument dictionary', None

        else:

            logger.debug('Blocked data command primary command appears to be : %s' % secondary_command_list[0])

        # Check send to port is true for primary command otherwise we don't know what to do with it.

        if secondary_command_list[4] != 'True':

            logger.critical('Unable to run command as send to port is true and there are no single commands with that setting')

            return secondary_command_list[0], 'PREMATURE_TERMINATION', 'Unable to run command with send to port false', None

        # primary / secondary command_list will have the following values to indexes as stated below,
        # or None if parse fails.

        # command_list : index - ( ident : 0, base : 1 , code : 2, variant : 3, send_to_port : 4, blocked_data : 5,
        # stepped_data : 6, traffic_data_type : 7, choice : 8, parameter : 9, units : 10, response_regex : 11,
        # response_data_type_name : 12 )

        # Now we need to sanity check the commands.

        # The Primary command can not have choices or parameters but must have response regex and data type name.

        if primary_command_list[8] is not None:

            logger.critical("BlockedDataCommand primary command has choices which is not allowed.")

            return ident, 'INVALID_XML', 'Primary command has choices!!', None

        if primary_command_list[9] is not None:

            logger.critical("BlockedDataCommand primary command requires parameter which is not allowed.")

            return ident, 'INVALID_XML', 'Primary command requires parameter which is not allowed!!', None

        if primary_command_list[11] is None:

            logger.critical("BlockedDataCommand Primary command hasn't a response regex which is not allowed.")

            return ident, 'INVALID_XML', "Primary command hasn't a response regex which is not allowed!!", None

        else:

            logger.debug('Primary command response regex : %s' % primary_command_list[11])

        if primary_command_list[12] is None:

            logger.critical("BlockedDataCommand Primary command hasn't a data type name which is not allowed.")

            return ident, 'INVALID_XML', "Primary command hasn't a data type name which is not allowed!!", None

        else:

            logger.debug('Primary command response data type name : %s' % primary_command_list[12])

        # The Secondary command can not have choices but must have a parameter, response regex and traffic data type.

        if secondary_command_list[8] is not None:

            logger.critical("BlockedDataCommand secondary command has choices which is not allowed.")

            return ident, 'INVALID_XML', 'Secondary command has choices which is not allowed.!!', None

        if secondary_command_list[9] is None:

            logger.critical("BlockedDataCommand Secondary command hasn't a parameter regex which is not allowed.")

            return ident, 'INVALID_XML', "Secondary command hasn't a parameter regex which is not allowed!!", None

        else:

            logger.debug('Secondary command parameter : %s' % secondary_command_list[9])

        if secondary_command_list[11] is None:

            logger.critical("BlockedDataCommand Secondary command hasn't a response regex which is not allowed.")

            return ident, 'INVALID_XML', "Secondary command hasn't a response regex which is not allowed!!", None

        else:

            logger.debug('Secondary command response regex : %s' % secondary_command_list[11])

        if secondary_command_list[12] is None:

            logger.critical("BlockedDataCommand Secondary command hasn't a data type name which is not allowed.")

            return ident, 'INVALID_XML', "Secondary command hasn't a data type name which is not allowed!!", None

        else:

            logger.debug('Secondary command response data type name : %s' % secondary_command_list[12])

        # We make the assumption that the primary DataTypeName should be the same as the secondary TrafficDataTypeName

        if primary_command_list[12] != secondary_command_list[7]:

            logger.critical("BlockedDataCommand primary and secondary data types do not match!!")

            return ident, 'INVALID_XML', "Primary and secondary data types do not match which is not allowed!!", None

        # command_list : index - ( ident : 0, base : 1 , code : 2, variant : 3, send_to_port : 4, blocked_data : 5,
        # stepped_data : 6, traffic_data_type : 7, choice : 8, parameter : 9, units : 10, response_regex : 11,
        # response_data_type_name : 12 )

        # First we check the primary command will parse and if it does send it to single command.

        if self.command_parser(primary_command_list[1], primary_command_list[2], None, None) is not None:

            response = self.single_command(instrument_address, primary_command_list[0], primary_command_list[1],
                                           primary_command_list[2], primary_command_list[3], None, None,
                                           primary_command_list[11], primary_command_list[10])

        else:

            logger.critical("BlockedDataCommand Unable to parse primary command!!")

            return ident, 'INVALID_XML', "Unable to parse primary command", None

        # Next we check the response status is SUCCESS otherwise we'll return PREMATURE_TERMINATION.

        if not response[1].startswith('SUCCESS'):

            return ident, 'PREMATURE_TERMINATION', None, None

        # If Primary command is SUCCESS then we're going to try run the secondary command.  Again we make the assumption
        # that the primary command response with be a number which we're going to iterate over.

        # First we attempt to turn the data response to an integer so we can count.

        counter = datatypes.DataTypeToInteger(primary_command_list[12], response[2])

        if counter is None:

            logger.critical("BlockedDataCommand Unable to convert primary response value to integer!!")

            return ident, 'PREMATURE_TEMINATION', "Unable to convert primary response value to integer", None

        #  Now deduct one as we always get a block count plus one

        counter -= 1

        # Now check the counter is greater than 0

        if counter < 0:

            logger.critical("BlockedDataCommand Block count less than one.!!")

            return ident, 'PREMATURE_TEMINATION', "NODATA", None

        # Double check the any previous RawData has been saved as this will destroy it otherwise.

        if not utilities.data_state_check(self.data_store, 'standard'):

            return ident, 'ABORT', None, None

        #  Set the data store back to consistent state.

        self.data_store.clear()
        self.metadata.clear()

        # Check the data store is in a good state to start with.

        if not self.data_store.default_state:

            logger.critical('Unable to reset data store.')

            return ident, 'PREMATURE_TERMINATION', 'Unable to reset data store.', None

        # Tell the data store the number of channels.

        self.data_store.channel_count = int(self.instrument.instrument_number_of_channels)
        # Setup progress dialog.

        progressDialog = QtGui.QProgressDialog('Downloading data ...', str("Abort"), 0, counter)

        progressDialog.setWindowTitle(ident)

        progressDialog.setModal(True)

        if self.StyleSheet is not None:
            progressDialog.setStyleSheet(self.StyleSheet)

        progressDialog.setWindowIcon(QtGui.QIcon('images/starbase.png'))

        progressDialog.resize(300, 90)

        progressDialog.show()

        # Now we'll iterate over the block count.

        for i in range(-1, counter):

            progressDialog.setValue(i)

            if progressDialog.wasCanceled():

                # Reset the data store again just to make sure we leave things in a sane state.

                self.data_store.clear()

                return ident, 'ABORT', None, None

            # Change count to the correct DataType to provide to secondary command as a parameter.

            count = datatypes.DataTypeFromInteger(secondary_command_list[7], counter)

            # Check we can parse the secondary command and if we do run it.

            if self.command_parser(secondary_command_list[1], secondary_command_list[2], None, count) is not None:

                response = self.single_command(instrument_address, secondary_command_list[0], secondary_command_list[1],
                                               secondary_command_list[2], secondary_command_list[3], None, count,
                                               secondary_command_list[11], secondary_command_list[10])

            else:

                logger.critical("BlockedDataCommand Unable to parse seconadry command!!")

                return ident, 'INVALID_XML', "Unable to parse secondary command", None

            # Check secondary command response is SUCCESS and if not return the error and hide progress dialog.

            if not response[1].startswith('SUCCESS'):

                progressDialog.hide()

                return ident, response[1], None, None

            # Append raw data to data store list if we have data.

            if len(response[2]) > 0:

                self.data_store.RawDataBlocks.append(response[2])

                # set the data source to instrument so we know where it came from and can run datatranslators etc in the
                # command interpreter.

                self.data_store.DataSource = 'Controller'

            counter -= 1

        else:

            # if the data store has somekind of data then return the original command ident, with the controller reponse
            # of the last run command and set the the last tuple to 'data'

            if len(self.data_store.RawDataBlocks) > 0:

                # set RawDataBlocksAvailable to True

                self.data_store.RawDataBlocksAvailable = True

                # A quick reminder of the response tuple layout

                # response = command identification, status, response value from controller, command units, data store trigger

                response = ident, response[1], None, None

            else:

                logger.warning('Data store appears to have no data.')

                response = ident, 'PREMATURE_TERMINATION', None, None

                # Reset the data store.

                self.data_store.clear()

                if not self.data_store.default_state:

                    logger.critical('Unable to reset data store defaults.')

                    response = ident, 'PREMATURE_TERMINATION', 'Critical error has occurred please check log file.', None

        return response
