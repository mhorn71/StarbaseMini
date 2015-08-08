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
# along with StarbaseMini.  If not, see <http:#www.gnu.org/licenses/>.

import dao
import logging

logger = logging.getLogger('dao.processor')


class DaoProcessor:
    def __init__(self, serial_port, serial_baudrate, serial_timeout, starinet_address,
                 starinet_port, stream):

        self.command_message = dao.StaribusCommandMessage()

        starinet_address = starinet_address
        starinet_port = starinet_port

        if stream == 'Starinet':
            # todo add Starinet Stream.
            self.stream = None
        else:
            try:
                self.message_stream = dao.StaribusStream(serial_port, serial_baudrate, serial_timeout)
            except IOError as msg:
                raise IOError(msg)

    def star_message(self, addr, base, code, variant, param):

        # Construct the Staribus Message this works for both Staribus and Starinet.
        constructed_message = self.command_message.construct(addr, base, code, variant, param)

        if constructed_message == 'MALFORMED_MESSAGE':
            return 'MALFORMED_MESSAGE', None
        else:

            stream_reply = self.message_stream.stream(constructed_message)

            if stream_reply == 'TIMEOUT':
                return 'TIMEOUT'
            else:
                response = stream_reply

            return response
