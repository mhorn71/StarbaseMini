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

import dao


class CommandInterpreter:
    def __init__(self, parent, type):
        '''
        Initialise the CommandInterpreter with the stream type.
        :param type: Staribus or Starinet
        :raises: TypeError
        '''

        # Parent object so we can set status messages for blocked and stepped commands.
        self.parent = parent
        self.instrument = self.parent.instrument

        self.ident = None

        if type == 'Staribus':
            self.stream = type
        elif type == 'Starinet':
            self.stream = type
        else:
            raise TypeError('Unrecognised Stream Type, should be Staribus or Starinet not : %s' % type)

    def process(self, ident, base, code, variant, send_to_port, blocked_data, stepped_data, choice, parameter):

        if blocked_data is None and stepped_data is None:
            response = self.single(ident, base, code, variant, choice, parameter, send_to_port)
        elif blocked_data is not None:
            response = self.blocked(ident, base, code, variant, blocked_data, send_to_port)
        elif stepped_data is not None:
            response = self.stepped(ident, base, code, variant, stepped_data, send_to_port)
        else:
            response = 'PREMATURE_TERMINATION', None

        return response

    def single(self, ident, base, code, variant, choice, parameter, send_to_port):

        command = base + code + variant

        if send_to_port == 'True':
            if choice is not None:
                message = command + '\x1F' + choice
            elif parameter is not None:
                message = command + '\x1F' + parameter
            else:
                message = command

            if self.stream == 'Staribus':
                response = dao.staribus(message)
            else:
                response = dao.starinet(message)
        else:
            self.parent.status_message('This command wasn\'t send to port')

        return response

    def blocked(self, ident, base, code, variant, blocked_data, send_to_port):
        self.parent.status_message('blocked data command')
        return 'Blocked Yo Yo'

    def stepped(self, ident, base, code, variant, stepped_data, send_to_port):
        self.parent.status_message('stepped data command')
        return 'Stepped Yo Yo'