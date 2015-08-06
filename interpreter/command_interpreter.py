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

        if type == 'Staribus':
            self.stream = None
        elif type == 'Starinet':
            self.stream = None
        else:
            raise TypeError('Unrecognised Stream Type, should be Staribus or Starinet not : %s' % type)

    def process(self, ident, base, code, variant, send_to_port, blocked_data, stepped_data, choice, parameter):
        self.parent.status_message('Ident : %s' % ident)
        self.parent.status_message('Base : %s' % base)
        self.parent.status_message('Code : %s' % code)
        self.parent.status_message('Variant : %s' % variant)
        self.parent.status_message('Send to Port : %s' % send_to_port)
        self.parent.status_message('Blocked data : %s' % blocked_data)
        self.parent.status_message('Stepped data : %s' % stepped_data)
        self.parent.status_message('Choice : %s' % choice)
        self.parent.status_message('Parameter : %s' % parameter)
