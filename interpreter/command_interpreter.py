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

from PyQt4 import QtGui

import core
import dao


class CommandInterpreter:
    def __init__(self, parent):
        '''
        Initialise the CommandInterpreter.
        :param parent: Parent Object which should be the UI Object.
        :raises: TypeError and IOError
        '''

        self.logger = logging.getLogger('interpreter.CommandInterpreter')

        # Parent object so we can set status messages for blocked and stepped commands.
        self.parent = parent
        self.instrument = self.parent.instrument
        self.data_type = 'data'

        self.response_regex = None
        self.check_response_message = 'INVALID_RESPONSE_MESSAGE', None

        self.segmenter = core.SegmentTimeSeries()

        staribus_port = self.parent.config.get('StaribusPort', 'staribus_port')
        staribus_baudrate = self.parent.config.get('StaribusPort', 'baudrate')
        staribus_timeout = self.parent.config.get('StaribusPort', 'timeout')
        starinet_address = self.instrument.instrument_starinet_address
        starinet_port = self.instrument.instrument_starinet_port

        if starinet_address == 'None':
            self.logger.debug('Starinet address None')
            if self.parent.staribus2starinet_relay_boolean == 'False':
                stream = 'Staribus'
                self.logger.debug('S2S is False so Staribus')
            else:
                stream = 'Starinet'
                starinet_address = self.parent.staribus2starinet_address
                starinet_port = self.parent.staribus2starinet_port
                self.logger.debug('S2S is True so Starinet')
                self.logger.debug('Sending Staribus packets to ' + starinet_address + ':' + starinet_port)
        else:
            self.logger.debug('S2S starinet address not None so Starinet')
            stream = 'Starinet'

        try:
            self.dao_processor = dao.DaoProcessor(staribus_port, staribus_baudrate, staribus_timeout, starinet_address,
                                                  starinet_port, stream)
        except IOError as msg:
            raise IOError(msg)

    def process_command(self, addr, base, code, variant, send_to_port, blocked_data, stepped_data, choice, parameter,
                        response_regex):

        if response_regex is None:
            self.response_regex = None
        else:
            self.response_regex = response_regex

        if self.parent.staribus2starinet_relay_boolean == 'true':
            addr = '00'

        if blocked_data is None and stepped_data is None:
            response = self.single(addr, base, code, variant, choice, parameter, send_to_port)
        elif blocked_data is not None:
            response = self.blocked(addr, base, code, variant, blocked_data, send_to_port)
        elif stepped_data is not None:
            response = self.stepped(addr, base, code, variant, stepped_data, send_to_port)
        else:
            response = 'PREMATURE_TERMINATION', None

        return response

    def check_response(self, response):
        #  Not sure this logic makes sense in all cases so beware demons maybe present!!
        if self.response_regex is not None and self.response_regex != 'ACK':
            if response[1] is not None:
                if re.match(self.response_regex, response[1]):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True

    def single(self, addr, base, code, variant, choice, parameter, send_to_port):

        if send_to_port == 'True':

            if choice is not None:
                param = self.parent.datatranslator.parameter_converter(base, code, variant, choice)
            elif parameter is not None:
                param = self.parent.datatranslator.parameter_converter(base, code, variant, parameter)
            else:
                param = None

            response = self.dao_processor.star_message(addr, base, code, variant, param)

        else:

            if base == '80' and code == '00':  # Import Local

                if self.data_state():

                    self.parent.saved_data_state = False

                    response = core.importer(self.parent.datatranslator, self.parent.metadata_deconstructor)

                    if response[0].startswith('SUCCESS'):
                        self.parent.datatranslator.create_data_array(self.parent.metadata_deconstructor.instrument_number_of_channels)
                        self.data_type = 'csv'

                else:
                    return 'ABORT', None

            elif base == '81' and code == '00':  # Export RawData

                if self.data_type == 'data':
                    response = core.exporter(self.parent.datatranslator, self.instrument, self.parent.metadata_creator,
                                             'data')
                elif self.data_type == 'csv':
                    response = core.exporter(self.parent.datatranslator, self.parent.metadata_deconstructor,
                                             self.parent.metadata_creator, 'csv')

                if response[0].startswith('SUCCESS'):
                    self.parent.saved_data_state = False

            elif base == '50' and code == '00':  # Segment Time Series.

                if self.data_type == 'data':
                    choice = choice.lower()

                    # look at how exporter works.

                    self.segmenter.data_setup(self.parent.datatranslator, self.instrument, self.parent.metadata_creator,
                                              'data')

                    if choice == 'day':
                        response = self.segmenter.segment_day()
                    elif choice == 'week':
                        response = self.segmenter.segment_week()

                elif self.data_type == 'csv':
                    choice = choice.lower()

                    # look at how exporter works.

                    self.segmenter.data_setup(self.parent.datatranslator, self.parent.metadata_deconstructor,
                                              self.parent.metadata_creator, 'csv')

                    if choice == 'day':
                        response = self.segmenter.segment_day()
                    elif choice == 'week':
                        response = self.segmenter.segment_week()

                if response[0].startswith('SUCCESS'):
                    self.parent.saved_data_state = False

            else:
                response = 'PREMATURE_TERMINATION', 'Unknown command.'

        if self.check_response(response):
            return response
        else:
            return self.check_response_message

    def blocked(self, addr, base, code, variant, blocked_data, send_to_port):

        '''
        Blocked data commands are almost certainly getData Starbase probably does this in a much nicer way.
        '''

        if send_to_port == 'True':
            return 'INVALID_XML', 'blocked data command, send to port is True!!'
        else:

            command_codes = blocked_data.split(',')

            self.parent.DataBlock = []

            primary_command_key = None
            secondary_command_key = None

            # Blocked commands cant have more than two sub commands.
            if len(command_codes) == 2:
                pass
            else:
                return 'INVALID_XML', 'Command should consist of two sub commands only'

            # Iter over dict keys to get ident of parent command.
            for key in self.instrument.command_dict.keys():
                if self.instrument.command_dict[key]['Code'] == code and \
                        self.instrument.command_dict[key]['Base'] == base:
                    parent_ident = key

            # Iterate over dict keys and get command idents
            for key in self.instrument.command_dict.keys():
                if self.instrument.command_dict[key]['Code'] == command_codes[0] and \
                        self.instrument.command_dict[key]['Base'] == base:
                    primary_command_key = key
                elif self.instrument.command_dict[key]['Code'] == command_codes[1] and \
                        self.instrument.command_dict[key]['Base'] == base:
                    secondary_command_key = key

            if primary_command_key is None:
                return 'INVALID_XML', 'Primary command not found'

            if secondary_command_key is None:
                return 'INVALID_XML', 'Secondary command not found'

            self.logger.debug('Primary Command Ident : %s' % primary_command_key)
            self.logger.debug('Primary CodeBase : %s' % base)
            self.logger.debug('Primary CommandCode : %s' % command_codes[0])
            pri_variant = self.instrument.command_dict[primary_command_key]['Variant']
            self.logger.debug('Primary variant : %s' % pri_variant)
            pri_choice = self.instrument.command_dict[primary_command_key]['Parameters']['Choices']
            self.logger.debug('Primary choices : %s' % pri_choice)
            pri_parameter = self.instrument.command_dict[primary_command_key]['Parameters']['Regex']
            self.logger.debug('Primary parameter : %s' % pri_parameter )
            pri_stp = self.instrument.command_dict[primary_command_key]['SendToPort']
            self.logger.debug('Primary SendToPort : %s' % pri_stp)
            pri_datatype = self.instrument.command_dict[primary_command_key]['Response']['DataTypeName']
            self.logger.debug('Primary DataTypeName : %s' % pri_datatype)

            if pri_choice != 'None':
                return 'INVALID_XML', 'Blocked primary command has choices which isn\'t allowed.'

            if pri_parameter != 'None':
                return 'INVALID_XML', 'Blocked primary command has a parameter which isn\'t allowed.'

            self.response_regex = self.instrument.command_dict[primary_command_key]['Response']['Regex']
            self.logger.debug('Primary response regex : %s' % self.response_regex)

            primary_command_response = self.single(addr, base, command_codes[0], pri_variant, None, None, pri_stp)

            self.logger.debug('Primary response : %s' % repr(primary_command_response))

            # Check primary response status starts with SUCCESS.
            if primary_command_response[0].startswith('SUCCESS'):
                self.logger.debug('Primary command started with SUCCESS')

                # Check primary response is valid
                if self.check_response(primary_command_response):
                    self.logger.debug('Primary response passed regex check')

                    primary_response = primary_command_response[1]

                    self.logger.debug('Primary command response : %s' % primary_response)

                else:
                    self.logger.debug('Primary response failed regex check.')
                    return primary_command_response
            else:
                self.logger.debug('Primary response didn\'t start with SUCCESS.')
                return primary_command_response

            # Check primary response will pass secondary parameter check if present.

            self.logger.debug('Secondary Command Ident : %s' % secondary_command_key)

            # This line is wrong it should be Response Regex not Parameters.
            secondary_parameter_regex = self.instrument.command_dict[secondary_command_key]['Parameters']['Regex']
            secondary_response_regex = self.instrument.command_dict[secondary_command_key]['Response']['Regex']

            self.logger.debug('Secondary response regex : %s' % secondary_response_regex)

            if secondary_parameter_regex == 'None':
                secondary_parameter_regex = None

            if primary_response is None and secondary_parameter_regex is not None:
                self.logger.debug('PREMATURE_TERMINATION : Secondary command requires a parameter and none is available.')
                return 'PREMATURE_TERMINATION', 'Secondary command requires a parameter and none is available.'

            # reset self.response_regex to secondary response regex
            self.response_regex = secondary_response_regex

            if re.match(secondary_parameter_regex, primary_response):
                try:
                    # Check DataTypeName so we know whether to convert to integer or not.
                    if pri_datatype == 'Integer':
                        count = primary_response
                    elif pri_datatype == 'HexInteger':
                        count = int(primary_response, 16)
                    else:
                        self.logger.debug('PREMATURE_TERMINATION : Primary command DataTypeName unknown.')
                        return 'PREMATURE_TERMINATION', 'Primary command DataTypeName unknown.'

                    self.logger.debug('Secondary command iter count : %s' % str(count))
                except ValueError:
                    self.logger.debug('PREMATURE_TERMINATION : Secondary command expected iterable primary response')
                    return 'PREMATURE_TERMINATION', 'Secondary command expected iterable primary response'

                sec_variant = self.instrument.command_dict[secondary_command_key]['Variant']
                self.logger.debug('Secondary command variant : %s' % sec_variant)
                sec_stp = self.instrument.command_dict[secondary_command_key]['SendToPort']
                self.logger.debug('Secondary SendToPort : %s' % sec_stp)

                if self.data_state():
                    self.parent.datatranslator.clear()
                else:
                    return 'ABORT', None

                progressDialog = QtGui.QProgressDialog('Downloading data ...',
                                 str("Abort"), 0, count)
                progressDialog.setWindowTitle(parent_ident)
                progressDialog.setModal(True)

                if self.parent.style_boolean:
                    with open(self.parent.stylesheet, 'r') as style:
                        progressDialog.setStyleSheet(style.read())

                progressDialog.setWindowIcon(QtGui.QIcon('images/starbase.png'))
                progressDialog.resize(300,90)

                progressDialog.show()

                for i in range(count):

                    progressDialog.setValue(i)

                    if progressDialog.wasCanceled():
                        return 'ABORT', None

                    # if primary response is HexInteger convert integer to hex and fill to four chars with zeros.
                    if pri_datatype == 'HexInteger':
                        datafile = hex(i).split('x')[1].upper().zfill(4)  # change count to hex
                    else:
                        datafile = i

                    secondary_command_response = self.single(addr, base, command_codes[1],
                                                             sec_variant, None, datafile, sec_stp)

                    if secondary_command_response[0].startswith('SUCCESS'):
                        pass
                    else:
                        progressDialog.hide()
                        return secondary_command_response

                    # Check primary response is valid
                    if self.check_response(secondary_command_response):

                        if self.parent.datatranslator.block_parser(secondary_command_response[1], sec_variant):
                            pass
                        else:
                            self.logger.warning('Unable to parse block : %s' % str(datafile))
                            self.logger.warning('Failed data  : %s' % repr(secondary_command_response[1]))
                    else:
                        progressDialog.hide()
                        return 'PREMATURE_TERMINATION', 'NODATA'

                self.parent.datatranslator.create_data_array(self.instrument.instrument_number_of_channels)
                self.parent.saved_data_state = True
                self.data_type = 'data'

                if len(self.parent.datatranslator.data_array) == 0:
                    return 'PREMATURE_TERMINATION', 'NODATA'
                else:
                    return 'SUCCESS', None
            else:
                return 'PREMATURE_TERMINATION', None

    def stepped(self, addr, base, code, variant, stepped_data, send_to_port):
        return 'ABORT', 'stepped data command not yet implemented.'

    def data_state(self):
        '''
        :return: True is it's safe to destroy any unsaved data, else False.
        '''
        if self.parent.saved_data_state is not False:

            message = 'WARNING:  You have unsaved data.\n\nAre you sure you want to continue this will ' + \
                      ' overwrite the unsaved data?'
            header = ''

            result = QtGui.QMessageBox.question(None,
                                                header,
                                                message,
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

            if result == QtGui.QMessageBox.Yes:
                return True
            else:
                return False
        else:
            return True
