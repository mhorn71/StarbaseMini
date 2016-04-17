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


class DaoProcessor:
    def __init__(self, serial_port, serial_baudrate, serial_timeout, starinet_address,
                 starinet_port, stream, staribus_port_type):

        self.logger = logging.getLogger('dao.DaoProcessor')

        self.command_message = dao.StaribusCommandMessage()
        self.response_message = dao.StaribusResponseMessage()

        starinet_address = starinet_address
        starinet_port = starinet_port

        if stream == 'Starinet':
            self.logger.debug('Starinet Stream selected')
            # we use the serial_timeout as well for the StarinetStream.
            try:
                self.message_stream = dao.StarinetStream(starinet_address, starinet_port, serial_timeout)
            except IOError as msg:
                raise IOError(msg)
            else:
                self.logger.debug('Stream set to Starinet')
        else:
            self.logger.debug('Staribus Stream selected')
            if staribus_port_type == 'RS232':

                try:
                    self.message_stream = dao.StaribusStream(serial_port, serial_baudrate, serial_timeout)
                except IOError as msg:
                    raise IOError(msg)
                else:
                    self.logger.debug('Stream set to Staribus')
            elif staribus_port_type == 'RS485':
                # Need to write the RS485 stream interface.
                pass


            else:
                raise IOError('Unknown port type')

    def close(self):
        try:
            self.message_stream.close()
        except AttributeError:
            pass

    def star_message(self, addr, base, code, variant, param):
        '''

        :param addr:
        :param base:
        :param code:
        :param variant:
        :param param:
        :return: tuple (status_message, payload)
                 Error messsages returned : MALFORMED_MESSAGE, ERROR, TIMEOUT
        '''

        # Construct the Staribus Message this works for both Staribus and Starinet.
        constructed_message = self.command_message.construct(addr, base, code, variant, param)
        self.logger.debug('Message command string : %s' % repr(constructed_message))

        if constructed_message == 'MALFORMED_MESSAGE':
            return 'MALFORMED_MESSAGE', None
        else:
            try:
                stream_reply = self.message_stream.stream(constructed_message)
            except IOError as msg:
                return 'ERROR', str(msg)

            if stream_reply == 'TIMEOUT':
                return 'TIMEOUT', None
            else:
                response = self.response_message.decipher(stream_reply)

            return response
