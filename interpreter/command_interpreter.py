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

import dao


class CommandInterpreter:
    def __init__(self, parent):
        '''
        Initialise the CommandInterpreter.
        :param parent: Parent Object which should be the UI Object.
        :raises: TypeError and IOError
        '''

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
            self.response_regex = None
            response = 'SUCCESS', 'This command wasn\'t send to port'

        if self.check_response(response):
            return response
        else:
            return self.check_response_message

    def blocked(self, addr, base, code, variant, blocked_data, send_to_port):
        # self.parent.status_message('blocked data command')
        self.response_regex = None
        return 'SUCCESS', 'blocked data command'

    def stepped(self, addr, base, code, variant, stepped_data, send_to_port):
        # self.parent.status_message('stepped data command')
        self.response_regex = None
        return 'SUCCESS', 'stepped data command'