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

        self.response_regex = None
        self.check_response_message = 'INVALID_RESPONSE_MESSAGE', None

        staribus_port = self.parent.config.get('StaribusPort', 'staribus_port')
        staribus_baudrate = self.parent.config.get('StaribusPort', 'baudrate')
        staribus_timeout = self.parent.config.get('StaribusPort', 'timeout')
        starinet_address = self.instrument.instrument_starinet_address
        starinet_port = self.instrument.instrument_starinet_port
        # instrument_address = self.instrument.instrument_staribus_address

        if starinet_address == 'None':
            stream = 'Staribus'
        else:
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
                param = choice
            elif parameter is not None:
                param = parameter
            else:
                param = None

            response = self.dao_processor.star_message(addr, base, code, variant, param)

        else:

            response = 'SUCCESS', 'This command wasn\'t send to port'

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

            primary_response = None
            secondary_response = None

            # Blocked commands cant have two sub commands.
            if len(command_codes) == 2:
                pass
            else:
                return 'INVALID_XML', 'Command should consist of two sub commands only'

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

            print('Primary Command Ident : %s' % primary_command_key)
            print('Primary CodeBase : %s' % base)
            print('Primary CommandCode : %s' % command_codes[0])
            pri_variant = self.instrument.command_dict[primary_command_key]['Variant']
            print('Primary variant : %s' % pri_variant)
            pri_choice = self.instrument.command_dict[primary_command_key]['Parameters']['Choices']
            print('Primary choices : %s' % pri_choice)
            pri_parameter = self.instrument.command_dict[primary_command_key]['Parameters']['Regex']
            print('Primary parameter : %s' % pri_parameter )
            pri_stp = self.instrument.command_dict[primary_command_key]['SendToPort']
            print('Primary SendToPort : %s' % pri_stp)
            # if self.instrument.command_dict[primary_command_key]['Response']['Units'] == 'None':
            #     sec_units = None
            # else:
            #     sec_units = self.instrument.command_dict[primary_command_key]['Response']['Units']

            if pri_choice != 'None':
                return 'INVALID_XML', 'Blocked primary command has choices which isn\'t allowed.'

            if pri_parameter != 'None':
                return 'INVALID_XML', 'Blocked primary command has a parameter which isn\'t allowed.'

            self.response_regex = self.instrument.command_dict[primary_command_key]['Response']['Regex']
            print('Primary response regex : %s' % self.response_regex)

            primary_command_response = self.single(addr, base, command_codes[0], pri_variant, None, None, pri_stp)

            print('Primary response : %s' % repr(primary_command_response))

            # Check primary response status starts with SUCCESS.
            if primary_command_response[0].startswith('SUCCESS'):
                print('Primary command started with SUCCESS')

                # Check primary response is valid
                if self.check_response(primary_command_response):
                    print('Primary response passed regex check')

                    primary_response = primary_command_response[1]

                    print('Primary command response : %s' % primary_response)

                    # # Update the UI with the status of the Primary Command.
                    # self.parent.status_message(primary_command_key, primary_command_response[0],
                    #                            primary_command_response[1], sec_units)
                else:
                    print('Primary response failed regex check.')
                    return primary_command_response
            else:
                print('Primary response didn\'t start with SUCCESS.')
                return primary_command_response

            # Check primary response will pass secondary parameter check if present.

            print('Secondary Command Ident : %s' % secondary_command_key)

            secondary_parameter_regex = self.instrument.command_dict[secondary_command_key]['Parameters']['Regex']

            print('Secondary response regex : %s' % secondary_parameter_regex)

            if secondary_parameter_regex == 'None':
                secondary_parameter_regex = None

            if primary_response is None and secondary_parameter_regex is not None:
                print('PREMATURE_TERMINATION : Secondary command requires a parameter and none is available.')
                return 'PREMATURE_TERMINATION', 'Secondary command requires a parameter and none is available.'

            # reset self.response_regex to secondary command regex
            self.response_regex = secondary_parameter_regex

            if re.match(secondary_parameter_regex, primary_response):
                try:
                    count = int(primary_response, 16)
                    print('Secondary command iter count : %s' % str(count))
                except ValueError:
                    print('PREMATURE_TERMINATION : Secondary command expected iterable primary response')
                    return 'PREMATURE_TERMINATION', 'Secondary command expected iterable primary response'

                sec_variant = self.instrument.command_dict[secondary_command_key]['Variant']
                print('Secondary command variant : %s' % sec_variant)
                sec_stp = self.instrument.command_dict[secondary_command_key]['SendToPort']
                print('Secondary SendToPort : %s' % sec_stp)

                # if self.instrument.command_dict[secondary_command_key]['Response']['Units'] == 'None':
                #     pri_units = None
                # else:
                #     pri_units = self.instrument.command_dict[secondary_command_key]['Response']['Units']

                progressDialog = QtGui.QProgressDialog('Downloading data ...',
                                 str("Abort"), 0, count)
                progressDialog.setWindowTitle('getData')
                progressDialog.setModal(True)
                progressDialog.show()

                for i in range(count):

                    progressDialog.setValue(i)

                    if progressDialog.wasCanceled():
                        return 'ABORT', None

                    datafile = hex(i).split('x')[1].upper().zfill(4)  # change count to hex

                    secondary_command_response = self.single(addr, base, command_codes[1],
                                                             sec_variant, None, datafile, sec_stp)

                    if secondary_command_response[0].startswith('SUCCESS'):
                        pass
                    else:
                        progressDialog.hide()
                        return secondary_command_response

                    # Check primary response is valid
                    if self.check_response(secondary_command_response):

                        secondary_response = secondary_command_response[1]

                        self.parent.DataBlock.append(secondary_response)
                        #
                        # # Update the UI with the status of the Primary Command.
                        # self.parent.status_message(secondary_command_key, secondary_command_response[0],
                        #                            secondary_command_response[1], sec_units)
                        # time.sleep(0.1)
                    else:
                        progressDialog.hide()
                        return 'PREMATURE_TERMINATION', 'NODATA'

            return 'SUCCESS', None

    def stepped(self, addr, base, code, variant, stepped_data, send_to_port):
        # self.parent.status_message('stepped data command')
        return 'SUCCESS', 'stepped data command'